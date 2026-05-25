import os
import time

from cartesia import Cartesia
from dotenv import load_dotenv

load_dotenv()

SAMPLE_TEXT = (
    "Hello! This is a test of the Cartesia text-to-speech API. "
    "The quick brown fox jumps over the lazy dog."
)


def run(text: str = SAMPLE_TEXT, voice_id: str = "a0e99841-438c-4a64-b679-ae501e7d6091", output_path: str = "output/cartesia.wav"):
    client = Cartesia(api_key=os.environ["CARTESIA_API_KEY"])

    start = time.perf_counter()
    audio_data = client.tts.bytes(
        model_id="sonic-3",
        transcript=text,
        voice_id=voice_id,
        output_format={
            "container": "wav",
            "encoding": "pcm_f32le",
            "sample_rate": 44100,
        },
    )
    elapsed = time.perf_counter() - start

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(audio_data)

    size = os.path.getsize(output_path)
    print(f"[Cartesia] {elapsed:.2f}s | {size:,} bytes | {output_path}")
    return {"provider": "cartesia", "elapsed": elapsed, "size": size, "path": output_path}


if __name__ == "__main__":
    run()
