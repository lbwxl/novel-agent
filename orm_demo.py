from sqlalchemy_demo import get_chapter
from sqlalchemy import Integer, Text
from sqlalchemy.orm import DeclarativeBase, mapped_column

# class Chapter:
#     def __init__(self, chapter: int, title: str, content: str):
#         self.chapter = chapter
#         self.title = title
#         self.content = content
class Base(DeclarativeBase):
  pass


class Chapter(Base):
  __tablename__ = "chapters"

  chapter = mapped_column(Integer, primary_key=True)
  title = mapped_column(Text)
  content = mapped_column(Text)


if __name__ == "__main__":
    record = get_chapter(1)

    if record is None:
        print("第 1 章不存在")
    else:
        chapter = Chapter(
          chapter=record["chapter"],
          title=record["title"],
          content=record["content"],
        )

        print(chapter.chapter)
        print(chapter.title)
        print(chapter.content)
