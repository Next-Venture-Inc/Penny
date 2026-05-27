from dataclasses import dataclass


@dataclass(frozen=True)
class DCAResult:
    total_invested: float
    final_value: float
    total_gains: float
    average_cost_per_unit: float
    units_owned: float
    multiple: float


def calculate_dca(
    monthly_amount: float,
    annual_rate_pct: float,
    years: int,
    starting_price: float = 100.0,
) -> DCAResult:
    """Simulate dollar-cost averaging into an asset over time."""
    if years <= 0:
        raise ValueError("years must be positive")
    if starting_price <= 0:
        raise ValueError("starting_price must be positive")

    months = years * 12
    monthly_rate = annual_rate_pct / 100.0 / 12

    total_invested = monthly_amount * months
    units = 0.0
    price = starting_price

    for month in range(months):
        if monthly_rate > 0:
            price = starting_price * (1 + monthly_rate) ** month
        units += monthly_amount / price if price > 0 else 0

    final_price = starting_price * (1 + monthly_rate) ** months if monthly_rate > 0 else starting_price
    final_value = units * final_price
    total_gains = final_value - total_invested
    avg_cost = total_invested / units if units > 0 else 0.0
    multiple = final_value / total_invested if total_invested > 0 else 0.0

    return DCAResult(
        total_invested=round(total_invested, 2),
        final_value=round(final_value, 2),
        total_gains=round(total_gains, 2),
        average_cost_per_unit=round(avg_cost, 4),
        units_owned=round(units, 4),
        multiple=round(multiple, 4),
    )
