# CLAUDE.md — Penny by Next Venture

This file is for Claude Code. Read it at the start of every session.

---

## What Penny is

Penny is an open-source, offline-first investment education CLI.
It teaches investing in plain English — so simple a 10-year-old can understand it.

Users run `penny` in their terminal and get:
- 11 structured lessons (markets, compound interest, ETFs, crypto, angel/VC/PE, Canadian tax)
- A paper trading simulator (fake money, real historical prices via yfinance)
- Quizzes after each lesson
- An AI tutor powered by Claude (optional, requires ANTHROPIC_API_KEY)
- Financial calculators (compound growth, DCA, TFSA, position sizing)

## What Penny is NOT

- Not a financial advisor. Never give specific buy/sell advice.
- Not a trading platform. No real money, no brokerage connections.
- Not a data-collection tool. Zero analytics, zero telemetry.
- Not a cloud app. Fully offline by default. AI is opt-in.

---

## Security rules — non-negotiable

1. **No secrets in source.** No API keys anywhere. Not in comments. Not as defaults.
2. **No `.env` committed.** Only `.env.example` with placeholders.
3. **All secrets via `os.environ.get()`** — never `os.environ["KEY"]`.
4. **Graceful degradation.** Every feature works without ANTHROPIC_API_KEY.
   The AI tutor shows: `"AI tutor unavailable — set ANTHROPIC_API_KEY to enable."`
5. **No arbitrary code execution from lesson files.**
   Never `eval()`, `exec()`, or `subprocess` anything from YAML content.
6. **Validate all external inputs** with pydantic before use.
7. **Pin all dependencies** to minor versions in pyproject.toml.
8. **No telemetry.** Zero tracking of any kind.

---

## Writing style — the core rule

Every word must be readable by a 10-year-old with no money knowledge.

- Short sentences. One idea each.
- No jargon without an instant plain-English translation in the same sentence.
- Use analogies first, then the real term.
- Active voice always.
- Use real numbers and examples, not abstract descriptions.
- Write like a friendly teacher, not a textbook.

See the word replacement table in the prompt for banned → preferred substitutions.

---

## How to add a new lesson

1. Create `penny/lessons/content/NN-your-lesson-name.yaml`
2. Follow this exact structure:

```yaml
# Penny by Next Venture — nextventure.io/penny
# Licensed under CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/
# If you use or adapt this lesson, credit Penny by Next Venture and share alike.

id: "NN-your-lesson-name"
title: "Your lesson title"
description: "One sentence description."
estimated_minutes: 10
tags: ["tag1", "tag2"]

steps:
  - type: concept       # or text, example, callout, calculator
    content: |
      Your content here.

quiz:
  - question: "Your question?"
    options:
      - "Option A"
      - "Option B"
      - "Option C"
      - "Option D"
    correct: 0          # 0-indexed
    explanation: "Why this answer is correct."
```

3. Valid `type` values: `text`, `concept`, `example`, `callout`, `calculator`
4. `calculator` type also needs: `calculator: "compound"` (or `dca`, `tfsa`, `position_size`)
5. Run `pytest tests/test_lessons.py` — it validates all lessons automatically.
6. Every lesson must have exactly 4 options per quiz question. `correct` is 0-indexed.

---

## How to add a new calculator

1. Create `penny/calculators/your_calc.py`
2. Return a frozen dataclass result
3. Pure functions only — no side effects, no API calls, no I/O
4. Add 100% test coverage in `tests/test_calculators.py`

Example structure:
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class YourResult:
    result_field: float

def calculate_your_thing(input_a: float, input_b: float) -> YourResult:
    ...
    return YourResult(result_field=round(value, 2))
```

---

## How to add a new Textual screen

1. Create `penny/ui/screens/your_screen.py`
2. Subclass `textual.screen.Screen`
3. Implement `compose()` returning widgets
4. Add BINDINGS for keyboard nav (escape to go back, q to quit)
5. Register in `penny/ui/app.py` SCREENS dict

```python
from textual.screen import Screen
from textual.app import ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Static

class YourScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("q", "app.quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Static("Your content here")
        yield Footer()
```

---

## Config — how it works

All config lives in `penny/config.py`.
It reads environment variables via `os.environ.get()`.
Never read env vars directly outside of `config.py`.
Import the module-level singleton: `from penny.config import config`

To add a new config value:
1. Add field to `Config` dataclass
2. Read it in `Config.from_env()` using `os.environ.get("KEY_NAME", "default")`
3. Never use `os.environ["KEY_NAME"]` — it raises on missing keys

---

## Commands

```bash
# Install for development
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Lint
ruff check penny/ tests/
ruff format --check penny/ tests/

# Run the app
penny

# Run a specific lesson
penny learn 01-how-markets-work

# Open AI tutor
export ANTHROPIC_API_KEY="your-key"
penny tutor
```

---

## Known constraints

- No external network calls at startup. App must launch instantly without network.
- yfinance data is cached locally after first fetch — app works offline after that.
- The AI tutor is the ONLY feature that requires a network call (and it's optional).
- Lesson YAML files are never eval'd or exec'd — treat all content as untrusted.
- SQLite progress DB lives at `~/.penny/progress.db` by default.

---

## AI tutor system prompt

The system prompt is in `penny/tutor/claude_tutor.py` → `SYSTEM_PROMPT`.

Do NOT change this prompt without review. Key rules it enforces:
- Plain English only — no jargon without explanation
- Canadian context (TFSA, RRSP, CAD)
- No specific buy/sell recommendations
- No personalized financial advice
- Redirect off-topic questions back to investing education
- Max 150 words per response (CLI constraint)

---

## Tech stack

| Purpose         | Library          |
|-----------------|------------------|
| CLI             | typer            |
| Terminal UI     | textual          |
| Formatting      | rich             |
| AI tutor        | anthropic        |
| Market data     | yfinance         |
| Data            | pandas           |
| Validation      | pydantic         |
| YAML parsing    | pyyaml           |
| HTTP            | httpx            |
| Local storage   | sqlite3 (stdlib) |
| Testing         | pytest           |
| Linting         | ruff             |

Do not add libraries without a clear justification in code comments
explaining why the existing stack is insufficient.
