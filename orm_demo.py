
from sqlalchemy_demo import engine
from sqlalchemy import Integer, Text, select
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

def insert_demo():
  with Session(engine) as session:
    existing = session.get(Chapter, 2)
    if existing is not None:
      print("第 2 章已存在，本次不插入")
      return

    chapter = Chapter(
      chapter=2,
      title="ORM 插入练习",
      content="这是一条通过 ORM 保存的学习记录。",
    )
    session.add(chapter)
    session.commit()
    print("第 2 章已提交")

  with Session(engine) as session:
    saved = session.get(Chapter, 2)
    print(saved.title)
    print(saved.content)

if __name__ == "__main__":
  with Session(engine) as session:
    # chapter = session.get(Chapter, 1)
    statement = select(Chapter).where(
      Chapter.title == "青石村之夜"
    )
    chapter = session.scalar(statement)
    if chapter is None:
      print("第 1 章不存在")
    else:
      print(type(chapter))
      print(chapter.chapter)
      print(chapter.title)
      print(chapter.content)

    print(session.get(Chapter, 2))

  insert_demo()
