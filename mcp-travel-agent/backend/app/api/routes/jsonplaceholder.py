from fastapi import APIRouter, Depends

from app.core.deps import get_jsonplaceholder_orchestrator
from app.orchestration.jsonplaceholder_orchestrator import JsonPlaceholderOrchestrator

router = APIRouter()


@router.get("/posts")
def list_posts(
    orchestrator: JsonPlaceholderOrchestrator = Depends(get_jsonplaceholder_orchestrator),
) -> list[dict]:
    return orchestrator.list_posts()
