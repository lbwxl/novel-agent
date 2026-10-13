from sqlalchemy import create_engine, text


engine = create_engine("sqlite:///novel/learning.sqlite3")


if __name__ == "__main__":
    connection = engine.connect()

    try:
        result = connection.execute(
            text(
                "SELECT chapter, title, content "
                "FROM chapters WHERE chapter = 1"
            )
        )

        row = result.fetchone()

        print(row)
    finally:
        connection.close()
