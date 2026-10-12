import sqlite3

def get_chapter(chapter: int):
  connection = sqlite3.connect("novel/learning.sqlite3")

  cursor = connection.execute(
    "SELECT chapter, title, content FROM chapters WHERE chapter = ?",
    [chapter],
  )

  row = cursor.fetchone()
  connection.close()
  return row

# connection = sqlite3.connect("novel/learning.sqlite3")
# print("数据库连接成功")
#
# connection.execute("""
#   CREATE TABLE IF NOT EXISTS chapters (
#     chapter INTEGER PRIMARY KEY,
#     title TEXT,
#     content TEXT
#   )
# """)
# print("章节表已准备好")

# connection.execute(
#   "INSERT INTO chapters (chapter, title, content) VALUES (?, ?, ?)",
#   [1, "青石村", "林深握紧柴刀，走向村口。"]
# )
# connection.commit()
# print("第一章已保存")
# chapter = 2
# cursor = connection.execute(
#   "SELECT chapter, title, content FROM chapters where chapter = ?",
#   [chapter]
# )
# row = cursor.fetchone()
# print(row)
# connection.close()

if __name__ == "__main__":
    print(get_chapter(1))
    print(get_chapter(2))
