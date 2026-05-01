from typing import Any, Dict, List

from pydantic import BaseModel
from fastapi import APIRouter
from shapely.geometry import LineString, MultiLineString, mapping

from app.core import config

from infrastructure.persistence.database import SessionDep
from infrastructure.persistence.pg_punto_repository import PgPuntoRepository
from infrastructure.persistence.pg_red_repository import PgRedRepository
from infrastructure.elevation.srtm_elevation_repository import SrtmElevationRepository
from infrastructure.output.kml_writer import KmlWriter
from application.use_cases.encontrar_relaciones import (
    EncontrarRelacionesUseCase,
    EncontrarRelacionesArbolRequest,
)



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

# ==================


class ArbolRequest(BaseModel):
    tipo_conectados: str
    tipo_no_conectados: str
    distancia_maxima: float = config.DISTANCIA_KM
    muestras: int = config.MUESTRAS
    nombre_red: str = ""


class PuntoSinConexionOut(BaseModel):
    ubigeo: int
    nombre: str
    longitud: float
    latitud: float
    tipo: str


class ArbolResponse(BaseModel):
    red_geojson: Dict[str, Any]
    puntos_sin_conexion: List[PuntoSinConexionOut]




@router.post("", response_model=ArbolResponse)
def post_arbol(body: ArbolRequest, session: SessionDep):
    import os
    os.makedirs(config.DIR_OUTPUT, exist_ok=True)

    repo = PgPuntoRepository(session)
    red_repo = PgRedRepository(session)
    elevation_repo = SrtmElevationRepository(body.muestras)
    kml_output = KmlWriter(directorio=config.DIR_OUTPUT)

    use_case = EncontrarRelacionesUseCase(
        punto_repo=repo,
        elevation_repo=elevation_repo,
        kml_output=kml_output,
        muestras=body.muestras,
        red_repo=red_repo,
    )

    result = use_case.ejecutar_dos_archivos_arbol(
        EncontrarRelacionesArbolRequest(
            tipo_conectados=body.tipo_conectados,
            tipo_no_conectados=body.tipo_no_conectados,
            distancia_maxima=body.distancia_maxima,
            nombre_red=body.nombre_red,
        )
    )

    lines = [
        LineString([
            (r.punto_inicial.longitud, r.punto_inicial.latitud),
            (r.punto_final.longitud, r.punto_final.latitud),
        ])
        for r in result.relaciones_exitosas
    ]
    red_geojson = dict(mapping(MultiLineString(lines))) if lines else {"type": "MultiLineString", "coordinates": []}

    return ArbolResponse(
        red_geojson=red_geojson,
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
