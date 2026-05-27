from dataclasses import dataclass


@dataclass(frozen=True)
class CompoundResult:
    final_value: float
    total_invested: float
    total_gains: float
    multiple: float
    years_to_double: float


def calculate_compound(
    principal: float,
    monthly_contribution: float,
    annual_rate_pct: float,
    years: int,
) -> CompoundResult:
    """Calculate compound growth with optional monthly contributions."""
    if years <= 0:
        raise ValueError("years must be positive")

    rate = annual_rate_pct / 100.0
    monthly_rate = rate / 12
    months = years * 12

    if monthly_rate == 0:
        final_value = principal + monthly_contribution * months
    else:
        final_value = principal * (1 + rate) ** years + monthly_contribution * (
            ((1 + monthly_rate) ** months - 1) / monthly_rate
        )

    total_invested = principal + monthly_contribution * months
    total_gains = final_value - total_invested
    multiple = final_value / total_invested if total_invested > 0 else 0.0

    if annual_rate_pct > 0:
        years_to_double = 72 / annual_rate_pct
    else:
        years_to_double = float("inf")

    return CompoundResult(
        final_value=round(final_value, 2),
        total_invested=round(total_invested, 2),
        total_gains=round(total_gains, 2),
        multiple=round(multiple, 4),
        years_to_double=round(years_to_double, 1),
    )
