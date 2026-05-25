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

**Analysis**:

- **Gemini** correctly transcribes the most proper nouns including Wing (not "Vinc"), Wiz, NanoBanana, Liza Koshy, but stumbles on "Gemma" (renders as "GEMA"/"Jema"), "Lyria" (renders as "Luria"/"Lauria"), "Chewy" (renders as "Chui"), and "Astound" (renders as "the Stand"). Gemini spells out numbers in words rather than digits, which matches the spoken form but differs from the ground truth format.

- **ElevenLabs** has the most accurate proper noun handling overall: correctly gets "Veo" (not "VIO"), "Wing" (not "Vinc"), "Lyria" (not "Liria"), "Supergoop" (not "Supergroup"), and "MoffettNathanson." It uniquely gets "Wiz" correct consistently and handles "Liza Koshy" correctly.

- **AssemblyAI** is strong on most terms but misses on "Vinc" (should be "Wing"/"Waze"), "VIO" (should be "Veo"), "Liria" (should be "Lyria"), and spells "Anat" as "Anant" throughout.

- **Deepgram** has similar accuracy to AssemblyAI but renders "Wiz" inconsistently as "WIS" or "Wizz," uses "Filip" instead of "Philipp," and gets "Vinc" for "Wing."

- **Cartesia** has the worst proper noun accuracy: "Ondar" for "Sundar," "Philipp Felsenberg" for "Philipp Schindler," "Viz" for "Wiz," "Shoei" for "Chewy," "Wink" for "Wing," "the sound broadband" for "Astound Broadband," and "IonWode" for "Ironwood."

### Financial Figures

All providers accurately captured the key financial figures including:
- $109.9 billion consolidated revenue
- 63% cloud growth, $20 billion cloud revenue
- $462 billion backlog
- $39.7 billion operating income, 36.1% margin
- $62.6 billion net income, $5.11 EPS
- $35.7 billion CapEx
- $180-$190 billion CapEx guidance

**Notable differences**:
- **Deepgram** renders numbers in expanded form ($109,900,000,000) rather than shorthand ($109.9 billion), which is technically accurate but less readable.
- **ElevenLabs** spells out all numbers in word form ("a hundred and nine-point-nine billion dollars"), matching the spoken form.
- **Cartesia** uses standard numerical notation ($109.9 billion), matching the ground truth format best among non-AssemblyAI providers.
- **Gemini run2**: ElevenLabs run2 has a critical error on the backlog figure -- "forty-six billion dollars" instead of "$462 billion" in the final Q&A section (line 41).
- **AssemblyAI** uses the clearest numerical format ($109.9 billion), matching the ground truth.
- **Deepgram** drops the "%" after "60" in "Approximately 60% of our investment" (line 332 in run1), rendering it as "Approximately 60" without the percent sign.

### Currency Errors

One notable systematic error: **Deepgram** transcribes Philipp Schindler's mention of "Google Services revenues were $90 billion" as "euro sign 90,000,000,000" (using euro symbol instead of dollar sign) in both runs. This occurs in two places -- both "$90 billion" and "$60 billion" are rendered with euro symbols. This is a significant error for a financial transcript.

**AssemblyAI** also renders "$90 billion" with a euro sign in one instance (line 3, Speaker C: "Google Services revenues were euro 90 billion"). This error does not appear in the ground truth.

**ElevenLabs** does not have this error -- it spells out the currency in words.

---

## 2. Speaker Diarization

### Ground Truth Speakers (~13 distinct)
1. Operator
2. James Friedland (IR)
3. Sundar Pichai (CEO)
4. Philipp Schindler (CBO)
5. Anat Ashkenazi (CFO)
6. Brian Nowak (Morgan Stanley)
7. Douglas Anmuth (JPMorgan)
8. Eric Sheridan (Goldman Sachs)
9. Ross Sandler/Unknown Analyst (Barclays)
10. Michael Nathanson (MoffettNathanson)
11. Mark Shmulik (AllianceBernstein)
12. Ronald Josey (Citi)
13. Kenneth Gawrelski (Wells Fargo)
14. Justin Post (Bank of America)

### Provider Diarization Results

