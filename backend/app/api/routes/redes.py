from typing import List

from fastapi import APIRouter

from app.core import config
from app.api.deps import CurrentUserIdDep

from infrastructure.persistence.database import SessionDep
from infrastructure.persistence.pg_punto_repository import PgPuntoRepository
from infrastructure.persistence.pg_red_repository import PgRedRepository
from infrastructure.elevation.srtm_elevation_repository import SrtmElevationRepository
from infrastructure.output.kml_writer import KmlWriter
from application.use_cases.encontrar_relaciones import (
    EncontrarRelacionesUseCase,
    EncontrarRelacionesArbolRequest,
)
from application.use_cases.listar_redes import ListarRedesUseCase

from infrastructure.geometry.shapely_geometry_repository import (
    ShapelyGeometryRepository,
)

from app.models import (
    RedOut,
    RelacionRedOut,
    PuntoSinConexionOut,
    ArbolRequest,
    ArbolResponse,
)

router = APIRouter()


@router.get("", response_model=List[RedOut])
def get_redes(session: SessionDep, user_id: CurrentUserIdDep):
    use_case = ListarRedesUseCase(red_repo=PgRedRepository(session, user_id=user_id))
    redes = use_case.ejecutar()
    return [
        RedOut(
            id=r.id,
            nombre=r.nombre,
            geojson=r.geojson or {"type": "MultiLineString", "coordinates": []},
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
def delete_red(red_id: int, session: SessionDep, user_id: CurrentUserIdDep):
    repo = PgRedRepository(session, user_id=user_id)
    repo.eliminar_red(red_id)


# ==================


@router.post("", response_model=ArbolResponse)
def post_arbol(body: ArbolRequest, session: SessionDep, user_id: CurrentUserIdDep):
    import os

    os.makedirs(config.DIR_OUTPUT, exist_ok=True)

    repo = PgPuntoRepository(session, user_id=user_id)
    red_repo = PgRedRepository(session, user_id=user_id)
    elevation_repo = SrtmElevationRepository(body.muestras)
    kml_output = KmlWriter(directorio=config.DIR_OUTPUT)

    use_case = EncontrarRelacionesUseCase(
        punto_repo=repo,
        elevation_repo=elevation_repo,
        kml_output=kml_output,
        muestras=body.muestras,
        red_repo=red_repo,
        geometry_gateway=ShapelyGeometryRepository(),
    )

    result = use_case.ejecutar_dos_archivos_arbol(
        EncontrarRelacionesArbolRequest(
            tipo_conectados=body.tipo_conectados,
            tipo_no_conectados=body.tipo_no_conectados,
            distancia_maxima=body.distancia_maxima,
            nombre_red=body.nombre_red,
        )
    )

    return ArbolResponse(
        red_geojson=result.red_geojson
        or {"type": "MultiLineString", "coordinates": []},
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
