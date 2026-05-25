"""Run diarized STT benchmark with parallel provider execution."""

import importlib
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

from dotenv import load_dotenv

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
        "name": "Alphabet Q1 2026 Earnings Call",
        "audio": "input/alphabet-q1-2026-earnings-call.mp3",
    },
]

NUM_RUNS = 2


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def run_single(provider_name: str, mod, audio_path: str, out_dir: str, run_num: int) -> dict:
    try:
        result = mod.run(audio_path=audio_path)
        txt_path = f"{out_dir}/{provider_name}_run{run_num}.txt"
        with open(txt_path, "w") as f:
            f.write(result["diarized_text"])
        return {
            "provider": provider_name,
            "run": run_num,
            "elapsed": result["elapsed"],
            "num_speakers": result.get("num_speakers"),
            "chars": len(result["text"]),
            "path": txt_path,
        }
    except Exception as e:
        return {"provider": provider_name, "run": run_num, "error": str(e)}


def run_benchmark():
    all_results = []

    for bench in BENCHMARKS:
        bench_slug = slug(bench["name"])
        out_dir = f"output/diarized-transcripts/{bench_slug}"
        os.makedirs(out_dir, exist_ok=True)

        print(f"\n{'=' * 70}")
        print(f"  {bench['name']} (parallel execution)")
        print(f"{'=' * 70}")

        modules = {}
        for provider_name, (module_path, env_key) in STT_PROVIDERS.items():
            if not os.environ.get(env_key):
                print(f"  [SKIP] {provider_name} — missing {env_key}")
                continue
            modules[provider_name] = importlib.import_module(module_path)

        tasks = []
        for provider_name, mod in modules.items():
            for run_num in range(1, NUM_RUNS + 1):
                tasks.append((provider_name, mod, bench["audio"], out_dir, run_num))

        print(f"  Launching {len(tasks)} tasks in parallel...\n")

        with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
            futures = {
                executor.submit(run_single, *task): task for task in tasks
            }
            for future in as_completed(futures):
                result = future.result()
                provider = result["provider"]
                run_num = result["run"]
                if "error" in result:
                    print(f"  {provider} run {run_num}: ERROR — {result['error']}")
                else:
                    print(
                        f"  {provider} run {run_num}: "
                        f"{result['elapsed']:.2f}s | "
                        f"speakers={result.get('num_speakers', 'N/A')} | "
                        f"{result['chars']} chars"
                    )
                all_results.append(result)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    summary_path = f"output/diarized-transcripts/{bench_slug}/run_summary_{timestamp}.json"
    with open(summary_path, "w") as f:
        json.dump({"timestamp": timestamp, "num_runs": NUM_RUNS, "parallel": True, "results": all_results}, f, indent=2)

    successful = len([r for r in all_results if "error" not in r])
    print(f"\n{'=' * 70}")
    print(f"  DONE — {successful}/{len(all_results)} successful runs")
    print(f"  Transcripts saved to output/diarized-transcripts/{bench_slug}/")
    print(f"  Summary: {summary_path}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    run_benchmark()
