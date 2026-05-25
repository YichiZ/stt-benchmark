"""Run all configured TTS providers and compare results."""

import importlib
import os
import sys

from dotenv import load_dotenv

load_dotenv()

TTS_PROVIDERS = {
    "elevenlabs": ("src.tts.elevenlabs_tts", "ELEVENLABS_API_KEY"),
    "deepgram": ("src.tts.deepgram_tts", "DEEPGRAM_API_KEY"),
    "openai": ("src.tts.openai_tts", "OPENAI_API_KEY"),
    "cartesia": ("src.tts.cartesia_tts", "CARTESIA_API_KEY"),
    "playht": ("src.tts.playht_tts", "PLAYHT_API_KEY"),
    "google": ("src.tts.google_tts", "GOOGLE_APPLICATION_CREDENTIALS"),
    "polly": ("src.tts.polly_tts", "AWS_ACCESS_KEY_ID"),
}

STT_PROVIDERS = {
    "assemblyai": ("src.stt.assemblyai_stt", "ASSEMBLYAI_API_KEY"),
    "deepgram": ("src.stt.deepgram_stt", "DEEPGRAM_API_KEY"),
    "elevenlabs": ("src.stt.elevenlabs_stt", "ELEVENLABS_API_KEY"),
    "cartesia": ("src.stt.cartesia_stt", "CARTESIA_API_KEY"),
}


def run_tts(providers: list[str] | None = None, text: str | None = None):
    results = []
    targets = providers or list(TTS_PROVIDERS.keys())

    for name in targets:
        if name not in TTS_PROVIDERS:
            print(f"[SKIP] Unknown provider: {name}")
            continue

        module_path, env_key = TTS_PROVIDERS[name]
        if not os.environ.get(env_key):
            print(f"[SKIP] {name} — missing {env_key}")
            continue

        print(f"\n--- {name.upper()} ---")
        try:
            mod = importlib.import_module(module_path)
            kwargs = {"text": text} if text else {}
            result = mod.run(**kwargs)
            results.append(result)
        except Exception as e:
            print(f"[ERROR] {name}: {e}")

    return results


def run_stt(audio_path: str, providers: list[str] | None = None):
    results = []
    targets = providers or list(STT_PROVIDERS.keys())

    for name in targets:
        if name not in STT_PROVIDERS:
            print(f"[SKIP] Unknown STT provider: {name}")
            continue

        module_path, env_key = STT_PROVIDERS[name]
        if not os.environ.get(env_key):
            print(f"[SKIP] {name} — missing {env_key}")
            continue

        print(f"\n--- {name.upper()} (STT) ---")
        try:
            mod = importlib.import_module(module_path)
            result = mod.run(audio_path=audio_path)
            results.append(result)
        except Exception as e:
            print(f"[ERROR] {name}: {e}")

    return results


def print_summary(results: list[dict]):
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"{'Provider':<15} {'Time (s)':<12} {'Size (bytes)':<15}")
    print("-" * 42)
    for r in sorted(results, key=lambda x: x.get("elapsed", 999)):
        print(f"{r['provider']:<15} {r.get('elapsed', 0):.2f}s{'':<6} {r.get('size', 'N/A')}")


if __name__ == "__main__":
    selected = sys.argv[1:] if len(sys.argv) > 1 else None
    results = run_tts(providers=selected)
    if results:
        print_summary(results)
