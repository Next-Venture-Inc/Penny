from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Button, Footer, Input, Markdown, Static

from penny.calculators.compound import calculate_compound
from penny.calculators.dca import calculate_dca
from penny.calculators.tfsa import calculate_tfsa


class CalculatorScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("q", "app.quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Static("  Calculators\n", id="header")
        yield Static("  Compound Growth Calculator\n", id="calc-label")
        yield Input(placeholder="Starting amount (e.g. 1000)", id="principal")
        yield Input(placeholder="Monthly contribution (e.g. 100)", id="monthly")
        yield Input(placeholder="Annual return % (e.g. 7)", id="rate")
        yield Input(placeholder="Years (e.g. 20)", id="years")
        yield Button("Calculate compound growth", id="btn-compound")
        yield Markdown("", id="result")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-compound":
            self._run_compound()

    def _run_compound(self) -> None:
        try:
            principal = float(self.query_one("#principal", Input).value or "0")
            monthly = float(self.query_one("#monthly", Input).value or "0")
            rate = float(self.query_one("#rate", Input).value or "0")
            years = int(self.query_one("#years", Input).value or "0")
            result = calculate_compound(principal, monthly, rate, years)
            output = (
                f"### Results\n\n"
                f"- **Final value:** ${result.final_value:,.2f}\n"
                f"- **Total you put in:** ${result.total_invested:,.2f}\n"
                f"- **Free gains from growth:** ${result.total_gains:,.2f}\n"
                f"- **Your money multiplied:** {result.multiple:.2f}x\n"
                f"- **Years to double at this rate:** {result.years_to_double}\n"
            )
            self.query_one("#result", Markdown).update(output)
        except (ValueError, ZeroDivisionError) as exc:
            self.query_one("#result", Markdown).update(f"Please check your inputs: {exc}")
