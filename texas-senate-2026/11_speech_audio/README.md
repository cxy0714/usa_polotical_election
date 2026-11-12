# 11_speech_audio — 演讲音频与交付分析

**English** — Audio was pulled from every downloaded video and measured, because the
archive's own gap register said delivery, tone and pacing were `unknown`. For
speech-type videos the audio track is also kept as a 64 kbps mono copy, and word-level
captions are captured as timed transcripts. Nothing here interprets *why* a candidate
sounds the way he does; it records what can be measured and marks the rest.

**中文** — 本目录从每段已下载视频中抽出音轨并做测量。档案此前的缺口登记写明：交付方式、
语气与节奏均为 `unknown`。演讲类视频另存 64 kbps 单声道音频副本，并把字幕整理成带时间码的
逐字稿。这里不解释「为什么听起来是这样」，只记录可测的量，其余标注为不可测。

---

## 1. Coverage / 覆盖范围

| | |
|---|---|
| Videos analysed | **145** |
| Speech-type videos | **94** (37.25 h of audio) |
| Audio copies kept (`audio/*.m4a`, 64 kbps mono) | **93** |
| Timed transcripts (`transcripts/`) | **78** |
| Delivery plots (`plots/`) | **93** |
| Segments (60 s windows) | **2542** |

Kinds treated as "speech": rally_speech, victory_speech, concession_speech,
convention_speech, town_hall, interview, final_rally, tour_launch. News packages are
measured but excluded from the candidate comparison, because their audio is mostly
reporter narration.

## 2. Method / 方法

1. **Decode** — `ffmpeg` → 16 kHz mono PCM; the working WAV is deleted after measurement,
   the kept copy is AAC 64 kbps mono.
2. **Speech/silence** — 25 ms frames, 10 ms hop, RMS in dBFS. The noise floor is the 10th
   percentile; the speech threshold is `max(noise+9 dB, min(p95−6 dB, −32 dB))`, then
   150 ms gaps are closed and runs under 120 ms dropped.
3. **Pauses** — silence runs ≥ 0.25 s *inside* the first–last speech span, reported as
   count, mean and maximum length, and per minute of speech.
4. **Loudness** — mean, SD and p10/p90 of dBFS over speech frames (dynamics, not LUFS).
5. **F0** — normalised autocorrelation, 40 ms window / 20 ms hop, 55–400 Hz; the first lag
   within 85 % of the frame maximum is taken as the period (this avoids the usual
   octave-up error from a strong second harmonic), then median-filtered over 5 frames.
   **Indicative only** on rally audio that contains music, applause and PA.
6. **Spectral centroid** — mean over speech frames (a rough brightness/timbre proxy).
7. **Speech rate** — words from the English captions yt-dlp saved (auto or manual).
   `wpm` divides by the caption span; `articulation_wpm` divides by measured speech time.
8. **Rhetoric counters** — pronoun classes, "Texas" mentions, vocabulary richness,
   mean sentence length and the 12 most frequent content words, all from the caption text.

Scripts: `../_staging/vision/analyze_speech.py` (measure) and
`../_staging/vision/gen_audio_readme.py` (this file + figures).

## 3. Deliverables / 交付物

| File | Content |
|---|---|
| `delivery_metrics.csv` | one row per video: speech/silence, pauses, loudness, F0, centroid, caption-derived rate and rhetoric counters |
| `speech_segments.csv` | 60 s windows per video: speech ratio, loudness, F0, words, wpm — the pacing arc |
| `transcripts/<slug>.txt` | caption text (English, verbatim as published) |
| `transcripts/<slug>.cues.csv` | timed cues: start, end, text |
| `transcripts/<slug>.lines.csv` | the same cues merged into readable ~28-word lines, one row per line — the unit used for bilingual alignment |
| `transcripts/<slug>.zh.csv` | machine translation of each line (reading aid, not a quotation source) |
| `audio/<slug>.m4a` | 64 kbps mono audio copy for speech-type videos |
| `plots/<slug>.png` | waveform envelope + VAD + F0 track + caption density |
| `summary_by_candidate.json` | medians per candidate and coverage counts |
| `fig_delivery_comparison.png` | four delivery measures, candidate vs candidate |
| `fig_pacing.png` | words-per-minute vs pause rate per speech |

