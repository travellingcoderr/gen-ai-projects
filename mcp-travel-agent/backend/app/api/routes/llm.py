from fastapi import APIRouter, Depends

from app.api.schemas.llm import LLMConfigResponse
from app.core.deps import get_llm_orchestrator
from app.orchestration.llm_orchestrator import LLMOrchestrator

router = APIRouter()


@router.get("/config", response_model=LLMConfigResponse)
def llm_config(orchestrator: LLMOrchestrator = Depends(get_llm_orchestrator)) -> LLMConfigResponse:
    return orchestrator.config()
