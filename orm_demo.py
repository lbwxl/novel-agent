
from sqlalchemy_demo import engine
from sqlalchemy import Integer, Text
from sqlalchemy.orm import DeclarativeBase, mapped_column, Session

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
  with Session(engine) as session:
    chapter = session.get(Chapter, 1)

    if chapter is None:
      print("第 1 章不存在")
    else:
      print(type(chapter))
      print(chapter.chapter)
      print(chapter.title)
      print(chapter.content)

    print(session.get(Chapter, 2))
