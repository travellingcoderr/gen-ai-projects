from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.jsonplaceholder import router as jsonplaceholder_router
from app.api.routes.llm import router as llm_router
from app.api.routes.search import router as search_router
from app.api.routes.travel import router as travel_router
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers

app = FastAPI(title="mcp-travel-agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(search_router, prefix="/api/test/wiki_search", tags=["wiki_search"])
app.include_router(jsonplaceholder_router, prefix="/api/test/jsonplaceholder", tags=["jsonplaceholder"])
app.include_router(llm_router, prefix="/api/llm", tags=["llm"])
app.include_router(travel_router, prefix="/api/travel", tags=["travel"])
