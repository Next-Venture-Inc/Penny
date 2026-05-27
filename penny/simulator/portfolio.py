from penny.models.portfolio import Portfolio, Position


class PortfolioManager:
    """Manages virtual buy/sell operations on a paper portfolio."""

    def __init__(self, starting_cash: float = 10_000.0) -> None:
        self.portfolio = Portfolio(cash=starting_cash)

    def buy(self, ticker: str, price: float, dollars: float) -> str:
        """Buy as many shares as possible with the given dollar amount."""
        ticker = ticker.upper()
        if dollars > self.portfolio.cash:
            return f"Not enough cash. You have ${self.portfolio.cash:,.2f}."
        shares = dollars / price
        self.portfolio.cash -= dollars

        if ticker in self.portfolio.positions:
            existing = self.portfolio.positions[ticker]
            total_shares = existing.shares + shares
            avg_cost = (
                existing.shares * existing.avg_cost + shares * price
            ) / total_shares
            self.portfolio.positions[ticker] = Position(ticker, total_shares, avg_cost)
        else:
            self.portfolio.positions[ticker] = Position(ticker, shares, price)

        return f"Bought {shares:.4f} shares of {ticker} at ${price:.2f}."

    def sell(self, ticker: str, price: float, shares: float) -> str:
        """Sell a number of shares."""
        ticker = ticker.upper()
        if ticker not in self.portfolio.positions:
            return f"You don't own any {ticker}."
        position = self.portfolio.positions[ticker]
        if shares > position.shares:
            return f"You only own {position.shares:.4f} shares of {ticker}."

        proceeds = shares * price
        self.portfolio.cash += proceeds
        remaining = position.shares - shares

        if remaining < 1e-6:
            del self.portfolio.positions[ticker]
        else:
            self.portfolio.positions[ticker] = Position(ticker, remaining, position.avg_cost)

        gain = (price - position.avg_cost) * shares
        return (
            f"Sold {shares:.4f} shares of {ticker} at ${price:.2f}. "
            f"Gain/Loss: ${gain:+,.2f}."
        )
