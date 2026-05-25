import os
import time

from deepgram import DeepgramClient
from dotenv import load_dotenv

load_dotenv()

SAMPLE_AUDIO = "output/elevenlabs.mp3"


def run(audio_path: str = SAMPLE_AUDIO):
    client = DeepgramClient(api_key=os.environ["DEEPGRAM_API_KEY"])

    with open(audio_path, "rb") as f:
        buffer = f.read()

    start = time.perf_counter()
    response = client.listen.v1.media.transcribe_file(
        request=buffer,
        model="nova-3",
        smart_format=True,
        diarize=True,
        utterances=True,
        request_options={"timeout_in_seconds": 600},
    )
    elapsed = time.perf_counter() - start

    plain_text = response.results.channels[0].alternatives[0].transcript

    diarized_lines = []
    speakers_seen = set()
    for utterance in (response.results.utterances or []):
        speaker = utterance.speaker
        speakers_seen.add(speaker)
        diarized_lines.append(f"Speaker {speaker}: {utterance.transcript}")

    diarized_text = "\n".join(diarized_lines)

    print(f"[Deepgram] {elapsed:.2f}s | {len(plain_text)} chars | {len(response.results.utterances or [])} utterances")
    return {
        "provider": "deepgram",
        "elapsed": elapsed,
        "text": plain_text,
        "diarized_text": diarized_text,
        "num_speakers": len(speakers_seen),
    }


if __name__ == "__main__":
    result = run()
    print(result["diarized_text"])
