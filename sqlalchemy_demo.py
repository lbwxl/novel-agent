from sqlalchemy import create_engine, text
engine = create_engine("sqlite:///novel/learning.sqlite3")

def get_chapter(chapter: int):
  with engine.connect() as connection:
    result = connection.execute(
      text(
        "SELECT chapter, title, content "
        "FROM chapters WHERE chapter = :chapter"
      ),
      {"chapter": chapter},
    )

    row = result.mappings().fetchone()

    if row is None:
      return None

    return dict(row)


if __name__ == "__main__":
    print(get_chapter(1))
    print(get_chapter(2))
