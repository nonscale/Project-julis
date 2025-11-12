import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.brokers.upbit import UpbitBroker

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

async def test_run_scan_successful(client: AsyncClient, monkeypatch):
    mock_tickers = ["KRW-BTC", "KRW-ETH"]
    mock_prices = {"KRW-BTC": 80000000.0, "KRW-ETH": 4000000.0}
    monkeypatch.setattr(UpbitBroker, "get_tickers", lambda self, market: mock_tickers)
    monkeypatch.setattr(UpbitBroker, "get_current_price", lambda self, tickers: mock_prices)
    response = await client.post("/api/v1/scans/1/run")
    assert response.status_code == 200
    data = response.json()
    assert data["result_count"] == 2

async def test_stop_scan(client: AsyncClient):
    response = await client.post("/api/v1/scans/1/stop")
    assert response.status_code == 200