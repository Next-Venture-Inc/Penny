from dataclasses import dataclass

ANNUAL_CONTRIBUTION_ROOM_2025 = 7_000.0

CUMULATIVE_ROOM_BY_YEAR: dict[int, float] = {
    2009: 5_000,
    2010: 10_000,
    2011: 15_000,
    2012: 20_000,
    2013: 25_500,
    2014: 31_000,
    2015: 41_000,
    2016: 46_500,
    2017: 52_000,
    2018: 57_500,
    2019: 63_500,
    2020: 69_500,
    2021: 75_500,
    2022: 81_500,
    2023: 88_000,
    2024: 95_000,
    2025: 102_000,
}


@dataclass(frozen=True)
class TFSAResult:
    total_contribution_room: float
    projected_value: float
    tax_free_gains: float
    equivalent_taxable_gains: float
    tax_saved: float


def calculate_tfsa(
    birth_year: int,
    current_balance: float,
    monthly_contribution: float,
    annual_rate_pct: float,
    years: int,
    marginal_tax_rate_pct: float = 43.41,
) -> TFSAResult:
    """Project TFSA growth and the tax savings vs a taxable account.

    marginal_tax_rate_pct: defaults to Ontario top combined rate (2025).
    """
    if years <= 0:
        raise ValueError("years must be positive")

    eligible_since = max(birth_year + 18, 2009)
    current_year = 2025
    room = CUMULATIVE_ROOM_BY_YEAR.get(current_year, 102_000)
    if eligible_since > current_year:
        room = 0.0
    elif eligible_since > 2009:
        room = CUMULATIVE_ROOM_BY_YEAR.get(current_year, 102_000) - CUMULATIVE_ROOM_BY_YEAR.get(eligible_since - 1, 0)

    rate = annual_rate_pct / 100
    monthly_rate = rate / 12
    months = years * 12

    if monthly_rate == 0:
        projected = current_balance + monthly_contribution * months
    else:
        projected = current_balance * (1 + rate) ** years + monthly_contribution * (
            ((1 + monthly_rate) ** months - 1) / monthly_rate
        )

    total_contrib = current_balance + monthly_contribution * months
    tax_free_gains = projected - total_contrib

    tax_saved = tax_free_gains * (marginal_tax_rate_pct / 100)

    return TFSAResult(
        total_contribution_room=round(room, 2),
        projected_value=round(projected, 2),
        tax_free_gains=round(tax_free_gains, 2),
        equivalent_taxable_gains=round(tax_free_gains * (1 - marginal_tax_rate_pct / 100), 2),
        tax_saved=round(tax_saved, 2),
    )
