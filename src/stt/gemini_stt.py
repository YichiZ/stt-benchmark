import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

SAMPLE_AUDIO = "output/elevenlabs.mp3"

TRANSCRIPTION_PROMPT = """\
Transcribe this audio with speaker diarization. For each speaker turn, output a line in this format:
Speaker <label>: <text>

Use consistent speaker labels (Speaker A, Speaker B, etc.) throughout.
Transcribe exactly what is said — do not summarize or paraphrase.
Include all filler words, false starts, and disfluencies.
"""


def run(audio_path: str = SAMPLE_AUDIO):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    uploaded_file = client.files.upload(file=audio_path)

    start = time.perf_counter()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[TRANSCRIPTION_PROMPT, uploaded_file],
    )
    elapsed = time.perf_counter() - start

    diarized_text = response.text.strip()

    lines = diarized_text.split("\n")
    speakers_seen = set()
    plain_parts = []
    for line in lines:
        if line.startswith("Speaker ") and ": " in line:
            speaker, text = line.split(": ", 1)
            speakers_seen.add(speaker)
            plain_parts.append(text)
        elif line.strip():
            plain_parts.append(line.strip())

    plain_text = " ".join(plain_parts)

    print(f"[Gemini] {elapsed:.2f}s | {len(plain_text)} chars | {len(speakers_seen)} speakers")
    return {
        "provider": "gemini",
        "elapsed": elapsed,
        "text": plain_text,
        "diarized_text": diarized_text,
        "num_speakers": len(speakers_seen) if speakers_seen else None,
    }


if __name__ == "__main__":
    result = run()
    print(result["diarized_text"])
