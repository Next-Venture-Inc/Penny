from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, ListItem, ListView, Markdown, Static

from penny.lessons.loader import load_all_lessons, load_lesson, LessonParseError
from penny.lessons.runner import LessonRunner


class LessonListScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("q", "app.quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        lessons = load_all_lessons()
        yield Static("  Lessons — pick one to start\n", id="header")
        items = [
            ListItem(
                Static(f"  {lesson.title}  (~{lesson.estimated_minutes} min)"),
                id=f"l-{lesson.id}",
            )
            for lesson in lessons
        ]
        lv = ListView(*items, id="lesson-list")
        yield lv
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        raw_id = event.item.id
        if raw_id and raw_id.startswith("l-"):
            lesson_id = raw_id[len("l-"):]
            self.app.push_screen(LessonPlayerScreen(lesson_id=lesson_id))


class LessonPlayerScreen(Screen):
    BINDINGS = [
        Binding("n", "next_step", "Next"),
        Binding("escape", "app.pop_screen", "Back"),
        Binding("q", "app.quit", "Quit"),
    ]

    def __init__(self, lesson_id: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self._lesson_id = lesson_id
        self._runner: LessonRunner | None = None

    def on_mount(self) -> None:
        try:
            lesson = load_lesson(self._lesson_id)
            self._runner = LessonRunner(lesson)
            self._render_step()
        except LessonParseError as exc:
            self.query_one("#content", Static).update(f"Error loading lesson: {exc}")

    def compose(self) -> ComposeResult:
        yield Static("", id="progress")
        yield Markdown("", id="content")
        yield Static("  Press [N] for next step, [Escape] to go back.", id="hint")
        yield Footer()

    def _render_step(self) -> None:
        if self._runner is None:
            return
        step = self._runner.current_step
        current, total = self._runner.progress
        self.query_one("#progress", Static).update(
            f"  Step {current + 1} of {total} — {self._runner.lesson.title}"
        )
        if step is None:
            self.query_one("#content", Markdown).update(
                "## Lesson complete!\n\nPress [Escape] to go back and take the quiz."
            )
        else:
            self.query_one("#content", Markdown).update(step.content)

    def action_next_step(self) -> None:
        if self._runner and not self._runner.complete:
            self._runner.advance()
            self._render_step()


class LessonScreen(Screen):
    def __init__(self, lesson_id: str | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self._lesson_id = lesson_id

    def on_mount(self) -> None:
        if self._lesson_id:
            self.app.switch_screen(LessonPlayerScreen(lesson_id=self._lesson_id))
        else:
            self.app.switch_screen(LessonListScreen())