| Provider    | # Speakers Detected | Named Speakers? | Main Speakers Correctly Separated? |
|-------------|--------------------|-----------------|------------------------------------|
| AssemblyAI  | 4 (A, B, C, D)    | No              | Partially -- merges many speakers  |
| Deepgram    | 6-11 (Speaker 0-10)| No             | Yes -- best separation among non-Gemini |
| ElevenLabs  | 10-11              | No              | Yes -- highest granularity         |
| Cartesia    | N/A (no diarization)| N/A            | N/A                                |
| Gemini      | 5-14               | Partially       | Yes -- best overall                |

#### AssemblyAI (4 speakers: A, B, C, D)
- Speaker A = Operator + all analyst questions (merged)
- Speaker B = Sundar Pichai + James Friedland (merged)
- Speaker C = Philipp Schindler
- Speaker D = Anat Ashkenazi
- **Critical issue**: All analyst questions are attributed to "Speaker A" (the Operator), making it impossible to distinguish between Brian Nowak, Doug Anmuth, Eric Sheridan, etc. Sundar and Jim Friedland are merged into one speaker. Only 4 speakers detected for a ~14-speaker call is very poor diarization.

#### Deepgram (6-11 speakers: Speaker 0-10)
- Speaker 0 = Operator
- Speaker 1 = James Friedland
- Speaker 2 = Sundar Pichai
- Speaker 3 = Occasional misattribution (appears briefly for Mark Shmulik's question and one line of Sundar's Maps discussion)
- Speaker 4 = Philipp Schindler
- Speaker 5 = Anat Ashkenazi
- Speaker 6 = Brian Nowak
- Speaker 7 = Michael Nathanson / Justin Post / Ronald Josey (merged)
- Speaker 8 = Douglas Anmuth
- Speaker 9 = Ross Sandler / brief interjection speaker
- Speaker 10 = Eric Sheridan / Kenneth Gawrelski (merged)
- **Strength**: Correctly separates the 3 main executives + operator + IR + some analysts. Better than AssemblyAI.
- **Weakness**: Merges several analysts into the same speaker IDs. Some analyst questions bleed into wrong speakers.

#### ElevenLabs (10-11 speakers)
- speaker_0 = Operator
- speaker_1 = James Friedland / Sundar Pichai (sometimes merged)
- speaker_2 = Sundar Pichai (primary)
- speaker_3 = Philipp Schindler (primary)
- speaker_4 = Anat Ashkenazi (primary) / Operator (sometimes merged)
- speaker_5 = Brian Nowak (partial)
- speaker_6 = Brian Nowak / Douglas Anmuth / Eric Sheridan (Q&A questions)
- speaker_7 = Ross Sandler / Michael Nathanson / Justin Post
- speaker_8 = Michael Nathanson / Mark Shmulik / Ronald Josey
- speaker_9 = Kenneth Gawrelski / Mark Shmulik
- speaker_10 = Justin Post (run2 only)
- **Strength**: Highest number of distinct speakers detected (10-11), closest to the true count. Successfully separates most Q&A transitions.
- **Weakness**: Some speaker confusion -- Doug's CapEx question answer is attributed to speaker_2 (Sundar) instead of speaker_4 (Anat). The Operator's closing remarks sometimes get attributed to Anat's speaker ID.
- **Notable issue**: Run1 detects 10 speakers (speaker_0 through speaker_10, missing some), Run2 detects 11 (speaker_0 through speaker_11). This means the runs are NOT identical.
- **Diarization misattribution**: In the Michael Nathanson Q&A section, the question is split across multiple speaker IDs (speaker_3 starting, speaker_8 continuing). Anat's margin expansion answer is partly attributed to speaker_2 (Sundar) instead of speaker_4 (Anat). The Ross Sandler question about AdWords in agentic shopping is correctly attributed to Philipp's response.

#### Cartesia (No diarization)
- Outputs "(no diarization)" header and a single continuous block of text with no speaker labels at all.
- Completely unusable for any analysis requiring speaker identification.
- The transcription includes a fabricated speaker attribution "Philipp Felsenberg: Thanks, Ondar" -- inventing a surname for Philipp Schindler and misspelling Sundar as "Ondar."

