from pydantic import BaseModel, ConfigDict
from typing import Optional
import datetime

class StrategyBase(BaseModel):
    """
    전략의 기본 필드를 정의하는 Pydantic 모델입니다.
    """
    name: str
    description: Optional[str] = None

class StrategyCreate(StrategyBase):
    """
    새로운 전략을 생성할 때 사용되는 모델입니다.
    """
    pass

class Strategy(StrategyBase):
    """
    데이터베이스에서 조회하거나 API 응답으로 사용될 완전한 전략 모델입니다.
    """
    id: int
    created_at: datetime.datetime

    # Pydantic V2 스타일의 모델 설정
    model_config = ConfigDict(from_attributes=True)
