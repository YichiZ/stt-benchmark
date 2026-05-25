import os
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SAMPLE_TEXT = (
    "Hello! This is a test of the OpenAI text-to-speech API. "
    "The quick brown fox jumps over the lazy dog."
)


def run(text: str = SAMPLE_TEXT, voice: str = "alloy", output_path: str = "output/openai.mp3"):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    start = time.perf_counter()
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice=voice,
        input=text,
        response_format="mp3",
    )
    elapsed = time.perf_counter() - start

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    response.stream_to_file(output_path)

    size = os.path.getsize(output_path)
    print(f"[OpenAI] {elapsed:.2f}s | {size:,} bytes | {output_path}")
    return {"provider": "openai", "elapsed": elapsed, "size": size, "path": output_path}


if __name__ == "__main__":
    run()
