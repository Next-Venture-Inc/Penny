# Contributing to Penny

Thanks for wanting to help make investing education better.
Every improvement you make helps someone learn something that can change their financial life.

---

## Set up your dev environment

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/Penny
cd Penny/projects/penny
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# Verify everything works:
pytest tests/ -v
ruff check penny/ tests/
penny  # Should launch the terminal UI
```

---

## How to write a new lesson

Lessons are YAML files in `penny/lessons/content/`.
Name them `NN-short-name.yaml` where NN is the next number in sequence.

Every word must be readable by someone who has never invested before.
If you wouldn't say it to a 16-year-old cousin, rewrite it.

### Required YAML structure

```yaml
# Penny by Next Venture — nextventure.io/penny
# Licensed under CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/
# If you use or adapt this lesson, credit Penny by Next Venture and share alike.

id: "NN-your-lesson-name"         # must match the filename (without .yaml)
title: "Your lesson title"
description: "One-sentence description of what this lesson teaches."
estimated_minutes: 12             # honest estimate
tags: ["tag1", "tag2"]

steps:
  - type: concept                 # concept | text | example | callout | calculator
    content: |
      Your content here.
      Use plain English. Short sentences. Real examples.

  - type: example
    content: |
      A real-world example with actual numbers.

  - type: callout
    content: |
      A key takeaway or important note.

  - type: calculator
    content: "Try it yourself."
    calculator: "compound"        # compound | dca | tfsa | position_size

quiz:
  - question: "Your question?"
    options:
      - "Option A"
      - "Option B"
      - "Option C"
      - "Option D"
    correct: 0                    # 0-indexed (0 = A, 1 = B, 2 = C, 3 = D)
    explanation: "Why this is right, explained simply. What the wrong answers miss."
```

### Writing checklist

- [ ] Every finance term is explained in the same sentence or the very next one
- [ ] All sentences are short (aim for under 20 words)
- [ ] At least one real number or real example in every step
- [ ] No passive voice ("returns are generated" → "your money makes you returns")
- [ ] Canadian context where relevant (TFSA, RRSP, TSX, CAD)
- [ ] Quiz has exactly 4 options per question
- [ ] `correct` is 0-indexed
- [ ] Explanation tells the learner WHY — not just what's right

### Validate your lesson

```bash
pytest tests/test_lessons.py -v
```

This automatically loads and validates all lessons. If yours has a problem, it will tell you exactly what's wrong.

---

## How to add a calculator

1. Create `penny/calculators/your_calc.py`
2. Write a pure function — no side effects, no API calls
3. Return a frozen dataclass
4. Add tests in `tests/test_calculators.py` — cover edge cases
5. Wire it up to a UI button in `penny/ui/screens/calculator.py`

---

## Pull request requirements

Before opening a PR:

- [ ] `pytest tests/ -v` — all tests pass
- [ ] `ruff check penny/ tests/` — no linting errors
- [ ] `ruff format --check penny/ tests/` — code is formatted
- [ ] No API keys, tokens, or secrets anywhere in any file
- [ ] `.env` is not committed (it's in `.gitignore`)
- [ ] New lessons validated by the test suite
- [ ] Writing follows the plain-English style guide

---

## Code of conduct

Be kind. We're all here to learn.

Questions? Open a GitHub issue at https://github.com/Next-Venture-Inc/Penny/issues

---

## License

By contributing, you agree that:
- Your code contributions are licensed under Apache 2.0
- Your lesson content contributions are licensed under CC BY-SA 4.0
