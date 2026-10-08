from tools import read_chapter,write_chapter,update_novel_state
import json


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

def test_state_update_recovers_after_failure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    # 准备尚未完成任何章节的旧状态。
    novel_dir = tmp_path / "novel"
    novel_dir.mkdir()
    state_path = novel_dir / "state.json"
    state_path.write_text(
        json.dumps({"current_chapter": 0, "location": "测试起点"}),
        encoding="utf-8",
    )

    # 先确认第 1 章已经成功保存。
    save_result = write_chapter.invoke({"chapter": 1, "content": "测试正文"})
    assert "保存成功" in save_result
    chapter_path = novel_dir / "chapters" / "001.md"
    assert chapter_path.read_text(encoding="utf-8") == "测试正文"

    # 用同名目录阻止临时文件写入，制造状态更新失败。
    temp_path = novel_dir / "state.json.tmp"
    temp_path.mkdir()
    result = update_novel_state.invoke({
        "current_chapter": 1,
        "location": "测试终点",
    })

    assert "小说状态更新失败" in result
    assert chapter_path.read_text(encoding="utf-8") == "测试正文"

    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state.get("current_chapter") == 0
    assert state.get("location") == "测试起点"

    # 解除故障，只重试状态更新，保留已保存的章节。
    temp_path.rmdir()
    result = update_novel_state.invoke({
        "current_chapter": 1,
        "location": "测试终点",
    })

    assert result == "小说进度已更新到第 1 章"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state.get("current_chapter") == 1
    assert state.get("location") == "测试终点"
    assert chapter_path.read_text(encoding="utf-8") == "测试正文"
    assert not temp_path.exists()
