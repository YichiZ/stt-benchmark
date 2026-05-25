"""Run diarized STT benchmark — 4 providers x 2 runs x 3 audio files.

Saves all diarized transcripts to output/diarized-transcripts/<audio-slug>/
for evaluation by Claude subagents.
"""

import importlib
import json
import os
import re
import time
from datetime import datetime, timezone

from dotenv import load_dotenv

load_dotenv()

STT_PROVIDERS = {
    "assemblyai": ("src.stt.assemblyai_stt", "ASSEMBLYAI_API_KEY"),
    "deepgram": ("src.stt.deepgram_stt", "DEEPGRAM_API_KEY"),
    "elevenlabs": ("src.stt.elevenlabs_stt", "ELEVENLABS_API_KEY"),
    "cartesia": ("src.stt.cartesia_stt", "CARTESIA_API_KEY"),
}

BENCHMARKS = [
    {
        "name": "Kevin Small Talk (The Office)",
        "audio": "input/Kevin's Small Talk - The Office US [_K-L9uhsBLM].mp3",
    },
    {
        "name": "Anne Hathaway Interview",
        "audio": "input/anne-hathaway-interview.mp3",
    },
    {
        "name": "Friends Afford Dinner",
        "audio": "input/friends-afford-dinner.mp3",
    },
]

NUM_RUNS = 2


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def run_benchmark():
    all_results = []

    for bench in BENCHMARKS:
        bench_slug = slug(bench["name"])
        out_dir = f"output/diarized-transcripts/{bench_slug}"
        os.makedirs(out_dir, exist_ok=True)

        print(f"\n{'=' * 70}")
        print(f"  {bench['name']}")
        print(f"{'=' * 70}")

        for provider_name, (module_path, env_key) in STT_PROVIDERS.items():
            if not os.environ.get(env_key):
                print(f"  [SKIP] {provider_name} — missing {env_key}")
                continue

            mod = importlib.import_module(module_path)

            for run_num in range(1, NUM_RUNS + 1):
                print(f"  {provider_name} run {run_num}/{NUM_RUNS}...", end=" ", flush=True)
                try:
                    result = mod.run(audio_path=bench["audio"])

                    txt_path = f"{out_dir}/{provider_name}_run{run_num}.txt"
                    with open(txt_path, "w") as f:
                        f.write(result["diarized_text"])

                    print(f"{result['elapsed']:.2f}s | "
                          f"speakers={result.get('num_speakers', 'N/A')} | "
                          f"{len(result['text'])} chars")

                    all_results.append({
                        "benchmark": bench["name"],
                        "benchmark_slug": bench_slug,
                        "provider": provider_name,
                        "run": run_num,
                        "elapsed": result["elapsed"],
                        "num_speakers": result.get("num_speakers"),
                        "text_length": len(result["text"]),
                        "diarized_path": txt_path,
                    })
                except Exception as e:
                    print(f"ERROR: {e}")
                    all_results.append({
                        "benchmark": bench["name"],
                        "benchmark_slug": bench_slug,
                        "provider": provider_name,
                        "run": run_num,
                        "error": str(e),
                    })

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    summary_path = f"output/diarized-transcripts/summary_{timestamp}.json"
    with open(summary_path, "w") as f:
        json.dump({"timestamp": timestamp, "num_runs": NUM_RUNS, "results": all_results}, f, indent=2)

    print(f"\n{'=' * 70}")
    print(f"  DONE — {len([r for r in all_results if 'error' not in r])} successful runs")
    print(f"  Transcripts saved to output/diarized-transcripts/")
    print(f"  Summary: {summary_path}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    run_benchmark()
