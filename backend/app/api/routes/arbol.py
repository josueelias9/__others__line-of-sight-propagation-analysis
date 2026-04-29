from pydantic import BaseModel
from typing import List

from fastapi import APIRouter

from app.core import config
from infrastructure.persistence.database import SessionDep
from infrastructure.persistence.pg_punto_repository import PgPuntoRepository
from infrastructure.elevation.srtm_elevation_repository import SrtmElevationRepository
from infrastructure.output.kml_writer import KmlWriter
from application.use_cases.encontrar_relaciones import (
    EncontrarRelacionesUseCase,
    EncontrarRelacionesArbolRequest,
)

router = APIRouter()


class ArbolRequest(BaseModel):
    tipo_conectados: str
    tipo_no_conectados: str
    distancia_maxima: float = config.DISTANCIA_KM
    muestras: int = config.MUESTRAS


class RelacionArbolOut(BaseModel):
    punto_inicial: str
    punto_final: str
    distancia: float


class PuntoSinConexionOut(BaseModel):
    ubigeo: int
    nombre: str
    longitud: float
    latitud: float
    tipo: str


class ArbolResponse(BaseModel):
    relaciones_exitosas: List[RelacionArbolOut]
    puntos_sin_conexion: List[PuntoSinConexionOut]


@router.post("", response_model=ArbolResponse)
def post_arbol(body: ArbolRequest, session: SessionDep):
    import os
    os.makedirs(config.DIR_OUTPUT, exist_ok=True)

    repo = PgPuntoRepository(session)
    elevation_repo = SrtmElevationRepository(body.muestras)
    kml_output = KmlWriter(directorio=config.DIR_OUTPUT)

    use_case = EncontrarRelacionesUseCase(
        punto_repo=repo,
        elevation_repo=elevation_repo,
        kml_output=kml_output,
        muestras=body.muestras,
    )

    result = use_case.ejecutar_dos_archivos_arbol(
        EncontrarRelacionesArbolRequest(
            tipo_conectados=body.tipo_conectados,
            tipo_no_conectados=body.tipo_no_conectados,
            distancia_maxima=body.distancia_maxima,
        )
    )

    return ArbolResponse(
        relaciones_exitosas=[
            RelacionArbolOut(
                punto_inicial=r.punto_inicial.nombre,
                punto_final=r.punto_final.nombre,
                distancia=r.distancia,
            )
            for r in result.relaciones_exitosas
        ],
        puntos_sin_conexion=[
            PuntoSinConexionOut(
                ubigeo=p.ubigeo,
                nombre=p.nombre,
                longitud=p.longitud,
                latitud=p.latitud,
                tipo=p.tipo,
            )
            for p in result.puntos_sin_conexion
        ],
    )
