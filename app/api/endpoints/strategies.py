from fastapi import APIRouter, HTTPException
from typing import List
import datetime

# 이전 단계에서 정의한 Pydantic 모델들을 가져옵니다.
from app.models.strategy import Strategy, StrategyCreate, StrategyBase

# APIRouter 인스턴스를 생성합니다. 이 라우터는 나중에 main.py에서 포함될 것입니다.
router = APIRouter()

# --- 메모리 내 데이터베이스 (In-memory DB) ---
# 실제 데이터베이스 대신, 간단한 Python dict를 사용하여 데이터를 임시로 저장합니다.
# 이는 API의 로직을 빠르게 개발하고 테스트하기 위함입니다.
db_strategies = {}
strategy_id_counter = 1
# -----------------------------------------

@router.post("/", response_model=Strategy, status_code=201)
async def create_strategy(strategy_in: StrategyCreate):
    """
    새로운 트레이딩 전략을 생성합니다.
    """
    global strategy_id_counter
    new_id = strategy_id_counter
    
    new_strategy = Strategy(
        id=new_id,
        name=strategy_in.name,
        description=strategy_in.description,
        created_at=datetime.datetime.now()
    )
    
    db_strategies[new_id] = new_strategy
    strategy_id_counter += 1
    
    return new_strategy

@router.get("/{strategy_id}", response_model=Strategy)
async def read_strategy(strategy_id: int):
    """
    주어진 ID를 가진 특정 전략의 정보를 조회합니다.
    """
    strategy = db_strategies.get(strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy

@router.get("/", response_model=List[Strategy])
async def read_strategies():
    """
    저장된 모든 전략의 목록을 조회합니다.
    """
    return list(db_strategies.values())

@router.put("/{strategy_id}", response_model=Strategy)
async def update_strategy(strategy_id: int, strategy_in: StrategyBase):
    """
    주어진 ID를 가진 전략의 정보를 수정합니다.
    """
    if strategy_id not in db_strategies:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    strategy = db_strategies[strategy_id]
    strategy.name = strategy_in.name
    strategy.description = strategy_in.description
    
    return strategy

@router.delete("/{strategy_id}", response_model=dict)
async def delete_strategy(strategy_id: int):
    """
    주어진 ID를 가진 전략을 삭제합니다.
    """
    if strategy_id not in db_strategies:
        raise HTTPException(status_code=404, detail="Strategy not found")
    
    del db_strategies[strategy_id]
    
    return {"message": "Strategy deleted successfully"}
