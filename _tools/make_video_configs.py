# -*- coding: utf-8 -*-
"""Curated video lists for the batch-2 cases (hand-picked from search results).

Short-form corpus: debates are represented by broadcast clips and candidate
appearances, because full-length debate downloads do not complete reliably on this
link. Metadata (channel/upload_date/duration) is filled by
`python _tools/video_pipeline.py meta <case>`.
"""
import json
from pathlib import Path

CASES = {
    "michigan-senate-2026": [
        ("MI_rogers_launch", "3t0eJ5AxK6k", "ROGERS", "launch", "Mike Rogers announces 2026 Senate campaign"),
        ("MI_elsayed_response", "oaRGoU6tjcg", "ELSAYED", "interview", "El-Sayed and Rogers on the Senate race before results"),
        ("MI_debate_clip", "GkwwWtkN7Vg", "JOINT", "debate_clip", "El-Sayed and Rogers in the second Senate debate"),
    ],
    "alaska-senate-2026": [
        ("AK_sullivan_floor", "05ym8FZI4ec", "SULLIVAN", "senate_floor", "Sen. Sullivan speaks on voter ID and insider trading"),
        ("AK_peltola_rally_short", "V1hhjF0CS7s", "PELTOLA", "rally", "Peltola holds rally in Anchorage"),
        ("AK_peltola_win", "paxtTdL6d7w", "PELTOLA", "victory_news", "CNN projects Peltola flips Alaska Senate seat"),
    ],
    "iowa-senate-2026": [
        ("IA_hinson_trump", "UVIH-V4fwaw", "HINSON", "rally", "Hinson remarks at Trump rally in Clive"),
        ("IA_turek_victory_short", "1_nOjXLcX1Y", "TUREK", "victory_speech", "Turek victory speech"),
        ("IA_turek_primary", "Aro0e7cn1_s", "TUREK", "primary_speech", "Turek wins the Democratic primary"),
    ],
    "ohio-senate-2026": [
        ("OH_brown_victory", "g6hGBQO3dZU", "BROWN", "victory_speech", "Brown acceptance speech after winning"),
        ("OH_brown_toledo", "fGZ-rOjU83A", "BROWN", "rally", "Brown kick-off event in Toledo"),
        ("OH_husted_concession", "UVz-YhfQTUA", "HUSTED", "concession", "Husted full concession speech"),
        ("OH_husted_launch", "zvsDiT_n298", "HUSTED", "launch", "Husted launches Senate campaign"),
    ],
    "georgia-senate-2026": [
        ("GA_collins_perry", "jpmqt8w2GOM", "COLLINS", "rally", "Collins remarks at Perry rally"),
        ("GA_debate_clip_1", "IrrH_UizdLE", "JOINT", "debate_clip", "Ossoff and Collins trade attacks in second debate"),
        ("GA_debate_clip_2", "ZyRji58xqwg", "OSSOFF", "debate_clip", "Ossoff line on John Lewis and Mike Collins"),
    ],
    "los-angeles-mayor-2026": [
        ("LA_bass_concede", "mulcAF2XEXk", "BASS", "concession", "Bass concedes to Raman"),
        ("LA_raman_win", "UKhyCjIJJjc", "RAMAN", "victory_speech", "Mayor-elect Raman remarks after winning"),
        ("LA_debate_clip", "dMQfRcycEtQ", "JOINT", "debate_clip", "Bass and Raman face off in mayoral debate"),
    ],
}


def main():
    for case, items in CASES.items():
        cfg = [dict(slug=s, video_id=i, candidate_source=c, kind=k, title=t,
                    file=f"{s}_{i}.mp4", channel="unknown", upload_date="unknown")
               for s, i, c, k, t in items]
        p = Path(case) / "_staging" / "vision" / "videos.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
        print(case, len(cfg))


if __name__ == "__main__":
    main()