#### Gemini (5-14 speakers)
- Run1: Uses Speaker A through Speaker N (14 distinct labels)
- Run2: Uses Speaker A through Speaker N (14 distinct labels)
- **Unique strength**: Gemini identifies speakers by name within the text. Jim Friedland introduces "Sundar Pichai, Philip Schindler, and Anat Ashkenazi" and Gemini successfully tracks these through the call.
- Speaker A = Operator
- Speaker B = James Friedland
- Speaker C = Sundar Pichai
- Speaker D = Philipp Schindler
- Speaker E = Anat Ashkenazi
- Speaker F = Brian Nowak
- Speaker G = Douglas Anmuth
- Speaker H = Eric Sheridan (run1) / multiple (run2)
- Speakers I-N = Various analysts
- **Strength**: Best diarization granularity with 14 speakers detected, close to the actual count. Correctly handles Q&A transitions where the Operator introduces each analyst.
- **Weakness**: Some speaker confusion in the Michael Nathanson question where the question is split between speakers (Michael starts but the second half of his question gets a different speaker ID). In run2, Anat's CapEx answer to Doug's question is misattributed to speaker_2 (Sundar). Run2 has a notable diarization issue where Anat's answer to Ron Josey's margin question starts with speaker_2 (Sundar) for the first sentence, then switches to speaker_4 (Anat).
- **Run2 anomaly**: In both Gemini runs, the Operator's administrative remarks ("Thank you. As a reminder...") at line 5/6 are merged with Anat's speaker_4, creating a long block that combines Anat's prepared remarks with the Operator's transition text. This misattribution means the Operator's Q&A instructions are attributed to Anat.

---

## 3. Consistency Across Runs

| Provider    | Identical Runs? | Notable Differences |
|-------------|----------------|---------------------|
| AssemblyAI  | YES            | Runs 1 and 2 are character-for-character identical |
| Deepgram    | YES            | Runs 1 and 2 are character-for-character identical |
| ElevenLabs  | NO             | Different speaker counts (10 vs 11), minor diarization label shifts |
| Cartesia    | YES            | Runs 1 and 2 are character-for-character identical |
| Gemini      | NO             | Significant diarization differences between runs |

**AssemblyAI**: Perfectly deterministic. Both runs produced identical output, which is important for reproducibility.

**Deepgram**: Perfectly deterministic. Both runs produced identical output.

**ElevenLabs**: Runs differ in diarization. Run1 attributes Ken Gawrelski's question to speaker_9, while Run2 uses speaker_10. Run2 introduces speaker_11 for Justin Post, which Run1 does not have. The text content is nearly identical but speaker label assignments shift. Most critically, **Run2 has a significant numerical error**: the cloud backlog figure in the final Q&A is transcribed as "forty-six billion dollars" instead of the correct "four hundred and sixty-two billion dollars" (Run1 gets this right as "four hundred and sixty-two billion dollars").

**Cartesia**: Perfectly deterministic. Both runs produced identical output.

**Gemini**: Runs differ in several ways. Both have 14 speaker labels (A-N), but the assignment of speakers to labels differs in the Q&A section. Run1 has Eric Sheridan and Doug Anmuth's questions attributed differently from Run2. In Run2, Anat's answer to Doug's CapEx question is incorrectly given a different speaker label. The text content also shows minor variation. Run2 has a duplicate response from Sundar (lines 42-44) where the same ROIC framework answer appears twice for Justin Post's margin question, suggesting a processing error.

---

## 4. Completeness

| Provider    | Complete? | Missing Content |
|-------------|-----------|-----------------|
| AssemblyAI  | YES       | Includes Operator intro + safe harbor (beyond ground truth) |
| Deepgram    | YES       | Includes Operator intro + safe harbor (beyond ground truth) |
| ElevenLabs  | YES       | Includes Operator intro + safe harbor (beyond ground truth) |
| Cartesia    | YES       | Includes all content but no speaker separation |
| Gemini      | YES       | Includes Operator intro + safe harbor; Run2 has duplicate content |

