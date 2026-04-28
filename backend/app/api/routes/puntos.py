from pydantic import BaseModel
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from app.core import config
from infrastructure.persistence.csv_punto_repository import CsvPuntoRepository
from application.use_cases.agregar_punto import AgregarPuntoUseCase, AgregarPuntoRequest

router = APIRouter()

_repo = CsvPuntoRepository(config.DIR_INPUT)


class PuntoOut(BaseModel):
    ubigeo: int
    nombre: str
    longitud: float
    latitud: float
    altura_antena: float
    tipo: str
    metros_sobre_nivel_mar: float
    green_asociado: str
    conectado: bool


class PuntoIn(BaseModel):
    nombre: str
    longitud: float
    latitud: float
    altura_antena: float = 15.0
    tipo: str
    green_asociado: Optional[str] = ""


@router.get("", response_model=List[PuntoOut])
def get_puntos():
    return [
        PuntoOut(
            ubigeo=p.ubigeo,
            nombre=p.nombre,
            longitud=p.longitud,
            latitud=p.latitud,
            altura_antena=p.altura_antena,
            tipo=p.tipo,
            metros_sobre_nivel_mar=p.metros_sobre_nivel_mar,
            green_asociado=p.green_asociado,
            conectado=p.conectado,
        )
        for p in _repo.leer_puntos()
    ]


@router.post("", response_model=PuntoOut, status_code=201)
def post_punto(body: PuntoIn):
    use_case = AgregarPuntoUseCase(punto_repo=_repo)
    response = use_case.ejecutar(
        AgregarPuntoRequest(
            nombre=body.nombre,
            longitud=body.longitud,
            latitud=body.latitud,
            altura_antena=body.altura_antena,
            tipo=body.tipo,
            green_asociado=body.green_asociado or "",
        )
    )
    p = response.punto
    return PuntoOut(
        ubigeo=p.ubigeo,
        nombre=p.nombre,
        longitud=p.longitud,
        latitud=p.latitud,
        altura_antena=p.altura_antena,
        tipo=p.tipo,
        metros_sobre_nivel_mar=p.metros_sobre_nivel_mar,
        green_asociado=p.green_asociado,
        conectado=p.conectado,
    )
