from textual.widget import Widget
from textual.app import RenderResult
from rich.text import Text


class LessonProgressBar(Widget):
    """Shows lesson progress as a simple ASCII bar."""

    def __init__(self, current: int, total: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.current = current
        self.total = total

    def render(self) -> RenderResult:
        if self.total == 0:
            return Text("No steps")
        pct = self.current / self.total
        filled = int(pct * 20)
        bar = "█" * filled + "░" * (20 - filled)
        return Text(f"Progress: [{bar}] {self.current}/{self.total}")
