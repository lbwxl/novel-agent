from pathlib import Path
from langchain_core.output_parsers import StrOutputParser
from model import model

chapter = 4

chapter_path = Path("novel/chapters") / f"{chapter:03d}.md"
content = chapter_path.read_text(encoding="utf-8")

prompt = f"""
请提取下面章节的摘要，供后续小说创作使用。

总长度约 150 字，按四项输出，每项一句：
1. 关键事件
2. 人物状态与变化
3. 未解决的问题或伏笔
4. 结尾场景与下一步安排

只保留正文支持的信息。
保持原文的不确定性、程度和时间范围，不补充猜测。
合并重复信息，优先保留影响后续剧情的内容。

章节正文：
{content}
"""

chain = model | StrOutputParser()
summary = chain.invoke(prompt)

print(summary)

summariesDir = Path("novel/summaries")
summariesChapter = summariesDir / f"{chapter:03d}.md"
summariesDir.mkdir(parents=True, exist_ok=True)
summariesChapter.write_text(summary, encoding="utf-8")
