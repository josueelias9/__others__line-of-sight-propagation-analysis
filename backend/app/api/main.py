from fastapi import APIRouter

from app.api.routes.puntos import router as puntos_router
from app.api.routes.relaciones import router as relaciones_router
from app.api.routes.cobertura import router as cobertura_router

api_router = APIRouter()

api_router.include_router(puntos_router, prefix="/puntos", tags=["puntos"])
api_router.include_router(relaciones_router, prefix="/relaciones", tags=["relaciones"])
api_router.include_router(cobertura_router, prefix="/cobertura", tags=["cobertura"])
