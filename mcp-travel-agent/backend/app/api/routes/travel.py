from fastapi import APIRouter, Depends

from app.api.schemas.travel import TravelPlanRequest, TravelPlanResponse
from app.core.deps import get_travel_orchestrator
from app.orchestration.travel_orchestrator import TravelOrchestrator

router = APIRouter()


@router.post("/plan", response_model=TravelPlanResponse)
def plan_trip(
    payload: TravelPlanRequest,
    orchestrator: TravelOrchestrator = Depends(get_travel_orchestrator),
) -> TravelPlanResponse:
    return orchestrator.plan_trip(payload)
