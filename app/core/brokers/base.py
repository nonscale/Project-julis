from abc import ABC, abstractmethod
from typing import List, Dict, Any
import pandas as pd

class BaseBroker(ABC):
    @abstractmethod
    def get_tickers(self, market: str) -> List[str]:
        pass
    @abstractmethod
    def get_ohlcv(self, ticker: str, interval: str = 'day', count: int = 200) -> pd.DataFrame:
        pass
    @abstractmethod
    def get_current_price(self, ticker: str | List[str]) -> float | Dict[str, float]:
        pass
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = [col.lower() for col in df.columns]
        return df