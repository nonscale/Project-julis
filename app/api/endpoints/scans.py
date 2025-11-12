from fastapi import APIRouter, HTTPException
from app.core.engine import ScanEngine
from app.core.brokers.upbit import UpbitBroker

router = APIRouter()
upbit_broker = UpbitBroker()
scan_engine = ScanEngine(broker=upbit_broker)

@router.post("/{strategy_id}/run", response_model=dict)
async def run_scan(strategy_id: int):
    try:
        results_df = scan_engine.run_primary_scan(market="KRW")
        results_json = results_df.to_dicts()
        return {
            "message": f"Strategy {strategy_id} scan completed.",
            "result_count": len(results_json),
            "results": results_json
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{strategy_id}/stop", response_model=dict)
async def stop_scan(strategy_id: int):
    return {"message": f"Stop command received for strategy {strategy_id}."}