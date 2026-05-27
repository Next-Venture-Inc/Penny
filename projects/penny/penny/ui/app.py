from textual.app import App, ComposeResult
from textual.binding import Binding

from penny.ui.screens.home import HomeScreen
from penny.ui.screens.lesson import LessonScreen
from penny.ui.screens.quiz import QuizScreen
from penny.ui.screens.tutor import TutorScreen
from penny.ui.screens.calculator import CalculatorScreen
from penny.ui.screens.simulator import SimulatorScreen


class PennyApp(App):
    """Penny by Next Venture — investment education for everyone."""

    CSS = """
    Screen {
        background: $surface;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("l", "push_screen('lessons')", "Lessons"),
        Binding("s", "push_screen('simulator')", "Simulator"),
        Binding("c", "push_screen('calculators')", "Calculators"),
        Binding("t", "push_screen('tutor')", "Tutor"),
    ]

    SCREENS = {
        "home": HomeScreen,
        "lessons": LessonScreen,
        "quiz": QuizScreen,
        "tutor": TutorScreen,
        "calculators": CalculatorScreen,
        "simulator": SimulatorScreen,
    }

    def __init__(
        self,
        start_screen: str = "home",
        lesson_id: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._start_screen = start_screen
        self._lesson_id = lesson_id

    def on_mount(self) -> None:
        if self._start_screen == "home":
            self.push_screen(HomeScreen())
        elif self._start_screen == "lessons":
            self.push_screen(LessonScreen(lesson_id=self._lesson_id))
        elif self._start_screen == "quiz":
            self.push_screen(QuizScreen(lesson_id=self._lesson_id))
        elif self._start_screen == "tutor":
            self.push_screen(TutorScreen())
        elif self._start_screen == "calculators":
            self.push_screen(CalculatorScreen())
        elif self._start_screen == "simulator":
            self.push_screen(SimulatorScreen())
        else:
            self.push_screen(HomeScreen())
