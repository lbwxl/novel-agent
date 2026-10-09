import json
from pathlib import Path
from langchain_core.tools import tool
from langchain_core.output_parsers import StrOutputParser
from model import model

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

    try:
        file_path = Path("novel/state.json")

        content = file_path.read_text(
          encoding="utf-8"
        )

        state = json.loads(content)
        if type(state) != dict:
          return f"state 类型必须为dict，state={state}"

        chapter = state.get("current_chapter")

        if type(chapter) != int:
            return f"current_chapter类型必须为 int"

        if chapter < 0:
            return f"current_chapter 不能小于 0"

        return json.dumps(
          state,
          ensure_ascii=False,
          indent=2,
        )
    except OSError as error:
        return f"小说进度获取失败 {error}"
    except json.decoder.JSONDecodeError as error:
        return f"JSON处理失败 {error}"

@tool
def write_chapter(chapter: int, content: str) -> str:
    """保存指定章节的小说正文。chapter是章节号，content是完整的章节正文。"""

    chapters_dir = Path("novel/chapters")

    if chapter < 1:
        return f"章节号必须大于等于 1，当前是 {chapter}"

    if content.strip() == "":
        return f"第 {chapter} 章正文不能为空"

    try:
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
    except OSError as error:
        return f"第 {chapter} 章保存失败：{error}。请勿更新小说进度。"

@tool
def update_novel_state(
    current_chapter: int,
    location: str,
) -> str:
    """更新小说当前进度。章节保存成功后使用；目标章节文件不存在时拒绝更新。"""
    try:
        chapter_path = Path("novel/chapters") / f"{current_chapter:03d}.md"

        if not chapter_path.is_file():
          return f"第 {current_chapter} 章文件不存在，本次没有更新小说进度。"

        file_path = Path("novel/state.json")
        temp_path = Path("novel/state.json.tmp")

        content = file_path.read_text(
          encoding="utf-8"
        )

        state = json.loads(content)
        expected_chapter = state["current_chapter"] + 1
        if expected_chapter != current_chapter:
          return f"下一章节应该是第 {expected_chapter} 章，当前要更新的章节是第 {current_chapter} 章，不符合逐章续写"

        state["current_chapter"] = current_chapter
        state["location"] = location

        temp_path.write_text(
          json.dumps(
            state,
            ensure_ascii=False,
            indent=2,
          ),
          encoding="utf-8",
        )
        temp_path.replace(file_path)
    except OSError as error:
        return f"小说状态更新失败，详见 {error}"
    except json.decoder.JSONDecodeError as error:
        return f"小说状态文件 JSON 格式错误 {error}"

    return f"小说进度已更新到第 {current_chapter} 章"

@tool
def read_chapter_summary(chapter: int) -> str:
    """读取指定章节的摘要，用于快速回顾历史事件、人物变化和伏笔。
    chapter 是章节号。摘要省略了细节，需要精确信息时使用 read_chapter。
    """
    # 在这里读取摘要文件并返回内容
    file_path = Path("novel/summaries") / f"{chapter:03d}.md"
    if not file_path.exists():
        return "文件不存在"
    result = file_path.read_text(encoding="utf-8")
    if result.strip() == "":
        return "文件内容为空"
    else:
        return result

@tool
def generate_chapter_summary(chapter: int) -> str:
    """根据已保存的章节正文生成并保存摘要。章节保存成功以后使用。"""
    chapter_path = Path("novel/chapters") / f"{chapter:03d}.md"

    if not chapter_path.is_file():
        return f"第 {chapter} 章正文不存在，无法生成摘要。"

    summary_path = Path("novel/summaries") / f"{chapter:03d}.md"

    if summary_path.exists():
        return f"第 {chapter} 章摘要已存在，本次没有重新生成。"

    content = chapter_path.read_text(encoding="utf-8")

    prompt = f"""
      请为下面的小说章节生成约 150 字的摘要，按四项输出：
      1. 关键事件
      2. 人物状态与变化
      3. 未解决的问题或伏笔
      4. 结尾场景与下一步安排

      只保留正文支持的信息，保持原文的不确定性，不补充猜测。
      优先保留明确的修炼境界、能力变化和人物目标。

      章节正文：
      {content}
    """

    chain = model | StrOutputParser()
    summary = chain.invoke(prompt)

    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(summary, encoding="utf-8")

    return f"第 {chapter} 章摘要已保存：{summary_path}"


tools = [
    read_world,
    read_characters,
    read_outline,
    read_chapter,
    get_novel_state,
    write_chapter,
    update_novel_state,
    read_chapter_summary,
    generate_chapter_summary
]
