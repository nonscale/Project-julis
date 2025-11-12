import pyupbit
import pandas as pd
from typing import List, Dict, Any
from .base import BaseBroker

class UpbitBroker(BaseBroker):
    def get_tickers(self, market: str = "KRW") -> List[str]:
        return pyupbit.get_tickers(fiat=market)
    def get_ohlcv(self, ticker: str, interval: str = 'day', count: int = 200) -> pd.DataFrame:
        df = pyupbit.get_ohlcv(ticker, interval=interval, count=count)
        return self._standardize_columns(df)
    def get_current_price(self, ticker: str | List[str]) -> float | Dict[str, float]:
        return pyupbit.get_current_price(ticker)
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = [col.lower() for col in df.columns]
        if 'value' in df.columns:
            df.rename(columns={'value': 'amount'}, inplace=True)
        return df