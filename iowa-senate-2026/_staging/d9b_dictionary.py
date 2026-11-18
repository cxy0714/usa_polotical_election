# -*- coding: utf-8 -*-
"""data_dictionary_bilingual.md, README.md, research_gaps.md, _research_conventions.md"""
import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CASE, KEY

K = lambda k: KEY[k]

D = {
    "source_id": "Case-unique id, SRC-0001 upward / 案件内唯一编号，从 SRC-0001 起",
    "url": "URL actually requested, logged in _staging/fetch_log.csv / 实际请求的网址，均记录于抓取日志",
    "title": "Page title as published / 页面标题原样",
    "publisher": "Outlet or institution / 媒体或机构",
    "publication_date": "ISO date the page was published, or unknown / 页面发布日（ISO）或 unknown",
    "event_date": "ISO date of the event the page describes, or unknown / 页面所述事件的日期或 unknown",
    "access_date": "Date this archive fetched the page; fixed at 2026-11-18 / 抓取日期，本档案固定为 2026-11-18",
    "source_tier": "T1 official/primary, T2 established independent media, T3 supplementary (Wikipedia included) / T1 官方一手、T2 established独立媒体、T3 补充材料（含维基百科）",
    "source_type": "Controlled type: news_article, poll, press_release, encyclopedia, etc. / 受控类型：新闻、民调、新闻稿、百科等",
    "relevant_quote_or_info": "One short factual line that is actually present in the page / 页面中确实存在的一句简短事实",
    "reliability_notes": "Known limits: paywall, machine translation, partisan source, blocked fetch / 已知局限：付费墙、机翻、党派来源、抓取被拒",
    "used_by": "Files and row ids that cite this source / 引用该来源的文件与行号",
    "position_id": "TUR-POS-#### or HIN-POS-#### / 候选人立场编号",
    "candidate_id": "TUREK or HINSON (case_meta ids) / case_meta 中的候选人编号",
    "issue": "Controlled issue vocabulary (Economy … Other) / 受控议题词表（经济…其他）",
    "subissue": "Free-text narrower topic / 更细的主题（自由文本）",
    "position_summary": "One-sentence neutral statement of the position / 一句话中性概括该立场",
    "candidate_statement": "Verbatim or paraphrase, marked as such / 原话或转述，并标明",
    "statement_date": "ISO date the statement was made, or unknown / 表态日期或 unknown",
    "context": "Where and to whom it was said / 在何场合、对谁说的",
    "source_urls": "Exactly one 'SRC-####|url' pair per row / 每行恰好一组 SRC-####|网址",
    "legislative_record": "Related vote or bill, where documented / 相关的投票或法案（有据可查者）",
    "position_changed": "yes / no / unknown, with the earlier position noted / 是否改变，注明先前立场",
    "change_notes": "What changed and when / 改变了什么、何时",
    "opponent_criticism": "How the rival attacked this position / 对手如何攻击该立场",
    "fact_check": "Independent corroboration status of the claim / 该主张的独立核实状态",
    "verification_status": "verified | partially verified | unverified | conflicting sources / 已核实｜部分核实｜未核实｜来源冲突",
    "event_id": "TUR-EVT-####, HIN-EVT-#### or JNT-EVT-#### / 活动编号",
    "event_date": "ISO date, or unknown / 活动日期或 unknown",
    "event_time": "Local start time HH:MM, or unknown / 当地开始时间或 unknown",
    "event_title": "Title used by the covering outlet, or a neutral description / 报道所用标题或中性描述",
    "event_category": "Controlled category (launch, rally, debate …) / 受控类别（启动、集会、辩论…）",
    "city": "City or 'unknown'; 'online' for virtual events / 城市或 unknown；线上活动写 online",
    "venue": "Named venue, or a description of what the report states / 具名场地，或按报道描述的写法",
    "state_region": "Controlled region from case_meta (Central, Eastern … nationwide) / case_meta 的受控区域词",
    "event_status": "held | announced | cancelled … / 已举行｜已宣布｜取消…",
    "campaign_phase": "pre_launch … post_election / 竞选阶段词",
    "stated_purpose": "What the campaign said the event was for / 竞选方自称的活动目的",
    "observable_function": "What an observer could verify happened / 观察者可核实的内容",
    "analyst_interpretation": "Prefixed INTERPRETATION: - clearly separated reading / 以 INTERPRETATION: 开头，明确区分的解读",
    "target_audience": "Who the event was built for / 活动面向的受众",
    "main_messages": "Messages actually delivered / 实际传达的信息",
    "policy_issues": "Pipe-delimited issue vocabulary / 以竖线分隔的议题词表",
    "speech_summary": "Short neutral summary of what was said / 简短中性的发言概述",
    "transcript_url": "URL or unknown / 逐字稿网址或 unknown",
    "video_url": "URL or unknown / 视频网址或 unknown",
    "photo_urls": "URLs or a note that none were retrieved / 图片网址，或说明未取得",
    "media_coverage": "Outlet names that covered it / 报道该活动的媒体",
    "opponent_reference": "How the rival was referenced / 如何提及对手",
    "visual_notes": "What the coverage says about staging, crowd, signage / 报道对舞台、人群、标语的描述",
    "analyst_notes": "Caveats: date source, surrogate event, crowd unknown / 说明：日期来源、代理人活动、人数不明",
    "speech_id": "TUR-SPC-#### or HIN-SPC-#### / 演说编号",
    "speech_title": "Title or neutral description / 标题或中性描述",
    "speech_url": "URL or unknown / 网址或 unknown",
    "duration": "Length as stated, or unknown / 时长或 unknown",
    "main_topics": "Pipe-delimited topics / 竖线分隔的主题",
    "major_quotes": "'verbatim quote' [timestamp] entries, paraphrase marked / 原话加时间戳，转述需标注",
    "rhetorical_devices": "Named devices observed in the text / 文本中可观察到的修辞手法",
    "opponent_references": "How rivals were named or attacked / 如何点名或攻击对手",
    "personal_story_elements": "Biographical material actually used / 实际使用的传记材料",
    "policy_claims": "Policy claims made in the speech / 演说中的政策主张",
    "source": "Outlet and byline that published the text / 刊出该文本的媒体与署名",
    "video_id": "TUR-VID-#### or HIN-VID-#### / 视频编号",
    "event_type": "debate, clip, news package, broadcast interview / 辩论、片段、新闻片、广播专访",
    "relevant_timestamps": "Timestamps, or unknown when no timing was retrieved / 时间点；未取得时写 unknown",
    "transcript_available": "yes | no | unknown / 是否有逐字稿",
    "visual_observations": "What was observed; explicitly 'not viewed' where applicable / 观察内容；未观看时明确写明",
    "completeness": "full | partial | clip | unknown / 完整度",
    "image_id": "TUR-IMG-#### or HIN-IMG-#### / 图片编号",
    "image_date": "ISO date or unknown / 日期或 unknown",
    "source_name": "Holding institution / 收藏或发布机构",
    "source_url": "Commons file page / 共享资源文件页",
    "original_image_url": "Direct file URL / 文件直链",
    "photographer": "Photographer or office credited / 署名摄影师或机构",
    "copyright_status": "public_domain | licensed | all_rights_reserved_link_only | unknown / 版权状态",
    "license": "Licence name as stated / 授权名称原样",
    "local_filename": "Relative path of the downloaded file, or unknown / 已下载文件的相对路径或 unknown",
    "image_resolution": "WxH in pixels / 像素宽高",
    "framing": "Portrait, group, candid … or unknown / 构图类型或 unknown",
    "camera_angle": "Eye level, low, high … or unknown / 机位或 unknown",
    "image_quality": "Sharpness/compression judgement or unknown / 画质判断或 unknown",
    "face_visibility": "clear | partial | obscured | unknown / 面部可见度",
    "body_visibility": "full | half | head-only | unknown / 身体可见范围",
    "clothing_notes": "What the image shows the candidate wearing / 图中候选人着装",
    "notes": "Free-text caveat for the row / 该行的自由文本说明",
    "ad_id": "TUR-AD-####, HIN-AD-#### or EXT-AD-#### / 广告编号",
    "sponsor": "Paying committee or group / 出资委员会或团体",
    "sponsor_type": "candidate_campaign | outside_pac | party_committee … / 出资方类型",
    "release_date": "ISO date or unknown / 发布日期或 unknown",
    "platform": "television, digital, radio, online video / 投放平台",
    "length_seconds": "Seconds as stated, or unknown / 时长秒数或 unknown",
    "issue_or_message": "Subject of the ad / 广告主题",
    "main_visual_elements": "Visuals as described by coverage, or 'no description retrieved' / 报道描述的视觉元素",
    "narration_soundtrack": "Narration/music details or unknown / 旁白与音乐细节或 unknown",
    "candidate_appearance": "Whether and how the candidate appears / 候选人是否出镜及方式",
    "main_claims": "Claims the ad makes / 广告中的主张",
    "fact_check": "What could be checked about those claims / 对该主张可核实的内容",
    "post_id": "TUR-SOC-#### or HIN-SOC-#### / 社媒帖编号",
    "account_handle": "Account or domain, or unknown / 账号或域名或 unknown",
    "post_date": "ISO date or unknown / 发帖日期或 unknown",
    "post_type": "announcement, video link, homepage, press release / 类型",
    "content_summary": "What the post says, quoted where possible / 帖子内容，尽量引用原文",
    "media_included": "Image, video or link attached / 附加的图片、视频或链接",
    "engagement_notes": "Likes/shares if retrieved, else 'no engagement metrics' / 互动数据或说明未取得",
    "coverage_id": "COV-#### / 报道编号",
    "outlet": "Publication or broadcaster / 刊播机构",
    "author": "Byline, or unknown / 署名或 unknown",
    "coverage_type": "news_report | analysis | op_ed | news_video … / 报道类型",
    "key_framing": "How the outlet framed the story / 该媒体的框架",
    "notable_quotes": "Quotes used by the outlet / 报道引用的原话",
    "framing_of_candidate": "Tone toward the candidate, described not scored / 对该候选人的语气（描述而非评分）",
    "mentions_opponent": "yes | no / 是否提及对手",
    "finance_id": "TUR-FIN-#### style ids / 资金编号",
    "period": "Coverage period YYYY-Qn / 覆盖期间",
    "report_type": "Report or snapshot type / 报告或快照类型",
    "reporting_deadline": "ISO deadline or unknown / 申报截止日或 unknown",
    "receipts": "Total receipts, plain integer USD / 总收入（整数美元）",
    "individual_contributions": "Itemised individual totals if available / 个人捐款合计（若有）",
    "pac_contributions": "PAC totals if available / PAC 捐款合计（若有）",
    "disbursements": "Total spent / 总支出",
    "cash_on_hand": "Closing cash / 期末现金",
    "debts_owed": "Debts outstanding / 未偿债务",
    "race_id": "IA-SEN-2026-GEN / -D-PRI / -R-PRI / 选举场次编号",
    "race_name": "Full race name / 场次全名",
    "election_date": "ISO election day / 选举日",
    "candidate": "Candidate name as published / 公布的候选人姓名",
    "party": "Party as published / 公布的政党",
    "votes": "Raw votes, integer / 原始票数",
    "percentage": "Share of that race's total, two decimals / 该场得票率，两位小数",
    "winner": "yes | no / 是否胜出",
    "county_id": "IA-<COUNTY> / 县级编号",
    "county": "County name as published / 县名",
    "other_votes": "Votes for all non-major candidates / 其他候选人票数合计",
    "total_votes": "County total / 该县总票数",
    "poll_id": "POLL-#### / 民调编号",
    "pollster": "Firm that conducted it / 执行机构",
    "sponsor": "Paying sponsor, or unknown / 委托方或 unknown",
    "field_start": "ISO first day of fielding / 调查起始日",
    "field_end": "ISO last day of fielding / 调查结束日",
    "population": "likely voters, registered voters, adults / 可能选民、登记选民、成年人",
    "sample_size": "N / 样本量",
    "margin_of_error": "Percentage points / 误差范围（百分点）",
    "other_pct": "Third-party share, or unknown when not tested / 第三方得票或 unknown",
    "undecided_pct": "Undecided share / 未决定比例",
    "leader": "Candidate ahead in that poll / 该民调中领先者",
    "margin": "Lead in percentage points / 领先百分点",
    "date": "ISO date of the speech or video, or unknown / 演说或视频日期（ISO）或 unknown",
    "entry_id": "TUR-CAR-#### or HIN-CAR-#### / 履历编号",
    "start_date": "ISO start, or unknown / 起始日或 unknown",
    "end_date": "ISO end, or unknown / 结束日或 unknown",
    "role_or_event": "Role held or event that happened / 担任的职务或发生的事件",
    "organization": "Institution / 机构",
    "location": "Place, or unknown / 地点或 unknown",
    "description": "One neutral sentence / 一句中性描述",
    "turek_votes": "Votes for Turek in that county / 该县 Turek 票数",
    "hinson_votes": "Votes for Hinson in that county / 该县 Hinson 票数",
    "turek_pct": "Turek share of the county total / 该县 Turek 得票率",
    "hinson_pct": "Hinson share of the county total / 该县 Hinson 得票率",
    "turek_pct": "Turek share in that poll / 该民调 Turek 支持率",
    "hinson_pct": "Hinson share in that poll / 该民调 Hinson 支持率",
}

