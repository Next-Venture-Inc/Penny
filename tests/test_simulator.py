import pytest

from penny.simulator.portfolio import PortfolioManager
from penny.models.portfolio import Portfolio, Position


class TestPortfolioManager:
    def test_starts_with_correct_cash(self):
        pm = PortfolioManager(10_000)
        assert pm.portfolio.cash == 10_000

    def test_buy_reduces_cash(self):
        pm = PortfolioManager(10_000)
        pm.buy("AAPL", 100.0, 500.0)
        assert pm.portfolio.cash == pytest.approx(9_500.0)

    def test_buy_creates_position(self):
        pm = PortfolioManager(10_000)
        pm.buy("AAPL", 100.0, 500.0)
        assert "AAPL" in pm.portfolio.positions
        assert pm.portfolio.positions["AAPL"].shares == pytest.approx(5.0)

    def test_buy_more_than_cash_fails(self):
        pm = PortfolioManager(100)
        result = pm.buy("AAPL", 100.0, 500.0)
        assert "Not enough" in result
        assert pm.portfolio.cash == 100

    def test_sell_increases_cash(self):
        pm = PortfolioManager(10_000)
        pm.buy("AAPL", 100.0, 1000.0)
        pm.sell("AAPL", 150.0, 5.0)
        assert pm.portfolio.cash == pytest.approx(9_000 + 750, rel=0.01)

    def test_sell_removes_position_when_zero_shares(self):
        pm = PortfolioManager(10_000)
        pm.buy("AAPL", 100.0, 1000.0)
        pm.sell("AAPL", 100.0, 10.0)
        assert "AAPL" not in pm.portfolio.positions

    def test_sell_nonexistent_fails(self):
        pm = PortfolioManager(10_000)
        result = pm.sell("AAPL", 100.0, 5.0)
        assert "don't own" in result

    def test_sell_too_many_shares_fails(self):
        pm = PortfolioManager(10_000)
        pm.buy("AAPL", 100.0, 500.0)
        result = pm.sell("AAPL", 100.0, 100.0)
        assert "only own" in result

    def test_buy_averages_cost(self):
        pm = PortfolioManager(10_000)
        pm.buy("AAPL", 100.0, 1000.0)
        pm.buy("AAPL", 200.0, 1000.0)
        pos = pm.portfolio.positions["AAPL"]
        assert pos.shares == pytest.approx(15.0, rel=0.01)
        assert pos.avg_cost == pytest.approx(133.33, rel=0.01)

    def test_ticker_normalized_to_uppercase(self):
        pm = PortfolioManager(10_000)
        pm.buy("aapl", 100.0, 500.0)
        assert "AAPL" in pm.portfolio.positions


class TestPortfolioModel:
    def test_total_invested_sums_positions(self):
        p = Portfolio(cash=5000)
        p.positions["AAPL"] = Position("AAPL", 10, 100)
        p.positions["GOOG"] = Position("GOOG", 5, 200)
        assert p.total_invested == pytest.approx(2000, rel=0.01)

    def test_market_value_uses_current_prices(self):
        p = Portfolio(cash=5000)
        p.positions["AAPL"] = Position("AAPL", 10, 100)
        value = p.market_value({"AAPL": 150})
        assert value == pytest.approx(5000 + 1500, rel=0.01)

    def test_market_value_uses_avg_cost_when_price_missing(self):
        p = Portfolio(cash=5000)
        p.positions["AAPL"] = Position("AAPL", 10, 100)
        value = p.market_value({})
        assert value == pytest.approx(5000 + 1000, rel=0.01)
