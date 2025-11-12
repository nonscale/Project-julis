from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import strategies, scans

app = FastAPI(title="Trading Bot API", version="0.1.0")
origins = ["http://localhost", "http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok"}
app.include_router(strategies.router, prefix="/api/v1/strategies", tags=["Strategies"])
app.include_router(scans.router, prefix="/api/v1/scans", tags=["Scans"])
@app.get("/", tags=["System"])
async def read_root():
    return {"message": "Welcome to the Trading Bot API"}