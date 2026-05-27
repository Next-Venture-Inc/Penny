from textual.widget import Widget
from textual.app import RenderResult
from rich.text import Text

SPARKS = "▁▂▃▄▅▆▇█"


class Sparkline(Widget):
    """Renders a small ASCII sparkline chart from a list of values."""

    def __init__(self, values: list[float], **kwargs) -> None:
        super().__init__(**kwargs)
        self.values = values

    def render(self) -> RenderResult:
        if not self.values:
            return Text("")
        min_v = min(self.values)
        max_v = max(self.values)
        spread = max_v - min_v or 1
        chars = [
            SPARKS[int((v - min_v) / spread * (len(SPARKS) - 1))]
            for v in self.values
        ]
        return Text("".join(chars))
