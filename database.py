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

def update_chapter_title(chapter: int, title: str):
    connection = sqlite3.connect("novel/learning.sqlite3")

    connection.execute(
      "UPDATE chapters SET title = ? WHERE chapter = ?",
      [title, chapter],
    )

    connection.commit()
    connection.close()


def delete_chapter(chapter: int):
  connection = sqlite3.connect("novel/learning.sqlite3")

  connection.execute(
    "DELETE FROM chapters WHERE chapter = ?",
    [chapter],
  )

  connection.commit()
  connection.close()

def rollback_demo():
    connection = sqlite3.connect("novel/learning.sqlite3")
    sql = "INSERT INTO chapters (chapter, title, content) VALUES (?, ?, ?)"

    try:
      connection.execute(sql, [3, "事务练习", "尚未提交的正文"])
      print("第3章插入已执行，尚未提交")

      # 第1章已经存在，故意触发主键冲突。
      connection.execute(sql, [1, "重复章节", "测试正文"])

      connection.commit()
    except sqlite3.IntegrityError:
      connection.rollback()
      print("发生主键冲突，本次事务已回滚")
    finally:
      connection.close()



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

# if __name__ == "__main__":
#     # 准备一条专门用于删除练习的记录。
#     connection = sqlite3.connect("novel/learning.sqlite3")
#     connection.execute(
#         "INSERT INTO chapters (chapter, title, content) VALUES (?, ?, ?)",
#         [2, "测试章节", "这是一条删除练习数据。"],
#     )
#     connection.commit()
#     connection.close()
#
#     print("删除前：", get_chapter(2))
#
#     delete_chapter(2)
#
#     print("删除后：", get_chapter(2))

if __name__ == "__main__":
    print("执行前：", get_chapter(3))
    rollback_demo()
    print("执行后：", get_chapter(3))