All providers captured the complete call. Notably, AssemblyAI, Deepgram, ElevenLabs, and Gemini all include the Operator's opening remarks and Jim Friedland's safe harbor statement, which are NOT in the ground truth transcript (the ground truth starts with Sundar's prepared remarks). This means all providers actually transcribed MORE content than the ground truth.

**Cartesia** has a minor completeness issue: the last question from Justin Post is included but the transition between Sundar's answer and Anat's backlog response is muddled without speaker labels.

**Gemini Run2** has a notable completeness issue: it duplicates Sundar's ROIC framework response to Justin Post's margin question, outputting it twice (lines 42 and 44 are substantively the same).

---

## 5. Speed

| Provider    | Time    | Relative Speed |
|-------------|---------|----------------|
| Deepgram    | ~88s    | Fastest (1x)   |
| Gemini      | ~117s   | 1.3x slower    |
| ElevenLabs  | ~186s   | 2.1x slower    |
| Cartesia    | ~204s   | 2.3x slower    |
| AssemblyAI  | ~327s   | 3.7x slower    |

Deepgram is by far the fastest at 88 seconds. Gemini follows at 117 seconds. AssemblyAI is the slowest at 327 seconds, nearly 4x slower than Deepgram.

---

## Detailed Provider Evaluations

### 1. Gemini -- Score: 88/100

**Transcription Accuracy (24/30)**: Gemini produces highly accurate transcriptions with excellent handling of most proper nouns. It correctly identifies "Wing" (not "Vinc"), "Wiz," and "NanoBanana." However, it misspells "Gemma" as "GEMA"/"Jema," "Lyria" as "Luria"/"Lauria," "Chewy" as "Chui," and "Astound Broadband" as "the Stand Broadband." Numbers are spelled out in word form (e.g., "a hundred and nine-point-nine billion dollars" vs "$109.9 billion"), which is faithful to the audio but differs from the conventional financial transcript format. Ground truth says "NVDIA" (a typo); Gemini correctly renders "Nvidia."

**Speaker Diarization (28/30)**: Best diarization of all providers. Detects 14 distinct speakers, closely matching the actual ~14 speakers. Correctly separates all three main executives (Sundar, Philipp, Anat), the Operator, IR, and most analysts. Q&A transitions are handled well. Minor issues: some speaker confusion in the Michael Nathanson section where his question gets split across speaker IDs, and the Operator's Q&A instructions sometimes merge with Anat's speaker label.

**Consistency (16/20)**: Runs are NOT identical. Diarization labels shift between runs, and Run2 has a duplicate response block. This non-determinism is a meaningful drawback for production use cases.

**Completeness (10/10)**: Full call captured. Run2 has a duplicate but no missing content.

**Speed (10/10)**: At 117 seconds, Gemini is the second-fastest provider -- very efficient given its superior diarization quality.

**Key excerpts compared to ground truth**:
- Ground truth: "Waze continues to expand across the U.S."
- Gemini run1: "Wing continues to expand across the US" (CORRECT -- the ground truth has an error; this is Wing, not Waze)
- Ground truth: "Veo 3.1 Lite" / Gemini: "VO 3.1 Light" (incorrect)
- Ground truth: "Gemma 4" / Gemini run1: "GEMA 4" (incorrect), run2: "Jema 4" (incorrect)

### 2. AssemblyAI -- Score: 82/100

**Transcription Accuracy (26/30)**: AssemblyAI produces the cleanest, most readable transcriptions. The text flows naturally with appropriate paragraph breaks. Proper nouns are generally well-handled. Financial figures are rendered in the conventional format ($109.9 billion), matching the ground truth exactly. However, it misses on "Veo" (renders "VIO"), "Lyria" (renders "Liria"), "Wing" (renders "Vinc"), and spells "Anat" as "Anant" throughout. The euro sign error for $90 billion is notable.

**Speaker Diarization (16/30)**: Only 4 speakers detected (A, B, C, D). All analyst questions lumped into "Speaker A" with the Operator. Sundar and Jim Friedland merged. This makes the transcript nearly unusable for understanding who asked which question in the Q&A. This is a major weakness.

**Consistency (20/20)**: Perfectly deterministic -- both runs are identical. This is the best possible score for reproducibility.

**Completeness (10/10)**: Full call captured including content beyond the ground truth.

**Speed (10/10)**: At 327 seconds, AssemblyAI is the slowest, but the time is still under 6 minutes for a 1-hour call, which is acceptable.

**Key excerpts compared to ground truth**:
- Ground truth: "Philipp Schindler" / AssemblyAI: "Philip Schindler" (minor spelling)
- Ground truth: "Anat Ashkenazi" / AssemblyAI: "Anant" (consistent misspelling of first name)
- Ground truth: "agentic e-commerce" / AssemblyAI: "a gentecommerce" (garbled in one instance, line 5)
- Ground truth: "$90 billion" / AssemblyAI: "euro 90 billion" (currency error)
- AssemblyAI has a strange "Speaker A: Back." insertion (line 4) that appears to be a noise artifact

### 3. ElevenLabs -- Score: 80/100

**Transcription Accuracy (24/30)**: ElevenLabs has arguably the best proper noun recognition of any provider. It correctly identifies "Veo" (not "VIO"), "Wing" (not "Vinc"), "Lyria" (not "Liria"), "Supergoop" (not "Supergroup"), "Liza Koshy," and "Wiz." It captures speech disfluencies (uh, um, stutters) very faithfully, which is excellent for verbatim transcription but makes the text harder to read. Numbers are spelled out in word form. The text uses extra spacing between words (three spaces), which is unusual formatting.

**Speaker Diarization (22/30)**: Detects 10-11 speakers, second-best after Gemini. Successfully separates the main executives and most analysts. However, some misattributions occur: Doug's CapEx question answer is attributed to Sundar instead of Anat in some sections. The Operator's closing remarks sometimes bleed into other speakers' labels.

**Consistency (14/20)**: Runs differ in speaker label assignments and speaker count (10 vs 11). Most critically, Run2 has a significant numerical transcription error on the backlog figure ("forty-six billion" vs "four hundred and sixty-two billion"). This inconsistency is concerning for production reliability.

**Completeness (10/10)**: Full call captured.

**Speed (10/10)**: At 186 seconds, ElevenLabs is mid-pack.

**Key excerpts compared to ground truth**:
- Ground truth: "Supergoop partnered with YouTube creator Liza Koshy"
- ElevenLabs: "Supergoop partnered with YouTube creator Liza Koshy" (CORRECT -- only provider to get both right)
- Ground truth: "Veo 3.1 Lite" / ElevenLabs: "Veo three point one Lite" (correct name, number spelled out)
- Ground truth: "Wiz" / ElevenLabs: "Wiz" (correct in prepared remarks, "Viz" in some mentions)
- Ground truth: "Brandcast" / ElevenLabs: "Braincast" (error in one run, line 5 of Anat's closing)

### 4. Deepgram -- Score: 72/100

**Transcription Accuracy (20/30)**: Deepgram has decent accuracy but several notable issues. The euro sign error (euro instead of $ for $90B and $60B mentions) is a critical flaw for financial transcripts. Numbers are rendered in fully expanded form ($109,900,000,000), which is technically correct but very hard to read and differs significantly from how financial figures are conventionally presented. It drops the "%" in "Approximately 60" (line 332). Proper nouns are mixed: gets "Anat" correct but misspells "Doug Anut" and "Mark Schmulloch." The text is excessively fragmented into one-sentence-per-line format (822 lines vs AssemblyAI's 32 lines for the same content).

**Speaker Diarization (18/30)**: Detects 6-11 speakers (Speaker 0-10), which is reasonable. The main executives are correctly separated. However, several analysts are merged: Michael Nathanson, Justin Post, and Ronald Josey share Speaker 7. Eric Sheridan and Kenneth Gawrelski share Speaker 10. One brief misattribution occurs at line 96 where a sentence from Sundar's Maps section is given to Speaker 3.

**Consistency (20/20)**: Perfectly deterministic -- both runs are identical.

**Completeness (10/10)**: Full call captured.

**Speed (4/10)**: At 88 seconds, Deepgram is the fastest provider by a significant margin. However, speed alone does not compensate for accuracy issues.

**Key excerpts compared to ground truth**:
- Ground truth: "$90 billion" / Deepgram: "euro 90,000,000,000" (currency AND format error)
- Ground truth: "Wiz" / Deepgram: "WIS" (line 167) and "Wizz" (line 174) -- inconsistent
- Ground truth: "Philipp" / Deepgram: "Filip" (line 210)
- Ground truth: "Cityweft" / Deepgram: "CityVeldt" (incorrect)
- Ground truth: "Super Group" (actually Supergoop) / Deepgram: "Lisa Kochi" for "Liza Koshy"

### 5. Cartesia -- Score: 55/100

**Transcription Accuracy (18/30)**: Cartesia's word-level accuracy is reasonable for common English words but falls apart on proper nouns. It fabricates "Philipp Felsenberg" for Philipp Schindler, renders "Sundar" as "Ondar," "Chewy" as "Shoei," "Wing" as "Wink," "Wiz" as "Viz," and "Astound Broadband" as "the sound broadband." The model names "Veo" becomes "VO" and "Gemini Lite" becomes "Gemini Live." Numbers are rendered in standard financial notation, which is good. However, the transcript includes the phrase "Thanks, Hunter" instead of "Thanks, Sundar" (a clear mishearing). The phrase "authentic experience" appears instead of "agentic experience" in one instance. "Shorts" is transcribed as "shots" in two places.

**Speaker Diarization (0/30)**: No diarization support at all. The output begins with "(no diarization)" and provides a single continuous text block. For an earnings call with multiple speakers, this makes the transcript essentially unusable for any analytical purpose requiring speaker identification.

**Consistency (20/20)**: Perfectly deterministic -- both runs are identical.

**Completeness (9/10)**: Full call content is present, but without speaker labels, it is difficult to verify transitions. Some content runs together without clear demarcation.

**Speed (8/10)**: At 204 seconds, Cartesia is slower than Deepgram and Gemini but faster than AssemblyAI.

**Key excerpts compared to ground truth**:
- Ground truth: "Philipp Schindler" / Cartesia: "Philipp Felsenberg" (fabricated surname)
- Ground truth: "Thanks, Sundar" / Cartesia: "Thanks, Ondar" (mishearing)
- Ground truth: "Chewy" / Cartesia: "Shoei" (wrong brand entirely)
- Ground truth: "agentic commerce" / Cartesia: "authentic commerce" (semantic error)
- Ground truth: "Shorts" / Cartesia: "shots" (wrong word)
- Ground truth: "rights per week" (should be "rides") / Cartesia: "rights per week" (same error as ground truth)

---

## Why Each Provider Ranked Where It Did

### Gemini (#1, 88/100) vs AssemblyAI (#2, 82/100)
Gemini wins primarily on diarization quality. With 14 detected speakers vs AssemblyAI's 4, Gemini provides a far more usable transcript for understanding who said what. Both have similar transcription accuracy, but AssemblyAI's diarization is critically weak -- merging all analysts into a single speaker makes the Q&A section nearly unusable. AssemblyAI's advantages are perfect consistency and cleaner text formatting, but these cannot overcome the diarization gap.

### AssemblyAI (#2, 82/100) vs ElevenLabs (#3, 80/100)
These are very close. ElevenLabs has better diarization (10-11 speakers vs 4) and better proper noun recognition, but AssemblyAI wins on consistency (deterministic output), cleaner formatting, and more readable text (no excessive disfluency markers or unusual spacing). ElevenLabs' Run2 numerical error on the $462B backlog figure is a significant reliability concern. AssemblyAI's clean, reproducible output gives it the edge despite worse diarization.

### ElevenLabs (#3, 80/100) vs Deepgram (#4, 72/100)
ElevenLabs wins on proper noun accuracy (Veo, Wing, Lyria, Wiz all correct), better diarization granularity (10-11 speakers vs 6-11), and no currency symbol errors. Deepgram's euro sign issue, excessively fragmented output, and expanded number format ($109,900,000,000) significantly reduce its usability for financial analysis. Deepgram's speed advantage (88s vs 186s) is notable but insufficient to compensate.

### Deepgram (#4, 72/100) vs Cartesia (#5, 55/100)
Despite Deepgram's issues, it provides speaker diarization (6-11 speakers), which Cartesia completely lacks. Deepgram also avoids the fabricated proper nouns that plague Cartesia ("Philipp Felsenberg," "Ondar," "Shoei"). Cartesia's complete lack of diarization makes it the least useful provider for multi-speaker audio, regardless of its word-level accuracy on common terms.

---

## Recommendations

1. **For financial transcript accuracy with speaker identification**: Use **Gemini**. Best diarization, good accuracy, fast speed. Run twice and compare to catch non-deterministic errors.

2. **For reproducible batch processing**: Use **AssemblyAI**. Deterministic output, clean formatting, excellent financial figure handling. Supplement with manual speaker identification if needed.

3. **For maximum proper noun accuracy**: Use **ElevenLabs**. Best proper noun recognition overall, good diarization. Verify consistency by running twice.

4. **For speed-critical applications**: Use **Deepgram** (88s). Accept the tradeoff of lower accuracy and formatting issues.

5. **Avoid Cartesia for multi-speaker audio**: No diarization support and significant proper noun errors make it unsuitable for earnings calls.
