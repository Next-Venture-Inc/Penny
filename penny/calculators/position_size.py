from dataclasses import dataclass


@dataclass(frozen=True)
class PositionSizeResult:
    position_size: float
    shares_to_buy: float
    risk_amount: float
    risk_pct_of_portfolio: float


def calculate_position_size(
    portfolio_value: float,
    risk_per_trade_pct: float,
    entry_price: float,
    stop_loss_price: float,
) -> PositionSizeResult:
    """Calculate how many shares to buy based on your risk tolerance.

    risk_per_trade_pct: the % of your total money you're OK losing on this trade.
    entry_price: the price you plan to buy at.
    stop_loss_price: the price where you'd sell to cut your losses.
    """
    if portfolio_value <= 0:
        raise ValueError("portfolio_value must be positive")
    if entry_price <= 0:
        raise ValueError("entry_price must be positive")
    if stop_loss_price >= entry_price:
        raise ValueError("stop_loss_price must be below entry_price")
    if not (0 < risk_per_trade_pct <= 100):
        raise ValueError("risk_per_trade_pct must be between 0 and 100")

    risk_amount = portfolio_value * (risk_per_trade_pct / 100)
    risk_per_share = entry_price - stop_loss_price
    shares = risk_amount / risk_per_share
    position_size = shares * entry_price

    return PositionSizeResult(
        position_size=round(position_size, 2),
        shares_to_buy=round(shares, 4),
        risk_amount=round(risk_amount, 2),
        risk_pct_of_portfolio=round((position_size / portfolio_value) * 100, 2),
    )
