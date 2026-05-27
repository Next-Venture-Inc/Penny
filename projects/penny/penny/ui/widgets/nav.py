from textual.widget import Widget
from textual.app import RenderResult
from rich.text import Text


class NavHint(Widget):
    """Shows keyboard shortcut hints."""

    def __init__(self, hints: list[tuple[str, str]], **kwargs) -> None:
        super().__init__(**kwargs)
        self.hints = hints

    def render(self) -> RenderResult:
        parts = [f"[{key}] {label}" for key, label in self.hints]
        return Text("  " + "   ".join(parts))
