# penny — investment education for everyone

**Every great investor started with their first penny.**

Penny is a free, open-source investment education tool that runs in your terminal.
Plain English. No jargon. No account required.

```
pipx install penny-learn
penny
```

---

## What you get

```
╭─────────────────────────────────────────╮
│  penny  — learn to invest               │
│  Every great investor started here.     │
╰─────────────────────────────────────────╯

  [L]  lessons        11 modules — start anywhere
  [S]  simulator      paper trade with real history
  [C]  calculators    compound growth, DCA, TFSA
  [T]  AI tutor       ask anything about investing
       (set ANTHROPIC_API_KEY to enable)

  [Q]  quit
```

---

## Install

```bash
pipx install penny-learn
```

Or with pip:

```bash
pip install penny-learn
```

---

## Lessons

| # | Lesson | Time |
|---|--------|------|
| 01 | How markets work — the basics | 10 min |
| 02 | Compound interest — the 8th wonder | 12 min |
| 03 | Dollar-cost averaging — invest a little, every time | 10 min |
| 04 | ETFs and index funds — the lazy genius move | 12 min |
| 05 | Picking stocks — what to look for | 15 min |
| 06 | Risk and spreading your money around | 10 min |
| 07 | Canadian taxes — TFSA, RRSP, and free money | 18 min |
| 08 | Crypto basics — what it is, and what it isn't | 14 min |
| 09 | Angel investing — betting on people with big dreams | 15 min |
| 10 | Venture capital — a fund that bets on the future | 18 min |
| 11 | Private equity — buying whole companies to make them better | 16 min |

---

## Enable the AI tutor

The AI tutor is powered by Claude. To enable it:

```bash
export ANTHROPIC_API_KEY="your-key-here"
penny
```

Your key never touches disk. Nothing is logged. Nothing is tracked.

The rest of the app — lessons, simulator, calculators, quizzes — works fully offline without any key.

**Never put your key in a file that could be committed to git.**

---

## Features

- **11 lessons** covering everything from market basics to venture capital
- **Paper trading simulator** — $10,000 virtual money, real historical prices
- **Financial calculators** — compound growth, dollar-cost averaging, TFSA, position sizing
- **Quiz after every lesson** with instant feedback
- **AI tutor** powered by Claude (optional)
- **Fully offline** — no account, no sign-up, no data sent anywhere by default
- **Canadian-first** — TFSA, RRSP, TSX, and Canadian tax context throughout

---

## Development

```bash
git clone https://github.com/Next-Venture-Inc/Penny
cd Penny/projects/penny
pip install -e ".[dev]"
pytest tests/ -v
ruff check penny/ tests/
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add lessons, calculators, and more.

---

## License

Code: [Apache 2.0](LICENSE)
Lesson content: [CC BY-SA 4.0](LICENSE-CONTENT)

Built by [Next Venture](https://nextventure.io) — nextventure.io/penny
