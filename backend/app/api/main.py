from fastapi import APIRouter, Depends

from app.api.deps import get_current_active_user
from app.api.routes.login import router as login_router
from app.api.routes.puntos import router as puntos_router
from app.api.routes.cobertura import router as cobertura_router
from app.api.routes.redes import router as redes_router

api_router = APIRouter()

# Public routes — no authentication required
api_router.include_router(login_router, prefix="/login")

# Protected routes — valid JWT required for all endpoints
_protected = APIRouter(dependencies=[Depends(get_current_active_user)])
_protected.include_router(puntos_router, prefix="/puntos", tags=["puntos"])
_protected.include_router(cobertura_router, prefix="/cobertura", tags=["cobertura"])
_protected.include_router(redes_router, prefix="/redes", tags=["redes"])

api_router.include_router(_protected)
