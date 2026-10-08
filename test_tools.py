from tools import read_chapter,write_chapter


def test_read_chapter_rejects_zero():
  result = read_chapter.invoke({"chapter": 0})

  assert result == "章节号必须大于等于1"

def test_write_chapter_does_not_overwrite(tmp_path, monkeypatch):
  monkeypatch.chdir(tmp_path)

  chapters_dir = tmp_path / "novel" / "chapters"
  chapters_dir.mkdir(parents=True)

  chapter_path = chapters_dir / "001.md"
  chapter_path.write_text("原正文", encoding="utf-8")


  # 接下来由你调用工具，并检查结果

  result = write_chapter.invoke({"chapter": 1, "content": "新正文"})
  assert result == "第 1 章已经存在，为防止覆盖，本次没有保存。"
  assert chapter_path.read_text(encoding="utf-8") == "原正文"
