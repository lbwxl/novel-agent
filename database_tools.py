from langchain_core.tools import tool
from sqlalchemy_demo import get_chapter

@tool
def read_database_chapter(chapter: int) -> str:
  """读取学习数据库中指定章节的正文。chapter 是章节号。"""
  record = get_chapter(chapter)
  if record is None:
    return f"学习数据库中没有第 {chapter} 章。"
  return record["content"]


if __name__ == "__main__":
    print(read_database_chapter.invoke({"chapter": 1}))
    print(read_database_chapter.invoke({"chapter": 2}))
