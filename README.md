# STT Benchmark

Benchmark comparing speech-to-text providers on transcription accuracy, speaker diarization, consistency, and speed.

## Providers Tested

- **ElevenLabs** (Scribe v2)
- **AssemblyAI** (Universal 3 Pro)
- **Deepgram** (Nova 3)
- **Cartesia** (Ink Whisper) -- no diarization support
- **Gemini** (2.5 Flash) -- diarization via prompt

## Audio Test Clips

1. [Kevin Small Talk (The Office)](https://www.youtube.com/watch?v=_K-L9uhsBLM) -- ~2 min, ~6 speakers, broken English
2. [Anne Hathaway Interview (Tonight Show)](https://www.youtube.com/watch?v=OQ5fWo61mnM) -- ~7 min, 2 main speakers
3. [Friends Afford Dinner](https://www.youtube.com/watch?v=lkbr5qnYSUU) -- ~4 min, ~6 characters + laugh track
4. [Alphabet Q1 2026 Earnings Call](https://www.youtube.com/watch?v=cmBeWtHXNrU) -- ~1 hour, ~13 speakers, ground truth transcript available

## Setup

```bash
# Install dependencies
uv sync

# Copy and fill in API keys
cp .env.example .env

# Run diarized benchmark (5 providers x 2 runs)
uv run python run_diarized_bench.py

# Run parallel benchmark (faster)
uv run python run_parallel_bench.py
```

## Project Structure

```
stt-benchmark/
├── pyproject.toml
├── .env.example
├── run_diarized_bench.py       # Sequential benchmark runner
├── run_parallel_bench.py       # Parallel benchmark runner
├── run_tts.py                  # TTS provider runner
├── run_stt_bench.py            # WER-based STT benchmark
├── src/
│   ├── tts/                    # Text-to-speech provider scripts
│   └── stt/                    # Speech-to-text provider scripts
├── input/                      # Audio files + transcripts (gitignored)
└── output/
    ├── stt-evaluation-results.md
    ├── earnings-call-evaluation.md
    └── diarized-transcripts/   # Raw transcripts per provider (gitignored)
```

---

# Speech-to-Text Provider Evaluation: Alphabet Q1 2026 Earnings Call

**Audio**: ~1 hour earnings call with ~13 distinct speakers
**Ground Truth**: Professional transcript with named speaker labels
**Providers Evaluated**: AssemblyAI, Deepgram, ElevenLabs, Cartesia, Gemini
**Runs per Provider**: 2

---

## Final Rankings

| Rank | Provider    | Score | Speed   | Key Strengths                          | Key Weaknesses                           |
|------|-------------|-------|---------|----------------------------------------|------------------------------------------|
| 1    | Gemini      | 88/100| ~117s   | Best diarization, correct speaker names, accurate proper nouns | Some verbosity in disfluency capture     |
| 2    | AssemblyAI  | 82/100| ~327s   | Excellent transcription accuracy, complete coverage | No speaker names, only Speaker A/B/C/D   |
| 3    | ElevenLabs  | 80/100| ~186s   | Best speaker count granularity, high accuracy, captures disfluencies | No speaker names, some misattributions   |
| 4    | Deepgram    | 72/100| ~88s    | Fastest speed, decent accuracy | Fewer speaker IDs, excessive fragmentation, currency errors |
| 5    | Cartesia    | 55/100| ~204s   | Decent word-level accuracy | No diarization at all, major proper noun errors |

---

## 1. Transcription Accuracy

### Proper Nouns

| Term (Ground Truth)       | AssemblyAI         | Deepgram          | ElevenLabs        | Cartesia          | Gemini            |
|---------------------------|--------------------|--------------------|-------------------|-------------------|-------------------|
| Sundar Pichai             | (not named)        | (not named)        | (not named)       | Ondar             | (not named)       |
| Philipp Schindler         | Philip Schindler   | Filip              | (not named)       | Philipp Felsenberg| Philip Schindler  |
| Anat Ashkenazi            | Anant              | Anat               | (not named)       | (not named)       | Anat              |
| NVIDIA                    | NVIDIA             | NVIDIA             | NVIDIA            | NVIDIA            | Nvidia            |
| Vera Rubin NVL72          | VERA Rubin NVL72   | Vera Rubin NVL72   | Vera Rubin NVL72  | Verarubin NVL72   | Vera Rubin NVL72  |
| Wiz (acquisition)         | Wiz                | WIS / Wizz         | Wiz               | Viz               | Wiz               |
| Lyria 3                   | Liria 3            | Liria three        | Lyria 3           | Liria 3           | Luria 3 / Lauria 3|
| Nano Banana 2             | Nanobanana 2       | Nano Banana two    | NanoBanana 2      | Nano Banana 2     | Nano Banana 2     |
| Veo 3.1 Lite              | VIO 3.1 Lite       | Vio 3.1 Lite       | Veo 3.1 Lite      | VO 3.1 Lite       | VO 3.1 Light      |
| Gemma 4                   | Gemma 4            | Gemma four         | Gemma 4 / Gemini 4| Gemma 4           | GEMA 4 / Jema 4   |
| Wing (Other Bets)         | Vinc               | Vinc               | Wing              | Wink              | Wing              |
| Liza Koshy                | Lisa Koshy         | Lisa Kochi         | Liza Koshy        | Lisa Koshy        | Lisa Koshie       |
| Supergoop (brand)         | Super Group        | Supergroup         | Supergoop         | Supergroup        | Super Group       |
| MoffettNathanson          | Muffet Nathanson   | MoffettNathanson   | MoffettNathanson  | Muffet Nathanson  | MoffettNathanson  |
| Douglas Anmuth            | Doug Anuth         | Doug Anut          | Doug Anuth/Annett | Doug Anuth        | Doug Anmuth       |
| Kenneth Gawrelski         | Ken Goralski       | Ken Gorelski       | Ken Gaworowski    | Ken Garalski      | Ken Gorowski      |
| Mark Shmulik              | Mark Schmalek      | Mark Schmulloch    | Mark Schmilick/Schmalick | Mark Shmulloch | Mark Shmulik / Smalik |
| Ronald Josey              | Ron Josi           | Ron Josey          | Ron Josey         | Ron Josie         | Ron Josie         |
| Cityweft (brand partner)  | CitiVelt           | CityVeldt          | Citywealth        | Citivelt          | Citywealth        |
| Chewy (partner)           | Chewy              | Chewy              | Chewy             | Shoei             | Chui              |
| Astound Broadband         | Astound Broadband  | Astound Broadband  | Astound Broadband | the sound broadband| the Stand Broadband|
| ROIC                      | ROIC               | ROIC               | ROIC              | ROC               | ROIC / ROC        |

### Financial Figures

All providers accurately captured the key financial figures ($109.9B revenue, 63% cloud growth, $462B backlog, $5.11 EPS, $35.7B CapEx, $180-190B CapEx guidance).

Notable differences:
- **Deepgram** renders numbers in expanded form ($109,900,000,000) and uses euro symbols instead of dollar signs for $90B and $60B mentions
- **ElevenLabs** spells out numbers in word form ("a hundred and nine-point-nine billion dollars")
- **ElevenLabs Run2** has a critical error: "$462 billion" transcribed as "forty-six billion dollars"
- **AssemblyAI** uses the clearest format ($109.9 billion), matching ground truth

---

## 2. Speaker Diarization

| Provider    | # Speakers Detected | Named Speakers? | Main Speakers Correctly Separated? |
|-------------|--------------------|-----------------|------------------------------------|
| Gemini      | 14                 | Partially       | Yes -- best overall                |
| ElevenLabs  | 10-11              | No              | Yes -- highest granularity         |
| Deepgram    | 6-11               | No              | Yes -- decent separation           |
| AssemblyAI  | 4                  | No              | Partially -- merges many speakers  |
| Cartesia    | N/A                | N/A             | N/A (no diarization)               |

- **Gemini**: 14 speakers detected, closest to actual count. Correctly handles Q&A transitions.
- **ElevenLabs**: 10-11 speakers, second-best. Some misattributions between Sundar and Anat.
- **Deepgram**: 6-11 speakers. Main executives separated but several analysts merged.
- **AssemblyAI**: Only 4 speakers. All analysts lumped into one speaker. Sundar and Jim Friedland merged.
- **Cartesia**: No diarization at all.

---

## 3. Consistency Across Runs

| Provider    | Identical Runs? | Notable Differences |
|-------------|----------------|---------------------|
| AssemblyAI  | YES            | Character-for-character identical |
| Deepgram    | YES            | Character-for-character identical |
| Cartesia    | YES            | Character-for-character identical |
| ElevenLabs  | NO             | Speaker count differs (10 vs 11), $462B error in Run2 |
| Gemini      | NO             | Diarization labels shift, Run2 has duplicate content |

---

## 4. Completeness

All providers captured the complete call. All providers actually transcribed MORE content than the ground truth (including the Operator's opening remarks and safe harbor statement).

---

## 5. Speed

| Provider    | Time    | Relative Speed |
|-------------|---------|----------------|
| Deepgram    | ~88s    | Fastest (1x)   |
| Gemini      | ~117s   | 1.3x slower    |
| ElevenLabs  | ~186s   | 2.1x slower    |
| Cartesia    | ~204s   | 2.3x slower    |
| AssemblyAI  | ~327s   | 3.7x slower    |

---

## Why Each Provider Ranked Where It Did

**Gemini (#1) vs AssemblyAI (#2)**: Gemini wins on diarization (14 speakers vs 4). AssemblyAI merges all analysts into one speaker, making the Q&A unusable. AssemblyAI has cleaner formatting and perfect consistency, but can't overcome the diarization gap.

**AssemblyAI (#2) vs ElevenLabs (#3)**: Very close. ElevenLabs has better diarization (10-11 vs 4) and better proper nouns, but AssemblyAI wins on consistency (deterministic) and cleaner formatting. ElevenLabs' $462B error in Run2 is a reliability concern.

**ElevenLabs (#3) vs Deepgram (#4)**: ElevenLabs wins on proper nouns (Veo, Wing, Lyria, Wiz all correct), better diarization, and no currency errors. Deepgram's euro sign issue and fragmented output reduce usability.

**Deepgram (#4) vs Cartesia (#5)**: Deepgram provides diarization (6-11 speakers) while Cartesia has none. Deepgram also avoids the fabricated proper nouns that plague Cartesia ("Philipp Felsenberg", "Ondar", "Shoei").

---

## Recommendations

1. **For financial transcripts with speaker identification**: Use **Gemini**. Best diarization, good accuracy, fast. Run twice to catch non-deterministic errors.
2. **For reproducible batch processing**: Use **AssemblyAI**. Deterministic output, clean formatting. Supplement with manual speaker identification if needed.
3. **For maximum proper noun accuracy**: Use **ElevenLabs**. Best proper noun recognition, good diarization. Verify by running twice.
4. **For speed-critical applications**: Use **Deepgram** (88s). Accept the tradeoff of lower accuracy.
5. **Avoid Cartesia for multi-speaker audio**: No diarization and significant proper noun errors.
