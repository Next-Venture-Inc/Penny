from datetime import date

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Button, Footer, Input, Markdown, Static

from penny.simulator.engine import SimulatorEngine


class SimulatorScreen(Screen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("q", "app.quit", "Quit"),
    ]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._engine = SimulatorEngine()

    def compose(self) -> ComposeResult:
        yield Static("  Paper Trading Simulator — $10,000 virtual money\n", id="header")
        yield Static("  Ticker (e.g. AAPL, XIU.TO):", id="lbl-ticker")
        yield Input(placeholder="Ticker", id="ticker")
        yield Static("  Date (YYYY-MM-DD):", id="lbl-date")
        yield Input(placeholder=str(date.today()), id="trade-date")
        yield Static("  Amount in $ to buy (or shares to sell):", id="lbl-amount")
        yield Input(placeholder="Amount", id="amount")
        yield Button("Buy", id="btn-buy", variant="success")
        yield Button("Sell shares", id="btn-sell", variant="error")
        yield Button("Show portfolio value", id="btn-value")
        yield Markdown("", id="output")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        ticker = self.query_one("#ticker", Input).value.strip().upper()
        date_str = self.query_one("#trade-date", Input).value.strip()
        amount_str = self.query_one("#amount", Input).value.strip()

        try:
            trade_date = date.fromisoformat(date_str) if date_str else date.today()
        except ValueError:
            self._show("Date must be in YYYY-MM-DD format, e.g. 2023-01-15")
            return

        if event.button.id == "btn-buy":
            if not ticker or not amount_str:
                self._show("Enter a ticker and an amount to buy.")
                return
            try:
                dollars = float(amount_str)
            except ValueError:
                self._show("Amount must be a number.")
                return
            result = self._engine.buy(ticker, trade_date, dollars)
            self._show(result)

        elif event.button.id == "btn-sell":
            if not ticker or not amount_str:
                self._show("Enter a ticker and number of shares to sell.")
                return
            try:
                shares = float(amount_str)
            except ValueError:
                self._show("Shares must be a number.")
                return
            result = self._engine.sell(ticker, trade_date, shares)
            self._show(result)

        elif event.button.id == "btn-value":
            result = self._engine.pnl_summary(trade_date)
            self._show(result)

    def _show(self, msg: str) -> None:
        self.query_one("#output", Markdown).update(msg)
