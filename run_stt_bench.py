"""Benchmark STT providers against ground truth VTT transcripts.

Evaluation methods:
  - WER (Word Error Rate): mechanical word-level accuracy
  - Gemini LLM Judge: semantic accuracy, completeness, speaker handling

Usage:
    uv run python run_stt_bench.py                    # all providers, 1 run
    uv run python run_stt_bench.py --runs 3            # all providers, 3 runs
    uv run python run_stt_bench.py elevenlabs deepgram # specific providers
    uv run python run_stt_bench.py --runs 5 cartesia   # specific + multi-run
    uv run python run_stt_bench.py --no-gemini          # WER only, skip Gemini
"""

import argparse
import importlib
import json
import os
import re
import statistics
import time
from datetime import datetime, timezone

from dotenv import load_dotenv
from jiwer import process_words, wer

load_dotenv()

STT_PROVIDERS = {
    "assemblyai": ("src.stt.assemblyai_stt", "ASSEMBLYAI_API_KEY"),
    "deepgram": ("src.stt.deepgram_stt", "DEEPGRAM_API_KEY"),
    "elevenlabs": ("src.stt.elevenlabs_stt", "ELEVENLABS_API_KEY"),
    "cartesia": ("src.stt.cartesia_stt", "CARTESIA_API_KEY"),
    "gemini": ("src.stt.gemini_stt", "GEMINI_API_KEY"),
}

BENCHMARKS = [
    {
        "name": "Kevin Small Talk (The Office)",
        "audio": "input/Kevin's Small Talk - The Office US [_K-L9uhsBLM].mp3",
        "transcript": "input/kevin-small-talk-transcript.en.vtt",
    },
    {
        "name": "Anne Hathaway Interview",
        "audio": "input/anne-hathaway-interview.mp3",
        "transcript": "input/anne-hathaway-interview-transcript.en.vtt",
    },
    {
        "name": "Friends Afford Dinner",
        "audio": "input/friends-afford-dinner.mp3",
        "transcript": "input/friends-afford-dinner-transcript.en.vtt",
    },
]

GEMINI_JUDGE_PROMPT = """\
You are an expert evaluator of speech-to-text transcription quality.

Compare the HYPOTHESIS transcription against the REFERENCE (ground truth) transcription.

Score each dimension from 0 to 100:

1. **semantic_accuracy**: Does the hypothesis capture the correct meaning? Minor word differences that preserve meaning should score high. Major misheard words or phrases that change meaning should score low.
2. **completeness**: Does the hypothesis include all the content from the reference? Missing sentences or sections should score low.
3. **readability**: Is the hypothesis well-formatted and readable? Good punctuation, capitalization, and paragraph structure score high.

Also provide:
- **overall_score**: A weighted overall score (0-100) considering all dimensions.
- **notable_errors**: A list of the most significant transcription errors (max 5), each as a short string.

REFERENCE:
{reference}

HYPOTHESIS:
{hypothesis}

Respond with ONLY a JSON object (no markdown, no code fences):
{{"semantic_accuracy": <int>, "completeness": <int>, "readability": <int>, "overall_score": <int>, "notable_errors": [<string>, ...]}}
"""


def gemini_judge(reference: str, hypothesis: str) -> dict | None:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None

    from google import genai

    client = genai.Client(api_key=api_key)
    prompt = GEMINI_JUDGE_PROMPT.format(reference=reference, hypothesis=hypothesis)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    text = response.text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    return json.loads(text)


def parse_vtt(path: str) -> str:
    with open(path) as f:
        content = f.read()

    text_lines = []
    for line in content.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if re.match(r"\d{2}:\d{2}:\d{2}\.\d+ --> \d{2}:\d{2}:\d{2}\.\d+", line):
            continue
        if re.match(r"^\d+$", line):
            continue
        cleaned = re.sub(r"^-\s*", "", line)
        text_lines.append(cleaned)

    return " ".join(text_lines)


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s']", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def run_single(mod, audio_path: str) -> dict:
    start = time.perf_counter()
    result = mod.run(audio_path=audio_path)
    elapsed = time.perf_counter() - start
    return {"text": result["text"], "elapsed": elapsed}


