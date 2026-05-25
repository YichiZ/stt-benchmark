import os
import time

from cartesia import Cartesia
from dotenv import load_dotenv

load_dotenv()

SAMPLE_AUDIO = "output/elevenlabs.mp3"


def run(audio_path: str = SAMPLE_AUDIO):
    client = Cartesia(api_key=os.environ["CARTESIA_API_KEY"])

    start = time.perf_counter()
    with open(audio_path, "rb") as f:
        result = client.stt.transcribe(
            file=f,
            model="ink-whisper",
            language="en",
        )
    elapsed = time.perf_counter() - start

    plain_text = result.text

    print(f"[Cartesia] {elapsed:.2f}s | {len(plain_text)} chars | no diarization support")
    return {
        "provider": "cartesia",
        "elapsed": elapsed,
        "text": plain_text,
        "diarized_text": f"(no diarization)\n{plain_text}",
        "num_speakers": None,
    }


if __name__ == "__main__":
    result = run()
    print(result["diarized_text"])
