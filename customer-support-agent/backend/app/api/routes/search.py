from fastapi import APIRouter, Depends, Query

from app.api.schemas.search import SearchResponse
from app.core.deps import get_search_orchestrator
from app.orchestration.search_orchestrator import SearchOrchestrator

router = APIRouter()


@router.get("", response_model=SearchResponse)
def search(
    q: str = Query(..., min_length=2),
    orchestrator: SearchOrchestrator = Depends(get_search_orchestrator),
) -> SearchResponse:
    return orchestrator.search(q)
