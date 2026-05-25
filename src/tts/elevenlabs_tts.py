import os
import time

from dotenv import load_dotenv
from elevenlabs import ElevenLabs

load_dotenv()

SAMPLE_TEXT = (
    "Hello! This is a test of the ElevenLabs text-to-speech API. "
    "The quick brown fox jumps over the lazy dog."
)


def run(text: str = SAMPLE_TEXT, voice: str = "Rachel", output_path: str = "output/elevenlabs.mp3"):
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

    start = time.perf_counter()
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    elapsed = time.perf_counter() - start

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    size = os.path.getsize(output_path)
    print(f"[ElevenLabs] {elapsed:.2f}s | {size:,} bytes | {output_path}")
    return {"provider": "elevenlabs", "elapsed": elapsed, "size": size, "path": output_path}


if __name__ == "__main__":
    run()
