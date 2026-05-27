from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, Input, Markdown, Static

from penny.config import config
from penny.tutor.claude_tutor import AITutor, TutorUnavailable

UNAVAILABLE_MSG = (
    "AI tutor unavailable — set ANTHROPIC_API_KEY to enable.\n\n"
    "You can still use lessons, the simulator, and calculators without it."
)


class TutorScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("q", "app.quit", "Quit"),
    ]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._tutor = AITutor()
        self._history: list[dict] = []

    def compose(self) -> ComposeResult:
        if not self._tutor.available:
            yield Static(UNAVAILABLE_MSG, id="unavailable")
        else:
            yield Static("  AI Tutor — ask anything about investing\n", id="header")
            yield Markdown("", id="conversation")
            yield Input(placeholder="Type your question and press Enter...", id="input")
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        question = event.value.strip()
        if not question:
            return
        self.query_one("#input", Input).value = ""
        self.query_one("#input", Input).disabled = True
        self._append_message("You", question)
        self.run_worker(self._ask(question), exclusive=True)

    async def _ask(self, question: str) -> None:
        try:
            response = self._tutor.ask(question, self._history)
            self._history.append({"role": "user", "content": question})
            self._history.append({"role": "assistant", "content": response})
            self._append_message("Penny", response)
        except TutorUnavailable as exc:
            self._append_message("Error", str(exc))
        finally:
            self.query_one("#input", Input).disabled = False
            self.query_one("#input", Input).focus()

    def _append_message(self, sender: str, text: str) -> None:
        conv = self.query_one("#conversation", Markdown)
        current = getattr(conv, "_markdown", "") or ""
        conv.update(current + f"\n\n**{sender}:** {text}")
