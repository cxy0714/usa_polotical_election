---
title: "Video keyframes and face identification"
title_zh: "视频关键帧与人脸识别"
compiled_by: Lead Research Agent
last_updated: 2026-11-18
status: complete
---

# Video keyframes and face identification / 视频关键帧与人脸识别

3 source videos, 36 extracted keyframes and 36 identity rows. The corpus is a convenience sample of publicly available YouTube uploads — debates, rallies, interviews, victory and concession speeches — not a controlled sample of the campaign's video output.

共 3 个来源视频、36 张关键帧、36 条身份判定。语料是公开 YouTube 视频的便利样本——辩论、集会、采访、胜选与承认败选演讲——不是竞选视频产出的受控样本。

## Corpus / 语料

| slug | kind | side | duration (s) | frames | frames with face | attributed |
|---|---|---|---:|---:|---:|---:|
| `GA_collins_perry` | rally | COLLINS | 522 | 12 | 12 | 12 |
| `GA_debate_clip_1` | debate_clip | JOINT | 152 | 12 | 9 | 6 |
| `GA_debate_clip_2` | debate_clip | OSSOFF | 128 | 12 | 12 | 11 |

Identity distribution / 身份分布: COLLINS 23, unknown 7, OSSOFF 6

## Method / 方法

- Frames: ffmpeg scene-change selection (`scene > 0.30`, at most 20 per video, 960 px wide). When a static-camera video yields fewer than six cuts, twelve evenly spaced frames are sampled instead and the row notes this.
- Detection: OpenCV YuNet (`yunet.onnx`), confidence 0.6, on frames upscaled 2× when narrower than 1600 px.
- Identification: OpenCV SFace (`sface.onnx`), cosine similarity against faces detected in the case's licensed portraits; a frame is attributed only when the best match clears 0.363 and beats the runner-up identity by 0.05. Everything else is `unknown`.
- Long videos (over 20 minutes) were downloaded as their first 15 minutes only; the `duration_s` column records the local excerpt, not the full upload.

## Limits / 限制

- The recogniser distinguishes only the two nominees in this case. A moderator, surrogate or crowd member can be assigned to whichever nominee is the closer of the two; the margin rule reduces but does not eliminate this.
- No captions, transcripts or audio measures are produced in this pass.
- Source videos are not committed (size and platform terms); `video_sources.csv` carries the URL and the local file name.
- The archive does not describe clothing, grooming or body language from these frames. `clothing_notes` in the image archive stays `unknown` unless a text source states it.

## Reproduce / 复现

```
python _tools/video_pipeline.py meta     georgia-senate-2026
python _tools/video_pipeline.py download georgia-senate-2026
python _tools/video_pipeline.py frames   georgia-senate-2026
python _tools/video_pipeline.py faces    georgia-senate-2026
```
