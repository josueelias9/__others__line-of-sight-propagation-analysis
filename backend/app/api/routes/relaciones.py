from pydantic import BaseModel
from typing import List

from fastapi import APIRouter
from app.core import config
from infrastructure.persistence.csv_punto_repository import CsvPuntoRepository

router = APIRouter()

_repo = CsvPuntoRepository(config.DIR_INPUT)


class RelacionOut(BaseModel):
    punto_inicial: str
    punto_final: str
    distancia: float


@router.get("", response_model=List[RelacionOut])
def get_relaciones():
    return [
        RelacionOut(
            punto_inicial=r.punto_inicial.nombre,
            punto_final=r.punto_final.nombre,
            distancia=r.distancia,
        )
        for r in _repo.leer_relaciones()
    ]
