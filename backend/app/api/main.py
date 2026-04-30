from fastapi import APIRouter

from app.api.routes.puntos import router as puntos_router
from app.api.routes.cobertura import router as cobertura_router
from app.api.routes.arbol import router as arbol_router
from app.api.routes.redes import router as redes_router

api_router = APIRouter()

api_router.include_router(puntos_router, prefix="/puntos", tags=["puntos"])
api_router.include_router(cobertura_router, prefix="/cobertura", tags=["cobertura"])
api_router.include_router(arbol_router, prefix="/arbol", tags=["arbol"])
api_router.include_router(redes_router, prefix="/redes", tags=["redes"])
