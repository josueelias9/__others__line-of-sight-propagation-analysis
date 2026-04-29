from pydantic import BaseModel
from typing import List

from fastapi import APIRouter
from infrastructure.persistence.database import SessionDep
from infrastructure.persistence.pg_punto_repository import PgPuntoRepository

router = APIRouter()


class RelacionOut(BaseModel):
    punto_inicial: str
    punto_final: str
    distancia: float


@router.get("", response_model=List[RelacionOut])
def get_relaciones(session: SessionDep):
    repo = PgPuntoRepository(session)
    return [
        RelacionOut(
            punto_inicial=r.punto_inicial.nombre,
            punto_final=r.punto_final.nombre,
            distancia=r.distancia,
        )
        for r in repo.leer_relaciones()
    ]
