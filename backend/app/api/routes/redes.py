from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from infrastructure.persistence.database import SessionDep
from infrastructure.persistence.pg_red_repository import PgRedRepository

router = APIRouter()


class RelacionRedOut(BaseModel):
    punto_inicial_ubigeo: int
    punto_final_ubigeo: int
    distancia: float


class RedOut(BaseModel):
    id: int
    nombre: str
    relaciones: List[RelacionRedOut]


@router.get("", response_model=List[RedOut])
def get_redes(session: SessionDep):
    repo = PgRedRepository(session)
    redes = repo.listar_redes()
    return [
        RedOut(
            id=r.id,
            nombre=r.nombre,
            relaciones=[
                RelacionRedOut(
                    punto_inicial_ubigeo=rel.punto_inicial.ubigeo,
                    punto_final_ubigeo=rel.punto_final.ubigeo,
                    distancia=rel.distancia,
                )
                for rel in r.lista_de_relaciones
            ],
        )
        for r in redes
    ]


@router.delete("/{red_id}", status_code=204)
def delete_red(red_id: int, session: SessionDep):
    repo = PgRedRepository(session)
    repo.eliminar_red(red_id)
