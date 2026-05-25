import os
import time

from dotenv import load_dotenv
from google.cloud import texttospeech

load_dotenv()

SAMPLE_TEXT = (
    "Hello! This is a test of the Google Cloud text-to-speech API. "
    "The quick brown fox jumps over the lazy dog."
)


def run(text: str = SAMPLE_TEXT, voice: str = "en-US-Journey-F", output_path: str = "output/google.mp3"):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        sample_rate_hertz=24000,
    )

    start = time.perf_counter()
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_params,
        audio_config=audio_config,
    )
    elapsed = time.perf_counter() - start

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(response.audio_content)

    size = os.path.getsize(output_path)
    print(f"[Google] {elapsed:.2f}s | {size:,} bytes | {output_path}")
    return {"provider": "google", "elapsed": elapsed, "size": size, "path": output_path}


if __name__ == "__main__":
    run()
