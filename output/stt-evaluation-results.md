# STT Provider Evaluation Results

Date: 2026-05-25
Providers: AssemblyAI, Deepgram, ElevenLabs, Cartesia
Runs per provider per audio: 2
Total API calls: 24

## Final Rankings

| Rank | Provider | Kevin | Anne Hathaway | Friends | Average |
|------|----------|-------|---------------|---------|---------|
| 1 | ElevenLabs | 82 | 88 | 85 | 85.0 |
| 2 | AssemblyAI | 78 | 79 | 78 | 78.3 |
| 3 | Cartesia | 45 | 52 | 65 | 54.0 |
| 4 | Deepgram | 58 | 58 | 45 | 53.7 |

## Speed vs Quality

| Provider | Avg Speed | Quality |
|----------|-----------|---------|
| Deepgram | ~6s | Low |
| Cartesia | ~7s | Low |
| ElevenLabs | ~18s | High |
| AssemblyAI | ~22s | Medium-High |

---

## Clip 1: Kevin Small Talk (The Office)

~2 min, ~6 speakers, Kevin speaks in intentionally broken English

### Transcription Differences

- "Yes, me do" -- AssemblyAI/Deepgram/ElevenLabs correct. Cartesia wrote "me too" (loses Kevin's character voice)
- "you no need use" -- ElevenLabs correct. Deepgram wrote "you know need use" (reverses meaning)
- "Stop worry" -- most correct. Cartesia added "-ing", losing Kevin's deliberate truncation
- "Me do now" vs "Me doing now" vs "Me do it now" -- ElevenLabs closest with "Me do now"

### Diarization

- ElevenLabs: 7 speakers, best separation -- Kevin consistently labeled throughout
- AssemblyAI: 6 speakers, reasonable but lumps some distinct speakers
- Deepgram: 6 speakers but badly broken -- one label absorbs Kevin, Jim, AND the moderator
- Cartesia: no diarization

### Consistency

- AssemblyAI: identical across runs
- Deepgram: identical across runs
- Cartesia: identical across runs
- ElevenLabs: minor differences ("best friends" vs "best friend", slight speaker reassignments)

### Scores

| Provider | Score | Justification |
|----------|-------|---------------|
| ElevenLabs | 82 | Best diarization (7 speakers, consistent Kevin label), strong accuracy. Penalized for odd formatting, slight non-determinism, moderate speed. |
| AssemblyAI | 78 | Best formatting and perfect consistency. Good accuracy. Diarization decent but merges some speakers. Slowest (18s). |
| Deepgram | 58 | Fast and deterministic, but diarization badly broken. "know" for "no" is a clear error. Over-fragmented output. |
| Cartesia | 45 | Fast and deterministic, but no diarization. "me too" error loses character voice. Unstructured wall of text. |

---

## Clip 2: Anne Hathaway Interview (Tonight Show)

~7 min, 2 main speakers (Jimmy Fallon + Anne Hathaway)

### Transcription Differences

- ElevenLabs captured stutters, laughter, applause, even "(door opens)" annotations
- AssemblyAI wrote "COVID of Vogue" instead of "cover of Vogue", "Gracie" instead of "racing"
- Deepgram garbled names: "Ed Hathaway", "Andrew Rannan", "Nick Galatzine", "dig for a baby"
- Cartesia: "Devil Wars Prada" (twice), "Felfth Night", "And halfway" instead of "Anne Hathaway"

### Diarization

- AssemblyAI: 2 speakers -- clean Jimmy/Anne split but misses audience entirely
- ElevenLabs: 3-4 speakers -- correctly separates Jimmy, Anne, and audience/band reactions
- Deepgram: 3 speakers but poorly applied -- long stretches merge both speakers into one label
- Cartesia: dashes for turn changes but no labels, breaks down in longer passages

### Consistency

- AssemblyAI: virtually identical between runs (trivial punctuation differences)
- Deepgram: byte-identical across runs
- Cartesia: byte-identical across runs
- ElevenLabs: minor variations (speaker_3 split differently in run 2)

### Scores

| Provider | Score | Justification |
|----------|-------|---------------|
| ElevenLabs | 88 | Best accuracy, rich annotations, good diarization. Slowest; minor run-to-run variance. |
| AssemblyAI | 79 | Very consistent, clean format, good accuracy. Some mishearings ("COVID", "Gracie"); only 2 speakers. |
| Deepgram | 58 | Fastest, perfectly deterministic. Poor diarization, garbled names, merged dialogue. |
| Cartesia | 52 | Deterministic, decent base accuracy. No diarization, wrong proper nouns, merged sections. |

---

## Clip 3: Friends Afford Dinner

~4 min, ~6 characters (Ross, Rachel, Monica, Chandler, Joey, Phoebe) + laugh track

### Transcription Differences

- ElevenLabs: correctly got "carpaccio", "beeper", captured stutters ("Gi- gift?")
- AssemblyAI: also got "carpaccio" and "beeper" right, minor "cha-ching" vs "chit-ching" inconsistency
- Deepgram: "croppuccino" instead of "carpaccio", "paper" instead of "beeper", "disk" instead of "desk"
- Cartesia: "Killing Me Soft" instead of "Killing Me Softly", "paper" instead of "beeper"

### Diarization

- ElevenLabs: 5 speakers -- most reasonable. Ross, Monica, Phoebe, waiter correctly separated, Joey/Chandler grouped
- AssemblyAI: 8 speakers -- over-split, at least one character split across two labels
- Deepgram: 3 speakers for 6+ characters -- nearly useless, massive stretches under one label
- Cartesia: no diarization

### Consistency

- Deepgram: perfectly deterministic
- Cartesia: perfectly deterministic
- AssemblyAI: near-identical (minor speaker attribution differences)
- ElevenLabs: near-identical (minor stutter variations)

### Scores

| Provider | Score | Justification |
|----------|-------|---------------|
| ElevenLabs | 85 | Best accuracy and sensible diarization (5 speakers). Odd formatting spacing. |
| AssemblyAI | 78 | Best formatting, near-equal accuracy. Over-segments speakers (8). |
| Cartesia | 65 | Fast, deterministic, decent base accuracy. No diarization, some errors. |
| Deepgram | 45 | Fastest but worst diarization (3 speakers) and significant transcription errors. |

---

## Provider Summaries

### ElevenLabs (Winner -- 85.0 avg)
Best transcription accuracy and best diarization across all clips. Captures nuance like stutters, laughter, and non-speech sounds. Tradeoffs: slowest provider (~9-37s), slight non-determinism between runs, and odd triple-spacing in formatted output.

### AssemblyAI (Runner-up -- 78.3 avg)
Best formatting and readability, near-perfect determinism, good accuracy. Tradeoffs: slowest on short clips (~18s), tends to over-split speakers (8 on Friends) or under-split (2 on Anne Hathaway), occasional mishearings ("COVID of Vogue").

### Cartesia (3rd -- 54.0 avg)
Fast (~7s) and perfectly deterministic. Decent base transcription accuracy. Fatal limitation: no diarization support at all. Some proper noun errors ("Devil Wars Prada"). Only viable if speed matters and speakers don't.

### Deepgram (4th -- 53.7 avg)
Fastest provider (~3-10s) and perfectly deterministic, but worst diarization (merges multiple speakers into one label across all clips) and notable transcription errors ("croppuccino", "Ed Hathaway", "you know need use"). Speed cannot compensate for accuracy issues.
