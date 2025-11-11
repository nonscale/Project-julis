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
    # 테스트를 위해 임시 메모리 DB를 초기화합니다.
    # 이렇게 하면 각 테스트가 독립적인 환경에서 실행됩니다.
    from app.api.endpoints import strategies
    strategies.db_strategies = {}
    strategies.strategy_id_counter = 1
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test/api/v1/strategies") as c:
        yield c

async def test_create_strategy(client: AsyncClient):
    """
    전략 생성 API가 정상적으로 동작하는지 테스트합니다.
    """
    response = await client.post("/", json={"name": "Test Strategy", "description": "A test description"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Strategy"
    assert data["description"] == "A test description"
    assert "id" in data
    assert "created_at" in data

async def test_read_strategy(client: AsyncClient):
    """
    특정 전략을 ID로 조회하는 API를 테스트합니다.
    """
    # 먼저 테스트용 전략을 생성합니다.
    create_response = await client.post("/", json={"name": "Readable Strategy", "description": "..."})
    strategy_id = create_response.json()["id"]

    # 생성된 전략을 조회합니다.
    response = await client.get(f"/{strategy_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == strategy_id
    assert data["name"] == "Readable Strategy"

async def test_read_inexistent_strategy(client: AsyncClient):
    """
    존재하지 않는 전략 조회 시 404 오류를 반환하는지 테스트합니다.
    """
    response = await client.get("/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Strategy not found"}

async def test_read_strategies(client: AsyncClient):
    """
    전체 전략 목록 조회 API를 테스트합니다.
    """
    # 테스트용 전략 2개를 생성합니다.
    await client.post("/", json={"name": "Strategy 1", "description": "..."})
    await client.post("/", json={"name": "Strategy 2", "description": "..."})

    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Strategy 1"
    assert data[1]["name"] == "Strategy 2"

async def test_update_strategy(client: AsyncClient):
    """
    전략 수정 API를 테스트합니다.
    """
    # 테스트용 전략을 생성합니다.
    create_response = await client.post("/", json={"name": "Original Name", "description": "Original Desc"})
    strategy_id = create_response.json()["id"]

    # 생성된 전략을 수정합니다.
    update_response = await client.put(f"/{strategy_id}", json={"name": "Updated Name", "description": "Updated Desc"})
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["name"] == "Updated Name"
    assert updated_data["description"] == "Updated Desc"

    # 수정된 내용이 잘 반영되었는지 다시 조회하여 확인합니다.
    get_response = await client.get(f"/{strategy_id}")
    assert get_response.json()["name"] == "Updated Name"

async def test_delete_strategy(client: AsyncClient):
    """
    전략 삭제 API를 테스트합니다.
    """
    # 테스트용 전략을 생성합니다.
    create_response = await client.post("/", json={"name": "To Be Deleted", "description": "..."})
    strategy_id = create_response.json()["id"]

    # 생성된 전략을 삭제합니다.
    delete_response = await client.delete(f"/{strategy_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Strategy deleted successfully"}

    # 삭제된 전략을 다시 조회했을 때 404 오류가 발생하는지 확인합니다.
    get_response = await client.get(f"/{strategy_id}")
    assert get_response.status_code == 404
