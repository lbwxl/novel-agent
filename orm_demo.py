from sqlalchemy_demo import get_chapter


class Chapter:
    def __init__(self, chapter: int, title: str, content: str):
        self.chapter = chapter
        self.title = title
        self.content = content


if __name__ == "__main__":
    record = get_chapter(1)

    if record is None:
        print("第 1 章不存在")
    else:
        chapter = Chapter(
            record["chapter"],
            record["title"],
            record["content"],
        )

        print(chapter.chapter)
        print(chapter.title)
        print(chapter.content)