def run_benchmark(providers: list[str] | None = None, num_runs: int = 1, use_gemini: bool = True):
    targets = providers or list(STT_PROVIDERS.keys())

    gemini_available = use_gemini and bool(os.environ.get("GEMINI_API_KEY"))
    if use_gemini and not gemini_available:
        print("[WARN] GEMINI_API_KEY not set — skipping Gemini judge\n")

    all_results: list[dict] = []

    for bench in BENCHMARKS:
        print(f"\n{'=' * 70}")
        print(f"  {bench['name']}")
        print(f"{'=' * 70}")

        ground_truth = parse_vtt(bench["transcript"])
        gt_normalized = normalize_text(ground_truth)
        gt_word_count = len(gt_normalized.split())
        print(f"Ground truth: {gt_word_count} words | Runs per provider: {num_runs}")
        print(f"Evaluation: WER{' + Gemini' if gemini_available else ''}\n")

        for name in targets:
            if name not in STT_PROVIDERS:
                print(f"[SKIP] Unknown provider: {name}")
                continue

            module_path, env_key = STT_PROVIDERS[name]
            if not os.environ.get(env_key):
                print(f"[SKIP] {name} — missing {env_key}")
                continue

            print(f"--- {name.upper()} ---")
            try:
                mod = importlib.import_module(module_path)

                bench_slug = re.sub(r"[^a-z0-9]+", "-", bench["name"].lower()).strip("-")
                transcript_dir = f"output/transcripts/{bench_slug}"
                os.makedirs(transcript_dir, exist_ok=True)

                run_results = []
                for i in range(num_runs):
                    r = run_single(mod, bench["audio"])
                    hyp_normalized = normalize_text(r["text"])
                    error_rate = wer(gt_normalized, hyp_normalized)
                    word_output = process_words(gt_normalized, hyp_normalized)
                    run_results.append({
                        "wer": error_rate,
                        "elapsed": r["elapsed"],
                        "substitutions": word_output.substitutions,
                        "insertions": word_output.insertions,
                        "deletions": word_output.deletions,
                        "hypothesis_words": len(hyp_normalized.split()),
                        "text": r["text"],
                    })

                    txt_path = f"{transcript_dir}/{name}_run{i + 1}.txt"
                    with open(txt_path, "w") as f:
                        f.write(r["text"])

                    if num_runs > 1:
                        print(f"  Run {i + 1}/{num_runs}: WER={error_rate:.2%} | {r['elapsed']:.2f}s")

                timings = [r["elapsed"] for r in run_results]
                wers = [r["wer"] for r in run_results]
                best_run = min(run_results, key=lambda x: x["wer"])

                avg_wer = statistics.mean(wers)
                avg_time = statistics.mean(timings)
                wer_accuracy = (1 - avg_wer) * 100

                print(f"  {'Avg ' if num_runs > 1 else ''}WER: {avg_wer:.2%} | WER Accuracy: {wer_accuracy:.1f}%")
                if num_runs > 1:
                    print(f"  WER range: {min(wers):.2%} – {max(wers):.2%} | "
                          f"Std dev: {statistics.stdev(wers):.2%}")
                    print(f"  Avg time: {avg_time:.2f}s | "
                          f"Min: {min(timings):.2f}s | Max: {max(timings):.2f}s")
                else:
                    print(f"  Time: {avg_time:.2f}s")
                print(f"  Best run — Sub: {best_run['substitutions']} | "
                      f"Ins: {best_run['insertions']} | Del: {best_run['deletions']}")

                gemini_scores = None
                if gemini_available:
                    print(f"  Gemini judging...", end=" ", flush=True)
                    try:
                        gemini_scores = gemini_judge(ground_truth, best_run["text"])
                        print(f"done")
                        print(f"  Gemini — Overall: {gemini_scores['overall_score']}/100 | "
                              f"Semantic: {gemini_scores['semantic_accuracy']}/100 | "
                              f"Completeness: {gemini_scores['completeness']}/100 | "
                              f"Readability: {gemini_scores['readability']}/100")
                        if gemini_scores.get("notable_errors"):
                            for err in gemini_scores["notable_errors"][:5]:
                                print(f"    - {err}")
                    except Exception as e:
                        print(f"error: {e}")

                print()

                all_results.append({
                    "benchmark": bench["name"],
                    "provider": name,
                    "avg_wer": avg_wer,
                    "min_wer": min(wers),
                    "max_wer": max(wers),
                    "wer_stdev": statistics.stdev(wers) if num_runs > 1 else 0,
                    "wer_accuracy": wer_accuracy,
                    "avg_time": avg_time,
                    "min_time": min(timings),
                    "max_time": max(timings),
                    "best_substitutions": best_run["substitutions"],
                    "best_insertions": best_run["insertions"],
                    "best_deletions": best_run["deletions"],
                    "reference_words": gt_word_count,
                    "num_runs": num_runs,
                    "gemini_overall": gemini_scores["overall_score"] if gemini_scores else None,
                    "gemini_semantic": gemini_scores["semantic_accuracy"] if gemini_scores else None,
                    "gemini_completeness": gemini_scores["completeness"] if gemini_scores else None,
                    "gemini_readability": gemini_scores["readability"] if gemini_scores else None,
                })
            except Exception as e:
                print(f"  [ERROR] {e}\n")

    save_results(all_results, num_runs, gemini_available)
    print_results(all_results, num_runs, gemini_available)


