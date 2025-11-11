from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# FastAPI 앱 인스턴스 생성
app = FastAPI(
    title="Trading Bot API",
    description="지능형 자동매매 플랫폼을 위한 API",
    version="0.1.0",
)

# 8.3. 프론트엔드 및 API 연동 지침에 따른 CORS 미들웨어 설정
# 개발 중인 프론트엔드(보통 localhost:5173)에서 오는 요청을 허용하기 위함
origins = [
    "http://localhost",
    "http://localhost:5173",  # Vite 기본 개발 서버 포트
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)


# Phase 1 요구사항: Health-Check API 구현
@app.get("/health", tags=["System"])
async def health_check():
    """
    서버가 정상적으로 실행 중인지 확인합니다.
    """
    return {"status": "ok"}


# API 라우터 포함
# app/api/endpoints/strategies.py 에서 정의한 라우터를 가져옵니다.
from app.api.endpoints import strategies

# "/api/v1/strategies" 접두사를 가진 API 엔드포인트들을 앱에 포함시킵니다.
app.include_router(strategies.router, prefix="/api/v1/strategies", tags=["Strategies"])


# 기본 루트 엔드포인트
@app.get("/", tags=["System"])
async def read_root():
    """
    API의 시작점을 알리는 간단한 환영 메시지를 반환합니다.
    """
    return {"message": "Welcome to the Trading Bot API"}
