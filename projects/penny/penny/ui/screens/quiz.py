from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Button, Footer, Markdown, Static

from penny.lessons.loader import load_lesson, load_all_lessons, LessonParseError
from penny.quiz.engine import QuizEngine


class QuizScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("q", "app.quit", "Quit"),
    ]

    def __init__(self, lesson_id: str | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self._lesson_id = lesson_id
        self._engine: QuizEngine | None = None
        self._awaiting_continue = False

    def on_mount(self) -> None:
        if not self._lesson_id:
            lessons = load_all_lessons()
            if lessons:
                self._lesson_id = lessons[0].id
        if self._lesson_id:
            try:
                lesson = load_lesson(self._lesson_id)
                self._engine = QuizEngine(lesson)
                self._render_question()
            except LessonParseError as exc:
                self.query_one("#question", Markdown).update(f"Error: {exc}")

    def compose(self) -> ComposeResult:
        yield Static("", id="progress")
        yield Markdown("", id="question")
        yield Button("A", id="btn-0", variant="default")
        yield Button("B", id="btn-1", variant="default")
        yield Button("C", id="btn-2", variant="default")
        yield Button("D", id="btn-3", variant="default")
        yield Static("", id="feedback")
        yield Footer()

    def _render_question(self) -> None:
        if self._engine is None:
            return
        q = self._engine.current_question
        if q is None:
            self.query_one("#question", Markdown).update(
                f"## Quiz done!\n\n{self._engine.summary}"
            )
            return
        idx, total = self._engine.state.current_index + 1, self._engine.state.total_questions
        self.query_one("#progress", Static).update(f"  Question {idx} of {total}")
        self.query_one("#question", Markdown).update(f"**{q.question}**")
        labels = ["A", "B", "C", "D"]
        for i, opt in enumerate(q.options):
            self.query_one(f"#btn-{i}", Button).label = f"{labels[i]}. {opt}"
        self.query_one("#feedback", Static).update("")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if self._engine is None or self._awaiting_continue:
            return
        btn_id = event.button.id
        if not btn_id or not btn_id.startswith("btn-"):
            return
        choice = int(btn_id.split("-")[1])
        is_correct, explanation = self._engine.answer(choice)
        feedback = ("Correct!" if is_correct else "Not quite.") + f"\n\n{explanation}"
        self.query_one("#feedback", Static).update(feedback)
        self._awaiting_continue = True
        if not self._engine.state.complete:
            self.set_timer(2.5, self._next_question)
        else:
            self.set_timer(3.0, self._show_summary)

    def _next_question(self) -> None:
        self._awaiting_continue = False
        self._render_question()

    def _show_summary(self) -> None:
        self._awaiting_continue = False
        self.query_one("#question", Markdown).update(
            f"## All done!\n\n{self._engine.summary}"
        )
