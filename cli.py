"""meeting-notes-lite 命令行入口。

用法示例：
    python3 cli.py --file meeting.txt
    python3 cli.py --text "议题：发布节奏。决定：改为双周发版。任务：张三负责整理文档，周五前完成。"
"""

from __future__ import annotations

import argparse
import sys

from meeting_notes import extract, render_markdown


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="meeting-notes-lite",
        description="从会议文本提取议题、决议、行动项",
    )
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="直接传入会议文本")
    src.add_argument("--file", help="从文本文件读取")
    p.add_argument("--title", default="会议纪要", help="纪要标题")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    text = args.text if args.text else open(args.file, encoding="utf-8").read()
    result = extract(text)
    print(render_markdown(result, title=args.title))
    return 0


if __name__ == "__main__":
    sys.exit(main())
