import os
import time

from dotenv import load_dotenv
from elevenlabs import ElevenLabs

load_dotenv()

SAMPLE_AUDIO = "output/elevenlabs.mp3"


def run(audio_path: str = SAMPLE_AUDIO):
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

    start = time.perf_counter()
    with open(audio_path, "rb") as f:
        result = client.speech_to_text.convert(
            file=f,
            model_id="scribe_v2",
            language_code="en",
            diarize=True,
        )
    elapsed = time.perf_counter() - start

    plain_text = result.text

    diarized_lines = []
    speakers_seen = set()
    if result.words:
        current_speaker = None
        current_words = []
        for word_info in result.words:
            speaker = getattr(word_info, "speaker_id", None) or "unknown"
            if speaker != current_speaker:
                if current_words and current_speaker is not None:
                    diarized_lines.append(f"Speaker {current_speaker}: {' '.join(current_words)}")
                    speakers_seen.add(current_speaker)
                current_speaker = speaker
                current_words = []
            text = getattr(word_info, "text", "") or getattr(word_info, "word", "")
            current_words.append(text)
        if current_words and current_speaker is not None:
            diarized_lines.append(f"Speaker {current_speaker}: {' '.join(current_words)}")
            speakers_seen.add(current_speaker)

    diarized_text = "\n".join(diarized_lines)

    print(f"[ElevenLabs] {elapsed:.2f}s | {len(plain_text)} chars | {len(diarized_lines)} segments")
    return {
        "provider": "elevenlabs",
        "elapsed": elapsed,
        "text": plain_text,
        "diarized_text": diarized_text,
        "num_speakers": len(speakers_seen),
    }


if __name__ == "__main__":
    result = run()
    print(result["diarized_text"])