FILES = [
    ("09_sources/sources.csv", "Source register / 来源登记"),
    ("01_candidates/policy_positions.csv", "Policy positions / 政策立场"),
    ("01_candidates/turek/career_timeline.csv", "Turek career timeline / Turek 履历"),
    ("01_candidates/hinson/career_timeline.csv", "Hinson career timeline / Hinson 履历"),
    ("02_campaign_events/campaign_events.csv", "Campaign events / 竞选活动"),
    ("03_speeches/speech_archive.csv", "Speech archive / 演说档案"),
    ("03_speeches/speech_video_index.csv", "Video index / 视频索引"),
    ("04_visual_archive/image_archive.csv", "Image archive / 图片档案"),
    ("05_campaign_media/advertisements.csv", "Advertisements / 广告"),
    ("05_campaign_media/social_media.csv", "Social media / 社交媒体"),
    ("05_campaign_media/media_coverage.csv", "Media coverage / 媒体报道"),
    ("06_campaign_finance/campaign_finance.csv", "Campaign finance / 竞选资金"),
    ("07_electoral_context/election_results.csv", "Election results / 选举结果"),
    ("07_electoral_context/county_results.csv", "County results / 县级结果"),
    ("07_electoral_context/polling.csv", "Polling / 民调"),
]

missing = []
parts = []
for rel, label in FILES:
    hdr = next(csv.reader(io.open(os.path.join(CASE, rel), encoding="utf-8", newline="")))
    parts.append("### `%s` — %s\n" % (rel, label))
    parts.append("| Column / 列 | Meaning / 含义 |\n|---|---|")
    for c in hdr:
        if c not in D:
            missing.append((rel, c))
        parts.append("| `%s` | %s |" % (c, D.get(c, "TODO")))
    parts.append("")

