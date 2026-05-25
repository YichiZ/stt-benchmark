import os
import time

import assemblyai as aai
from dotenv import load_dotenv

load_dotenv()

SAMPLE_AUDIO = "output/elevenlabs.mp3"


def run(audio_path: str = SAMPLE_AUDIO):
    aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]

    config = aai.TranscriptionConfig(
        speech_models=["universal-3-pro"],
        speaker_labels=True,
    )
    transcriber = aai.Transcriber(config=config)

    start = time.perf_counter()
    transcript = transcriber.transcribe(audio_path)
    elapsed = time.perf_counter() - start

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"AssemblyAI error: {transcript.error}")

    diarized_lines = []
    for utterance in (transcript.utterances or []):
        diarized_lines.append(f"Speaker {utterance.speaker}: {utterance.text}")

    diarized_text = "\n".join(diarized_lines)
    plain_text = transcript.text

    print(f"[AssemblyAI] {elapsed:.2f}s | {len(plain_text)} chars | {len(transcript.utterances or [])} utterances")
    return {
        "provider": "assemblyai",
        "elapsed": elapsed,
        "text": plain_text,
        "diarized_text": diarized_text,
        "num_speakers": len(set(u.speaker for u in (transcript.utterances or []))),
    }


if __name__ == "__main__":
    result = run()
    print(result["diarized_text"])
