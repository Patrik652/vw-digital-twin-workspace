from pathlib import Path


def test_todo_has_completed_tasks():
    text = Path(__file__).resolve().parents[1] / "TODO_CODEX.md"
    content = text.read_text()
    assert "[x] Task 2" in content or "[X] Task 2" in content
