# meeting-notes-lite

零依赖的**会议纪要提取器**：把一段会议记录 / 速记文本，自动拆解为「议题 / 决议 / 行动项」三块，并用正则识别行动项里的负责人和期限，最后输出 Markdown 表格。无需任何 API。

## 功能简介

- **议题**：识别「议题：/ 讨论：」开头的行。
- **决议**：抓取含「决定 / 达成一致 / 确定 / 通过 / 结论」的行。
- **行动项**：识别「待办 / 任务 / action item / TODO」行，并抽取负责人（中文姓名或 @handle）与期限（周X / 日期 / EOD / by ...）。
- 输出带表格的 Markdown 纪要。

## 快速开始

```bash
python3 cli.py --file meeting.txt

python3 cli.py --text "议题：发布节奏。决定：改为双周发版。任务：张三负责整理文档，周五前完成。"
```

## 无 API key 如何运行

本项目**完全不需要 API key**，纯本地规则提取。

## 目录说明

```
meeting-notes-lite/
├── meeting_notes.py   # 议题/决议/行动项识别 + Markdown 渲染
├── cli.py           # 命令行入口
├── tests/
│   └── test_notes.py
├── README.md
├── LICENSE
└── .gitignore
```

## 运行测试

```bash
python3 -m unittest discover -s tests
```

## License

MIT License，Copyright (c) 2026 ljiang9。
