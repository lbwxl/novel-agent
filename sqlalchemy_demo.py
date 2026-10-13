from sqlalchemy import create_engine, text


engine = create_engine("sqlite:///novel/learning.sqlite3")


if __name__ == "__main__":

    with  engine.connect() as connection:
      result = connection.execute(
        text(
          "SELECT chapter, title, content "
          "FROM chapters WHERE chapter = 1"
        )
      )

      row = result.fetchone()

      print(row)
