# Demo Steps README Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a concise, reliable demo script section to README that shows how to run and verify the system locally.

**Architecture:** Update README only; add a focused demo checklist with Docker Compose and curl commands. Tests validate presence of the demo section.

**Tech Stack:** Markdown, pytest.

---

### Task 1: README demo section

**Files:**
- Modify: `README.md`
- Create: `tests/test_readme_demo.py`

**Step 1: Write the failing test**

Create `tests/test_readme_demo.py`:

```python
from pathlib import Path


def test_readme_has_demo_section():
    text = Path(__file__).resolve().parents[1] / "README.md"
    content = text.read_text()
    assert "## Demo Steps" in content
    assert "docker compose up" in content
    assert "curl" in content
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_readme_demo.py::test_readme_has_demo_section -v`
Expected: FAIL (section missing)

**Step 3: Write minimal implementation**

Update `README.md` with a new section:

- Heading: `## Demo Steps`
- Command: `docker compose up --build`
- Health checks (curl for ports 8000-8002)
- Optional websocket note

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_readme_demo.py::test_readme_has_demo_section -v`
Expected: PASS

**Step 5: Commit**

```bash
git add README.md tests/test_readme_demo.py
git commit -m "docs: add demo steps"
```

---

### Task 2: Full test run

**Files:**
- None

**Step 1: Run full test suite**

Run: `pytest`
Expected: PASS

