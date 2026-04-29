from dataclasses import asdict
from typing import Any, Dict, List

from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException

from app.core import config
from infrastructure.persistence.database import SessionDep
from infrastructure.persistence.pg_cobertura_guardada_repository import PgCoberturaGuardadaRepository
from infrastructure.persistence.pg_punto_repository import PgPuntoRepository
from infrastructure.elevation.srtm_elevation_repository import SrtmElevationRepository
from infrastructure.geometry.shapely_geometry_repository import ShapelyGeometryRepository
from interface.presenters.cobertura_presenter import GenerarPoligonoCoberturaPresenter
from application.use_cases.generar_poligono_cobertura import (
    GenerarPoligonoCoberturaUseCase,
    GenerarPoligonoCoberturaRequest,
)
from application.use_cases.listar_coberturas import (
    ListarCoberturasUseCase,
    ListarCoberturasRequest,
)

router = APIRouter()


class CoberturaRequest(BaseModel):
    ubigeo: int
    numero_de_ldv: int = Field(default=config.NUMERO_DE_LDV, ge=100, le=300)
    muestras: int = Field(default=config.MUESTRAS, ge=100, le=300)
    distancia_km: float = Field(default=config.DISTANCIA_KM, ge=1, le=15)
    altura_torre_fantasma: float = Field(default=config.ALTURA_TORRE_FANTASMA, ge=5, le=20)


class CoberturaGuardadaOut(BaseModel):
    id: int
    punto_ubigeo: int
    punto_nombre: str
    geojson: Dict[str, Any]
    numero_de_ldv: int
    muestras: int
    distancia_km: float
    altura_torre_fantasma: float


@router.post("")
def post_cobertura(body: CoberturaRequest, session: SessionDep):
    distancia_grados = config.de_km_a_grados(body.distancia_km)
    cobertura_repo = PgCoberturaGuardadaRepository(session)
    presenter = GenerarPoligonoCoberturaPresenter()

    use_case = GenerarPoligonoCoberturaUseCase(
        elevation_repo=SrtmElevationRepository(body.muestras),
        punto_repo=PgPuntoRepository(session),
        geometry_gateway=ShapelyGeometryRepository(),
        output_boundary=presenter,
        numero_de_ldv=body.numero_de_ldv,
        muestras=body.muestras,
        distancia_grados=distancia_grados,
        altura_torre_fantasma=body.altura_torre_fantasma,
        cobertura_repo=cobertura_repo,
    )

    try:
        view_model = use_case.ejecutar(GenerarPoligonoCoberturaRequest(ubigeo=body.ubigeo))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return asdict(view_model)


@router.get("", response_model=List[CoberturaGuardadaOut])
def get_coberturas(session: SessionDep):
    use_case = ListarCoberturasUseCase(repo=PgCoberturaGuardadaRepository(session))
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
def delete_cobertura(id: int, session: SessionDep):
    repo = PgCoberturaGuardadaRepository(session)
    try:
        repo.eliminar(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
