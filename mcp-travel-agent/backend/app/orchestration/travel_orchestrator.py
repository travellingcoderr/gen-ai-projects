from app.api.schemas.travel import TravelPlanRequest, TravelPlanResponse
from app.services.travel.travel_workflow_service import TravelWorkflowService


class TravelOrchestrator:
    def __init__(self, service: TravelWorkflowService) -> None:
        self.service = service

    def plan_trip(self, request: TravelPlanRequest) -> TravelPlanResponse:
        data = self.service.plan(request)
        return TravelPlanResponse(**data)
