import pytest

from penny.calculators.compound import calculate_compound, CompoundResult
from penny.calculators.dca import calculate_dca, DCAResult
from penny.calculators.position_size import calculate_position_size, PositionSizeResult
from penny.calculators.tfsa import calculate_tfsa, TFSAResult


class TestCompound:
    def test_basic_growth(self):
        result = calculate_compound(1000, 0, 10, 1)
        assert result.final_value == pytest.approx(1100.0, rel=0.01)

    def test_two_years_compounding(self):
        result = calculate_compound(500, 0, 8, 2)
        assert result.final_value == pytest.approx(583.2, rel=0.01)

    def test_zero_rate_principal_only(self):
        result = calculate_compound(1000, 0, 0, 5)
        assert result.final_value == pytest.approx(1000.0, rel=0.01)
        assert result.total_gains == pytest.approx(0.0, abs=0.01)

    def test_zero_principal_contributions_only(self):
        result = calculate_compound(0, 100, 0, 12)
        assert result.total_invested == pytest.approx(14400.0, rel=0.01)
        assert result.final_value == pytest.approx(14400.0, rel=0.01)

    def test_rule_of_72(self):
        result = calculate_compound(1000, 0, 10, 1)
        assert result.years_to_double == pytest.approx(7.2, rel=0.01)

    def test_zero_rate_infinite_doubling(self):
        result = calculate_compound(1000, 0, 0, 1)
        assert result.years_to_double == float("inf")

    def test_multiple_calculation(self):
        result = calculate_compound(1000, 0, 10, 10)
        assert result.multiple == pytest.approx(result.final_value / result.total_invested, rel=0.01)

    def test_invalid_years_raises(self):
        with pytest.raises(ValueError):
            calculate_compound(1000, 0, 10, 0)

    def test_returns_frozen_dataclass(self):
        result = calculate_compound(1000, 0, 10, 1)
        with pytest.raises(Exception):
            result.final_value = 999

    def test_with_monthly_contribution(self):
        result = calculate_compound(0, 200, 8, 30)
        assert result.final_value > result.total_invested
        assert result.total_gains > 0


class TestDCA:
    def test_basic_dca(self):
        result = calculate_dca(200, 0, 12)
        assert result.total_invested == pytest.approx(200 * 12 * 12, rel=0.01)

    def test_zero_rate_no_gains(self):
        result = calculate_dca(100, 0, 10)
        assert result.total_invested == pytest.approx(result.final_value, rel=0.01)

    def test_positive_rate_grows(self):
        result = calculate_dca(100, 8, 20)
        assert result.final_value > result.total_invested

    def test_invalid_years_raises(self):
        with pytest.raises(ValueError):
            calculate_dca(100, 8, 0)

    def test_invalid_price_raises(self):
        with pytest.raises(ValueError):
            calculate_dca(100, 8, 10, starting_price=0)

    def test_multiple_above_one(self):
        result = calculate_dca(100, 10, 20)
        assert result.multiple > 1.0


class TestPositionSize:
    def test_basic_position(self):
        result = calculate_position_size(
            portfolio_value=10_000,
            risk_per_trade_pct=2,
            entry_price=100,
            stop_loss_price=90,
        )
        assert result.risk_amount == pytest.approx(200.0, rel=0.01)
        assert result.shares_to_buy == pytest.approx(20.0, rel=0.01)
        assert result.position_size == pytest.approx(2000.0, rel=0.01)

    def test_stop_loss_above_entry_raises(self):
        with pytest.raises(ValueError):
            calculate_position_size(10_000, 2, 90, 100)

    def test_zero_portfolio_raises(self):
        with pytest.raises(ValueError):
            calculate_position_size(0, 2, 100, 90)

    def test_zero_entry_raises(self):
        with pytest.raises(ValueError):
            calculate_position_size(10_000, 2, 0, 90)

    def test_invalid_risk_pct_raises(self):
        with pytest.raises(ValueError):
            calculate_position_size(10_000, 0, 100, 90)


class TestTFSA:
    def test_basic_projection(self):
        result = calculate_tfsa(1990, 0, 500, 7, 20)
        assert result.projected_value > 0
        assert result.tax_free_gains >= 0

    def test_zero_years_raises(self):
        with pytest.raises(ValueError):
            calculate_tfsa(1990, 0, 500, 7, 0)

    def test_room_for_2009_eligible(self):
        result = calculate_tfsa(1985, 0, 0, 0, 1)
        assert result.total_contribution_room == pytest.approx(102_000, rel=0.01)

    def test_tax_saved_positive_with_gains(self):
        result = calculate_tfsa(1980, 0, 1000, 8, 20)
        assert result.tax_saved > 0
        assert result.tax_free_gains > 0
