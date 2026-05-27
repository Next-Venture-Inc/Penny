import json
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from penny.config import config


def _cache_path(ticker: str) -> Path:
    path = Path(config.data_cache_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path / f"{ticker.upper()}.parquet"


def fetch_history(
    ticker: str,
    start: date,
    end: date,
) -> pd.DataFrame:
    """Fetch OHLCV data, using local cache if available.

    Returns a DataFrame with columns: Open, High, Low, Close, Volume.
    Falls back to cached data if network is unavailable.
    """
    cache = _cache_path(ticker)

    if cache.exists():
        df = pd.read_parquet(cache)
        needed_start = pd.Timestamp(start)
        needed_end = pd.Timestamp(end)
        cached_start = df.index.min()
        cached_end = df.index.max()
        if cached_start <= needed_start and cached_end >= needed_end:
            mask = (df.index >= needed_start) & (df.index <= needed_end)
            return df.loc[mask]

    try:
        import yfinance as yf

        raw = yf.download(
            ticker,
            start=start.isoformat(),
            end=(end + timedelta(days=1)).isoformat(),
            progress=False,
            auto_adjust=True,
        )
        if raw.empty:
            raise ValueError(f"No data returned for {ticker}")
        raw.to_parquet(cache)
        return raw
    except Exception:
        if cache.exists():
            return pd.read_parquet(cache)
        raise