## 4. Measured delivery / 测量结果

Medians over speech-type videos. n is the number of videos contributing a value.

| Measure | Talarico | Paxton |
|---|---|---|
| speaking share of audio / 说话占比 | 0.67 (n=44) | 0.62 (n=25) |
| pauses ≥0.25 s per minute / 每分钟停顿 | 38.4 (n=43) | 36.3 (n=24) |
| words per minute / 语速 | 123 (n=21) | 159 (n=17) |
| median F0, Hz / 基频中位数 | 207.8 (n=44) | 173.9 (n=25) |
| F0 range, semitones / 音域 | 13.5 (n=44) | 14.0 (n=25) |
| loudness SD, dB / 音量动态 | 7.4 (n=44) | 6.9 (n=25) |
| mean pause, s / 平均停顿 | 0.84 (n=44) | 0.88 (n=25) |

Rhetoric counters (median per speech, caption-derived):

| Counter | Talarico | Paxton |
|---|---|---|
| words per speech | 2036 | 2345 |
| first person I | 21 | 48 |
| we / our / us | 71 | 53 |
| you / your | 24 | 43 |
| they / them / their | 23 | 25 |
| "Texas" | 14 | 22 |

## 5. What can and cannot be claimed / 可以说与不可以说

- **Can**: speech share, pause counts, loudness dynamics, caption-based speaking rate,
  and *indicative* pitch ranges, each per video and per 60 s segment.
- **Cannot**: infer emotion, sincerity, confidence or "tone" from these numbers; infer
  audience reaction from loudness (applause contaminates the VAD); compare venues as if
  microphone and PA were equal — they are not. Rally audio is a *mix*, not a studio feed.
- **Do not average across kinds.** A 20 s news soundbite and a 20 min rally speech are not
  the same measurement; the comparison table already restricts to speech-type videos.

### 5.1 Bilingual reading / 双语阅读

Each transcript is split into lines (about 28 words, or a natural pause) and each line
is machine-translated to Chinese, so the site can show timecode | English | Chinese in
one table. **The Chinese column is a reading aid only**: the source is automatic caption
text that already mishears names, and the translation adds its own errors. Quote the
English line against the video, never the Chinese text.

逐字稿被切成约 28 词一行（或自然停顿），每行再机器翻译成中文，
网站因此能以「时间码 | 英文 | 中文」三列并排。**中文列只是阅读辅助**：
原文本身是自动字幕，已经会误听人名，机翻又会叠加它自己的错误。
引用时一律以英文行对照视频，不得把中文当作候选人的原话。

Every transcript page links to its source video, and each line's timecode is a YouTube
deep link (`?t=` seconds), so a row can be checked against the footage in one click.
每份逐字稿页都链到原视频，每行时间码就是 YouTube 深链接（`?t=秒`）
，点一下就能回到录像里核对那一句。

## 6. Reproduction / 复现

```powershell
python texas-senate-2026/_staging/vision/download_all.py        # video + captions
python texas-senate-2026/_staging/vision/analyze_speech.py      # decode + measure
python texas-senate-2026/_staging/vision/extract_transcript_lines.py  # lines for bilingual tables
python texas-senate-2026/_staging/vision/translate_lines.py --jobs 8      # machine translation (optional)
python texas-senate-2026/_staging/vision/gen_audio_readme.py    # this file + figures
```

## 7. Limits and rights / 局限与版权

1. **Caption coverage is partial.** Where no English captions exist, `words`, `wpm` and the
   rhetoric counters are empty — the delivery measures are still valid.
2. **Auto captions are not transcripts.** They drop punctuation and mishear names; counts
   are approximate (±few %) and sentence statistics are rough.
3. **F0 on mixed audio** can lock onto music or crowd noise. `voiced_ratio` and the wide
   p10–p90 spread show how much of each file is genuinely trackable.
4. **Loudness is dBFS, not LUFS**, and no microphone calibration exists — never compare
   absolute levels across venues.
5. **Rights**: audio is cut from YouTube uploads owned by the campaigns and stations.
   Internal analysis only; not licensed for republication or for re-upload.
