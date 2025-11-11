import pytest
from httpx import AsyncClient, ASGITransport

# 테스트 대상 FastAPI 앱을 가져옵니다.
from app.main import app

# `pytest-asyncio`가 설치되어 있으면, pytest는 `async def`로 정의된 테스트 함수를 자동으로 인식합니다.

@pytest.fixture
async def client():
    """
    테스트를 위한 비동기 HTTP 클라이언트를 생성하는 pytest fixture 입니다.
    ASGITransport를 사용하여 실제 HTTP 요청 없이 FastAPI 앱과 직접 통신합니다.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

async def test_health_check(client: AsyncClient):
    """
    /health 엔드포인트가 정상적으로 응답하는지 테스트합니다.
    - 상태 코드가 200 OK인지 확인합니다.
    - JSON 응답이 {"status": "ok"}인지 확인합니다.
    """
    response = await client.get("/health")
    
    # 응답 상태 코드를 검증합니다.
    assert response.status_code == 200
    
    # 응답 JSON 본문을 검증합니다.
    assert response.json() == {"status": "ok"}

async def test_read_root(client: AsyncClient):
    """
    루트(/) 엔드포인트가 정상적으로 응답하는지 테스트합니다.
    """
    response = await client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Trading Bot API"}