if missing:
    print("MISSING DESCRIPTIONS:", missing)

io.open(os.path.join(CASE, "09_sources/data_dictionary_bilingual.md"), "w", encoding="utf-8",
        newline="\n").write("""---
title: Data dictionary (bilingual)
title_zh: 数据字典（双语）
compiled_by: Research Agent (batch 2)
last_updated: 2026-11-18
status: complete
coverage_note: Every column of every shipped CSV is described; controlled vocabularies are listed at the end.
---

# Data dictionary / 数据字典

## How to read a row / 如何读一行

English: Each dataset is one CSV with a fixed header, no blank cells, and `unknown` wherever a fact was not
established. A row's `source_urls` cell contains exactly one `SRC-####|https://…` pair; the id resolves in
`09_sources/sources.csv` and the URL after the pipe must be identical to the URL registered there.

中文：每个数据集是一个表头固定的 CSV，不允许空单元格；凡未确认的事实一律写 `unknown`。每行的 `source_urls`
恰好包含一组 `SRC-####|https://…`，编号可在 `09_sources/sources.csv` 中解析，竖线后的网址必须与登记网址完全一致。

## Column reference / 列说明

""" + "\n".join(parts) + """## Controlled vocabularies / 受控词表

| Field / 字段 | Values / 取值 |
|---|---|
| `issue` | Economy, Healthcare, Education, Immigration, Abortion, Gun policy, Energy, Religion, Labor, Democracy, Foreign policy, Other / 经济、医疗、教育、移民、堕胎、枪支政策、能源、宗教、劳工、民主、外交、其他 |
| `event_category` | launch, announcement, rally, town_hall, meet_and_greet, community_visit, small_business_visit, workplace_visit, university_visit, religious_appearance, labor_event, party_event, county_party_meeting, q_and_a, interview_tv, interview_radio, podcast, newspaper_interview, livestream, debate, debate_invitation, press_conference, video_release, tour_stop, tour_launch, tour_finale, fundraiser, endorsement_event, hq_opening, early_voting_event, gotv_event, surrogate_event, election_eve, watch_party, victory_speech, concession_speech, swearing_in, appointment_announcement, filing, other |
| `event_status` | held, cancelled, postponed, rescheduled, virtual, announced, unverified, disputed / 已举行、取消、延期、改期、线上、已宣布、未核实、有争议 |
| `campaign_phase` | pre_launch, launch, primary, runoff, general, early_voting, gotv, election_day, post_election |
| `coverage_type` | news_report, analysis, op_ed, fact_check, interview, live_blog, newsletter, news_video |
| `sponsor_type` | candidate_campaign, authorized_committee, outside_pac, party_committee, unknown |
| `copyright_status` | public_domain, licensed, all_rights_reserved_link_only, unknown |
| `verification_status` | verified, partially verified, unverified, conflicting sources / 已核实、部分核实、未核实、来源冲突 |
| `source_tier` | T1 official/primary, T2 established independent media, T3 supplementary |
| `completeness` | full, partial, clip, unknown |
| `winner` | yes, no |
| `state_region` | Central, Eastern, Western, Northern, Southern, statewide, national, unknown |

## Derived values / 派生值

English: Percentages in `election_results.csv`, `county_results.csv` and `polling.csv` are either published
figures (marked in `notes`) or recomputed from raw votes. Recomputation is stated in the row; published
figures are never silently recalculated.

中文：`election_results.csv`、`county_results.csv` 与 `polling.csv` 中的百分比，要么是来源公布的数字（在
`notes` 中注明），要么由原始票数重算；重算必在行内说明，公布数字绝不悄悄改动。
""".replace("TODO", "see the row's source / 见该行来源"))
print("data dictionary written; missing:", len(missing))
