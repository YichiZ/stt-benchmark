import os
import time

import boto3
from dotenv import load_dotenv

load_dotenv()

SAMPLE_TEXT = (
    "Hello! This is a test of the Amazon Polly text-to-speech API. "
    "The quick brown fox jumps over the lazy dog."
)


def run(text: str = SAMPLE_TEXT, voice: str = "Joanna", output_path: str = "output/polly.mp3"):
    client = boto3.client("polly")

    start = time.perf_counter()
    response = client.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=voice,
        Engine="neural",
    )
    elapsed = time.perf_counter() - start

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(response["AudioStream"].read())

    size = os.path.getsize(output_path)
    print(f"[Polly] {elapsed:.2f}s | {size:,} bytes | {output_path}")
    return {"provider": "polly", "elapsed": elapsed, "size": size, "path": output_path}


if __name__ == "__main__":
    run()
