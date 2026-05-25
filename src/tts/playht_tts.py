import os
import time

from dotenv import load_dotenv
from pyht import Client
from pyht.client import TTSOptions

load_dotenv()

SAMPLE_TEXT = (
    "Hello! This is a test of the PlayHT text-to-speech API. "
    "The quick brown fox jumps over the lazy dog."
)


def run(text: str = SAMPLE_TEXT, voice: str = "s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json", output_path: str = "output/playht.mp3"):
    client = Client(
        user_id=os.environ["PLAYHT_USER_ID"],
        api_key=os.environ["PLAYHT_API_KEY"],
    )

    options = TTSOptions(voice=voice)

    start = time.perf_counter()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        for chunk in client.tts(text, options):
            f.write(chunk)
    elapsed = time.perf_counter() - start

    size = os.path.getsize(output_path)
    print(f"[PlayHT] {elapsed:.2f}s | {size:,} bytes | {output_path}")
    return {"provider": "playht", "elapsed": elapsed, "size": size, "path": output_path}


if __name__ == "__main__":
    run()
