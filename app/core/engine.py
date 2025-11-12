import polars as pl
from app.core.brokers.upbit import UpbitBroker

class ScanEngine:
    def __init__(self, broker: UpbitBroker):
        self.broker = broker
    def run_primary_scan(self, market: str = "KRW") -> pl.DataFrame:
        tickers = self.broker.get_tickers(market=market)
        all_prices_data = self.broker.get_current_price(tickers)
        df = pl.DataFrame({
            "ticker": list(all_prices_data.keys()),
            "price": list(all_prices_data.values())
        })
        return df