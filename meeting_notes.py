"""meeting-notes-lite：从会议文本提取议题、决议、行动项。

规则：
- 议题：以「议题/讨论/topic」开头或形如小标题的行；
- 决议：含「决定/决议/达成一致/确定/通过/结论」等关键词的行；
- 行动项：含「待办/任务/action/TODO/负责」等标记的行，并尝试识别
  负责人（姓名 / @handle）与期限（日期 / 周X / EOD / by ...）。
"""

from __future__ import annotations

import re

TOPIC_MARKERS = re.compile(r"^\s*(?:议题|讨论|主题|topic|agenda)\s*[:：]")
DECISION_MARKERS = re.compile(r"(决定|决议|达成一致|确定|通过|结论是|一致认为)")
ACTION_MARKERS = re.compile(r"(待办|行动项|任务|action\s*item|todo|负责|跟进|owner)")

OWNER_RE = re.compile(
    r"(?:负责(?:人)?[:：]?\s*)?"
    r"(@[A-Za-z0-9_]+|[\u4e00-\u9fa5]{2,4}(?=\s*(?:负责|来做|跟进|处理|完成)))")
DEADLINE_RE = re.compile(
    r"(?:(?:截止|于|在|before|by)\s*)?"
    r"((?:下?周[一二三四五六日天])|(?:周[一二三四五六日天])|"
    r"\d{1,2}[-/月]\d{1,2}[日号]?(?:前|之前)?|"
    r"\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日号]?|"
    r"EOD|COB|月底|本周内)")


def extract(text: str) -> dict:
    """提取会议纪要结构化结果。"""
    topics: list[str] = []
    decisions: list[str] = []
    actions: list[dict] = []

    for raw in text.splitlines():
        line = raw.strip().lstrip("-•*0123456789.、 ")
        if not line:
            continue

        if TOPIC_MARKERS.match(raw):
            topics.append(re.sub(TOPIC_MARKERS, "", line).strip())
            continue

        if DECISION_MARKERS.search(line):
            decisions.append(line)
            continue

        if ACTION_MARKERS.search(line):
            owner = ""
            m = OWNER_RE.search(line)
            if m:
                owner = m.group(1)
            deadline = ""
            d = DEADLINE_RE.search(line)
            if d:
                deadline = d.group(1)
            actions.append({"task": line, "owner": owner, "deadline": deadline})

    return {"topics": topics, "decisions": decisions, "action_items": actions}


def render_markdown(result: dict, title: str = "会议纪要") -> str:
    """把结构化结果渲染成 Markdown 纪要。"""
    out = [f"# {title}", ""]

    out.append("## 议题")
    out.append("")
    if result["topics"]:
        for t in result["topics"]:
            out.append(f"- {t}")
    else:
        out.append("- （无）")
    out.append("")

    out.append("## 决议")
    out.append("")
    if result["decisions"]:
        for d in result["decisions"]:
            out.append(f"- {d}")
    else:
        out.append("- （无）")
    out.append("")

    out.append("## 行动项")
    out.append("")
    if result["action_items"]:
        out.append("| 任务 | 负责人 | 期限 |")
        out.append("| --- | --- | --- |")
        for a in result["action_items"]:
            out.append(f"| {a['task']} | {a['owner'] or '未指定'} | "
                       f"{a['deadline'] or '未指定'} |")
    else:
        out.append("- （无）")
    out.append("")
    return "\n".join(out)
