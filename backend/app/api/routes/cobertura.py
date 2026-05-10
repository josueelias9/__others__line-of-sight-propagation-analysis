from dataclasses import asdict
from typing import List

from fastapi import APIRouter, HTTPException

from app.core import config
from app.api.deps import CurrentUserIdDep
from infrastructure.persistence.database import SessionDep
from infrastructure.persistence.pg_cobertura_guardada_repository import (
    PgCoberturaGuardadaRepository,
)
from infrastructure.persistence.pg_punto_repository import PgPuntoRepository
from infrastructure.elevation.srtm_elevation_repository import SrtmElevationRepository
from infrastructure.geometry.shapely_geometry_repository import (
    ShapelyGeometryRepository,
)
from interface.presenters.cobertura_presenter import GenerarPoligonoCoberturaPresenter
from application.use_cases.generar_poligono_cobertura import (
    GenerarPoligonoCoberturaUseCase,
    GenerarPoligonoCoberturaRequest,
)
from application.use_cases.listar_coberturas import (
    ListarCoberturasUseCase,
    ListarCoberturasRequest,
)


from app.models import CoberturaGuardadaOut, CoberturaRequest

router = APIRouter()


@router.post("")
def post_cobertura(
    body: CoberturaRequest, session: SessionDep, user_id: CurrentUserIdDep
):
    distancia_grados = config.de_km_a_grados(body.distancia_km)
    cobertura_repo = PgCoberturaGuardadaRepository(session, user_id=user_id)
    presenter = GenerarPoligonoCoberturaPresenter()

    use_case = GenerarPoligonoCoberturaUseCase(
        elevation_repo=SrtmElevationRepository(body.muestras),
        punto_repo=PgPuntoRepository(session, user_id=user_id),
        geometry_gateway=ShapelyGeometryRepository(),
        output_boundary=presenter,
        numero_de_ldv=body.numero_de_ldv,
        muestras=body.muestras,
        distancia_grados=distancia_grados,
        altura_torre_fantasma=body.altura_torre_fantasma,
        cobertura_repo=cobertura_repo,
    )

    try:
        view_model = use_case.ejecutar(
            GenerarPoligonoCoberturaRequest(ubigeo=body.ubigeo)
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return asdict(view_model)


@router.get("", response_model=List[CoberturaGuardadaOut])
def get_coberturas(session: SessionDep, user_id: CurrentUserIdDep):
    use_case = ListarCoberturasUseCase(
        repo=PgCoberturaGuardadaRepository(session, user_id=user_id)
    )
    items = use_case.ejecutar(ListarCoberturasRequest())
    return [
        CoberturaGuardadaOut(
            id=c.id,
            punto_ubigeo=c.punto_ubigeo,
            punto_nombre=c.punto_nombre,
            geojson=c.geojson,
            numero_de_ldv=c.numero_de_ldv,
            muestras=c.muestras,
            distancia_km=c.distancia_km,
            altura_torre_fantasma=c.altura_torre_fantasma,
        )
        for c in items
    ]


@router.delete("/{id}", status_code=204)
def delete_cobertura(id: int, session: SessionDep, user_id: CurrentUserIdDep):
    repo = PgCoberturaGuardadaRepository(session, user_id=user_id)
    try:
        repo.eliminar(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
