from datetime import date, timedelta

import pandas as pd

from penny.simulator.data import fetch_history
from penny.simulator.portfolio import PortfolioManager

BENCHMARK_TICKER = "XIU.TO"
STARTING_CASH = 10_000.0


class SimulatorEngine:
    """Paper trading engine — uses historical prices, no real money."""

    def __init__(self) -> None:
        self.manager = PortfolioManager(STARTING_CASH)
        self._history: list[dict] = []

    @property
    def portfolio(self):
        return self.manager.portfolio

    def get_price(self, ticker: str, on_date: date) -> float | None:
        """Look up the closing price of a ticker on a given date."""
        try:
            df = fetch_history(ticker, on_date - timedelta(days=7), on_date)
            if df.empty:
                return None
            close_col = "Close"
            if isinstance(df.columns, pd.MultiIndex):
                close_col = ("Close", ticker.upper())
            row = df[close_col].dropna().iloc[-1]
            return float(row)
        except Exception:
            return None

    def buy(self, ticker: str, on_date: date, dollars: float) -> str:
        price = self.get_price(ticker, on_date)
        if price is None:
            return f"Could not get price for {ticker} on {on_date}. Try a different date."
        result = self.manager.buy(ticker, price, dollars)
        self._history.append({"date": on_date, "action": "buy", "ticker": ticker, "price": price, "dollars": dollars})
        return result

    def sell(self, ticker: str, on_date: date, shares: float) -> str:
        price = self.get_price(ticker, on_date)
        if price is None:
            return f"Could not get price for {ticker} on {on_date}."
        result = self.manager.sell(ticker, price, shares)
        self._history.append({"date": on_date, "action": "sell", "ticker": ticker, "price": price, "shares": shares})
        return result

    def portfolio_value(self, on_date: date) -> float:
        prices = {}
        for ticker in self.portfolio.positions:
            p = self.get_price(ticker, on_date)
            if p is not None:
                prices[ticker] = p
        return self.portfolio.market_value(prices)

    def pnl_summary(self, on_date: date) -> str:
        current_value = self.portfolio_value(on_date)
        gain = current_value - STARTING_CASH
        pct = (gain / STARTING_CASH) * 100
        return (
            f"Portfolio value: ${current_value:,.2f} | "
            f"Gain/Loss: ${gain:+,.2f} ({pct:+.1f}%) | "
            f"Cash: ${self.portfolio.cash:,.2f}"
        )
