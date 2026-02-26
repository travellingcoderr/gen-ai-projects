from fastapi import APIRouter, Depends

from app.api.schemas.langgraph import LangGraphSupportRequest, LangGraphSupportResponse
from app.core.deps import get_langgraph_orchestrator
from app.orchestration.langgraph_orchestrator import LangGraphOrchestrator

router = APIRouter()


@router.post("/support", response_model=LangGraphSupportResponse)
def process_support_message(
    payload: LangGraphSupportRequest,
    orchestrator: LangGraphOrchestrator = Depends(get_langgraph_orchestrator),
) -> LangGraphSupportResponse:
    return orchestrator.process_support_message(payload.query)
