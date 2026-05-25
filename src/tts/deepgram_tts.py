import os
import time

from deepgram import DeepgramClient, SpeakOptions
from dotenv import load_dotenv

load_dotenv()

SAMPLE_TEXT = (
    "Hello! This is a test of the Deepgram Aura text-to-speech API. "
    "The quick brown fox jumps over the lazy dog."
)


def run(text: str = SAMPLE_TEXT, voice: str = "aura-asteria-en", output_path: str = "output/deepgram.mp3"):
    client = DeepgramClient(os.environ["DEEPGRAM_API_KEY"])

    options = SpeakOptions(model=voice)

    start = time.perf_counter()
    response = client.speak.rest.v("1").save(output_path, {"text": text}, options)
    elapsed = time.perf_counter() - start

    size = os.path.getsize(output_path)
    print(f"[Deepgram] {elapsed:.2f}s | {size:,} bytes | {output_path}")
    return {"provider": "deepgram", "elapsed": elapsed, "size": size, "path": output_path}


if __name__ == "__main__":
    run()
