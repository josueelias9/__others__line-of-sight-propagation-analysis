from pydantic import BaseModel
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from app.core import config
from infrastructure.persistence.database import SessionDep
from infrastructure.persistence.pg_punto_repository import PgPuntoRepository
from infrastructure.elevation.srtm_elevation_repository import SrtmElevationRepository
from application.use_cases.agregar_punto import AgregarPuntoUseCase, AgregarPuntoRequest
from application.use_cases.asignar_alturas import AsignarAlturasUseCase

router = APIRouter()


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
def get_puntos(session: SessionDep, tipo: Optional[str] = Query(None)):
    repo = PgPuntoRepository(session)
    puntos = repo.leer_puntos_por_tipo(tipo) if tipo else repo.leer_puntos()
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
        for p in puntos
    ]


@router.post("", response_model=PuntoOut, status_code=201)
def post_punto(body: PuntoIn, session: SessionDep):
    repo = PgPuntoRepository(session)
    use_case = AgregarPuntoUseCase(punto_repo=repo)
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


@router.post("/alturas", response_model=List[PuntoOut])
def post_alturas(session: SessionDep):
    repo = PgPuntoRepository(session)
    elevation_repo = SrtmElevationRepository(muestras=config.MUESTRAS)
    use_case = AsignarAlturasUseCase(punto_repo=repo, elevation_repo=elevation_repo)
    response = use_case.ejecutar()
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
        for p in response.puntos
    ]
