import unittest

from meeting_notes import extract, render_markdown


SAMPLE = """
议题：下季度发布节奏
讨论：资源排期

大家一致认为应该改为双周发版。
决定：从下月起双周发版。
结论是灰度比例调到 20%。

待办：张三负责整理发布文档，周五前完成。
任务：李四跟进监控看板，10-15 前上线。
行动项：@bob 负责准备回滚预案，by EOD。
"""


class TestExtract(unittest.TestCase):
    def setUp(self):
        self.r = extract(SAMPLE)

    def test_topics(self):
        self.assertIn("下季度发布节奏", self.r["topics"])

    def test_decisions(self):
        self.assertTrue(any("双周发版" in d for d in self.r["decisions"]))

    def test_action_items_count(self):
        self.assertGreaterEqual(len(self.r["action_items"]), 3)

    def test_owner_recognized(self):
        owners = [a["owner"] for a in self.r["action_items"]]
        self.assertIn("张三", owners)
        self.assertIn("@bob", owners)

    def test_deadline_recognized(self):
        deadlines = [a["deadline"] for a in self.r["action_items"]]
        self.assertTrue(any("周五" in d for d in deadlines))
        self.assertTrue(any("10-15" in d for d in deadlines))
        self.assertTrue(any("EOD" in d for d in deadlines))

    def test_empty(self):
        r = extract("")
        self.assertEqual(r["topics"], [])
        self.assertEqual(r["action_items"], [])


class TestRender(unittest.TestCase):
    def test_markdown(self):
        md = render_markdown(extract(SAMPLE))
        self.assertIn("# 会议纪要", md)
        self.assertIn("## 行动项", md)
        self.assertIn("| 任务 | 负责人 | 期限 |", md)


if __name__ == "__main__":
    unittest.main()
