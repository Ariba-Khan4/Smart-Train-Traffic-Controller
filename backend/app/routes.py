from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services import predict_train_delay, suggest_reroute
from app.utils import log_request
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class DelayPredictionRequest(BaseModel):
    train_id: str
    current_time: str
    station: str
    weather_condition: Optional[str] = "clear"
    day_of_week: Optional[int] = 1

class DelayPredictionResponse(BaseModel):
    train_id: str
    delay_probability: float
    predicted_delay_minutes: int
    risk_level: str
    factors: List[str]

class RerouteRequest(BaseModel):
    delayed_train_id: str
    current_station: str
    destination_station: str
    delay_minutes: int
    available_routes: Optional[List[str]] = []

class RerouteResponse(BaseModel):
    delayed_train_id: str
    recommended_action: str
    alternative_trains: List[dict]
    reroute_path: List[str]
    estimated_recovery_time: int
    confidence_score: float

@router.post("/predict_delay", response_model=DelayPredictionResponse)
async def predict_delay(request: DelayPredictionRequest):
    """
    Predict train delay probability based on current conditions
    """
    try:
        log_request("predict_delay", request.dict())
        result = predict_train_delay(
            train_id=request.train_id,
            current_time=request.current_time,
            station=request.station,
            weather=request.weather_condition,
            day_of_week=request.day_of_week
        )
        return result
    except Exception as e:
        logger.error(f"Error in predict_delay: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reroute", response_model=RerouteResponse)
async def reroute_train(request: RerouteRequest):
    """
    Suggest optimal rerouting for delayed trains
    """
    try:
        log_request("reroute", request.dict())
        result = suggest_reroute(
            delayed_train_id=request.delayed_train_id,
            current_station=request.current_station,
            destination_station=request.destination_station,
            delay_minutes=request.delay_minutes,
            available_routes=request.available_routes
        )
        return result
    except Exception as e:
        logger.error(f"Error in reroute: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trains")
async def get_all_trains():
    """
    Get all active trains in the system
    """
    from app.utils import load_sample_data
    try:
        data = load_sample_data()
        return {"trains": data.to_dict('records')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
