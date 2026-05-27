from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

from penny.config import config

BANNER = """\
╭─────────────────────────────────────────╮
│  penny  — learn to invest               │
│  Every great investor started here.     │
╰─────────────────────────────────────────╯"""

MENU = """\
  [L]  lessons        11 modules — start anywhere
  [S]  simulator      paper trade with real history
  [C]  calculators    compound growth, DCA, TFSA
  [T]  AI tutor       ask anything about investing
       {tutor_note}

  [Q]  quit"""


class HomeScreen(Screen):
    BINDINGS = [
        Binding("l", "open_lessons", "Lessons"),
        Binding("s", "open_simulator", "Simulator"),
        Binding("c", "open_calculators", "Calculators"),
        Binding("t", "open_tutor", "Tutor"),
        Binding("q", "app.quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        tutor_note = (
            "(AI tutor ready)"
            if config.ai_enabled
            else "(set ANTHROPIC_API_KEY to enable)"
        )
        menu = MENU.format(tutor_note=tutor_note)
        yield Static(BANNER, id="banner")
        yield Static(menu, id="menu")
        yield Footer()

    def action_open_lessons(self) -> None:
        from penny.ui.screens.lesson import LessonScreen
        self.app.push_screen(LessonScreen())

    def action_open_simulator(self) -> None:
        from penny.ui.screens.simulator import SimulatorScreen
        self.app.push_screen(SimulatorScreen())

    def action_open_calculators(self) -> None:
        from penny.ui.screens.calculator import CalculatorScreen
        self.app.push_screen(CalculatorScreen())

    def action_open_tutor(self) -> None:
        from penny.ui.screens.tutor import TutorScreen
        self.app.push_screen(TutorScreen())
