import json
from pathlib import Path
from langchain_core.tools import tool

@tool
def read_world():
    """读取小说世界观设定。"""
    return Path("novel/world.md").read_text(
        encoding="utf-8"
    )

@tool
def read_characters():
    """读取小说人物设定"""
    return Path("novel/characters.md").read_text(
        encoding="utf-8"
    )

@tool
def read_outline():
    """读取小说整体大纲"""
    return Path("novel/outline.md").read_text(
        encoding="utf-8"
    )

@tool
def read_chapter(chapter: int) -> str:
    """读取指定章节的小说正文。chapter是需要读取的章节号。"""
    if chapter < 1:
        return "章节号必须大于等于1"

    file_path = Path("novel/chapters") / f"{chapter:03d}.md"

    if not file_path.exists():
        return f"第{chapter}章不存在"
    return file_path.read_text(
        encoding="utf-8"
    )

@tool
def get_novel_state() -> str:
    """读取小说当前进度，包括当前章节、当前卷、主角和当前位置。"""

    file_path = Path("novel/state.json")

    content = file_path.read_text(
        encoding="utf-8"
    )

    return json.dumps(
        json.loads(content),
        ensure_ascii=False,
        indent=2,
    )

tools = [
    read_world,
    read_characters,
    read_outline,
    read_chapter,
    get_novel_state
]
