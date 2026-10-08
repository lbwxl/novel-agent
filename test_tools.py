from tools import read_chapter


def test_read_chapter_rejects_zero():
  result = read_chapter.invoke({"chapter": 0})

  assert result == "章节号必须大于等于1"
