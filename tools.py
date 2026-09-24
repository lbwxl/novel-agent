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

@tool
def write_chapter(chapter: int, content: str) -> str:
    """保存指定章节的小说正文。chapter是章节号，content是完整的章节正文。"""

    chapters_dir = Path("novel/chapters")

    chapters_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = chapters_dir / f"{chapter:03d}.md"

    if file_path.exists():
        return f"第 {chapter} 章已经存在，为防止覆盖，本次没有保存。"

    file_path.write_text(
        content,
        encoding="utf-8",
    )

    return f"第 {chapter} 章保存成功：{file_path}"

@tool
def update_novel_state(
    current_chapter: int,
    location: str,
) -> str:
    """更新小说当前进度。写完新章节以后使用"""
    file_path = Path("novel/state.json")

    content = file_path.read_text(
        encoding="utf-8"
    )

    state = json.loads(content)
    state["current_chapter"] = current_chapter
    state["location"] = location
    file_path.write_text(
        json.dumps(
            state,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return f"小说进度已更新到第 {current_chapter} 章"

tools = [
    read_world,
    read_characters,
    read_outline,
    read_chapter,
    get_novel_state,
    write_chapter
]
