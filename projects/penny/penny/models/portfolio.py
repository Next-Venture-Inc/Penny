from dataclasses import dataclass, field
from datetime import date


@dataclass
class Position:
    ticker: str
    shares: float
    avg_cost: float

    @property
    def total_cost(self) -> float:
        return self.shares * self.avg_cost


@dataclass
class Portfolio:
    cash: float = 10_000.0
    positions: dict[str, Position] = field(default_factory=dict)
    start_date: date = field(default_factory=date.today)

    @property
    def total_invested(self) -> float:
        return sum(p.total_cost for p in self.positions.values())

    def market_value(self, prices: dict[str, float]) -> float:
        equity = sum(
            p.shares * prices.get(p.ticker, p.avg_cost)
            for p in self.positions.values()
        )
        return self.cash + equity
