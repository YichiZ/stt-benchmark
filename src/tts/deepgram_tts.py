import os
import time

from deepgram import DeepgramClient
from dotenv import load_dotenv

load_dotenv()

SAMPLE_TEXT = (
    "Hello! This is a test of the Deepgram Aura text-to-speech API. "
    "The quick brown fox jumps over the lazy dog."
)


def run(text: str = SAMPLE_TEXT, voice: str = "aura-2-asteria-en", output_path: str = "output/deepgram.mp3"):
    client = DeepgramClient(api_key=os.environ["DEEPGRAM_API_KEY"])

    start = time.perf_counter()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        for chunk in client.speak.v1.audio.generate(
            text=text,
            model=voice,
            encoding="mp3",
        ):
            f.write(chunk)
    elapsed = time.perf_counter() - start

    size = os.path.getsize(output_path)
    print(f"[Deepgram] {elapsed:.2f}s | {size:,} bytes | {output_path}")
    return {"provider": "deepgram", "elapsed": elapsed, "size": size, "path": output_path}


if __name__ == "__main__":
    run()