def save_results(results: list[dict], num_runs: int, gemini_available: bool):
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    report = {
        "timestamp": timestamp,
        "num_runs": num_runs,
        "gemini_enabled": gemini_available,
        "results": results,
    }

    report_path = f"output/stt_bench_{timestamp}.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nResults saved to {report_path}")


def print_results(results: list[dict], num_runs: int, gemini_available: bool):
    if not results:
        return

    print(f"\n{'=' * 80}")
    print(f"  RESULTS — RANKED BY COMBINED SCORE ({num_runs} run{'s' if num_runs > 1 else ''} per provider)")
    print(f"{'=' * 80}\n")

    benchmarks = sorted(set(r["benchmark"] for r in results))

    for bench_name in benchmarks:
        bench_results = [r for r in results if r["benchmark"] == bench_name]
        bench_results.sort(key=lambda x: combined_score(x, gemini_available), reverse=True)

        print(f"  {bench_name}")
        if gemini_available:
            print(f"  {'Provider':<15} {'WER Acc':>8} {'Gemini':>8} {'Combined':>10} {'Semantic':>10} "
                  f"{'Complete':>10} {'Readable':>10} {'Time':>8}")
            print(f"  {'-' * 85}")
            for r in bench_results:
                combo = combined_score(r, gemini_available)
                print(
                    f"  {r['provider']:<15} {r['wer_accuracy']:>7.1f}% {r['gemini_overall']:>7}/100 "
                    f"{combo:>9.1f}% {r['gemini_semantic']:>9}/100 "
                    f"{r['gemini_completeness']:>9}/100 {r['gemini_readability']:>9}/100 "
                    f"{r['avg_time']:>7.2f}s"
                )
        else:
            print(f"  {'Provider':<15} {'WER Acc':>10} {'WER':>10} {'Time':>10} {'Sub':>6} {'Ins':>6} {'Del':>6}")
            print(f"  {'-' * 65}")
            for r in bench_results:
                print(
                    f"  {r['provider']:<15} {r['wer_accuracy']:>9.1f}% {r['avg_wer']:>9.2%} "
                    f"{r['avg_time']:>9.2f}s {r['best_substitutions']:>6} "
                    f"{r['best_insertions']:>6} {r['best_deletions']:>6}"
                )
        print()

    # Overall average
    providers_seen = sorted(set(r["provider"] for r in results))
    print(f"  OVERALL AVERAGE")
    if gemini_available:
        print(f"  {'Provider':<15} {'WER Acc':>9} {'Gemini':>9} {'Combined':>10} {'Avg Time':>10}")
        print(f"  {'-' * 56}")
    else:
        print(f"  {'Provider':<15} {'WER Acc':>12} {'Avg WER':>10} {'Avg Time':>10}")
        print(f"  {'-' * 50}")

    averages = []
    for provider in providers_seen:
        pr = [r for r in results if r["provider"] == provider]
        avg_wer_acc = statistics.mean(r["wer_accuracy"] for r in pr)
        avg_wer_val = statistics.mean(r["avg_wer"] for r in pr)
        avg_time = statistics.mean(r["avg_time"] for r in pr)
        avg_gemini = None
        avg_combined = avg_wer_acc
        if gemini_available and all(r["gemini_overall"] is not None for r in pr):
            avg_gemini = statistics.mean(r["gemini_overall"] for r in pr)
            avg_combined = statistics.mean(combined_score(r, gemini_available) for r in pr)
        averages.append((provider, avg_wer_acc, avg_wer_val, avg_gemini, avg_combined, avg_time))

    for provider, avg_wer_acc, avg_wer_val, avg_gemini, avg_combined, avg_time in sorted(
        averages, key=lambda x: -x[4]
    ):
        if gemini_available and avg_gemini is not None:
            print(
                f"  {provider:<15} {avg_wer_acc:>8.1f}% {avg_gemini:>8.1f} "
                f"{avg_combined:>9.1f}% {avg_time:>9.2f}s"
            )
        else:
            print(f"  {provider:<15} {avg_wer_acc:>11.1f}% {avg_wer_val:>9.2%} {avg_time:>9.2f}s")

    print()


def combined_score(result: dict, gemini_available: bool) -> float:
    wer_acc = result["wer_accuracy"]
    if gemini_available and result.get("gemini_overall") is not None:
        return 0.5 * wer_acc + 0.5 * result["gemini_overall"]
    return wer_acc


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark STT providers")
    parser.add_argument("providers", nargs="*", help="Specific providers to test")
    parser.add_argument("--runs", type=int, default=1, help="Number of runs per provider per audio (default: 1)")
    parser.add_argument("--no-gemini", action="store_true", help="Skip Gemini LLM judge, use WER only")
    args = parser.parse_args()

    run_benchmark(
        providers=args.providers or None,
        num_runs=args.runs,
        use_gemini=not args.no_gemini,
    )
