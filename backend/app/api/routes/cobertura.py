from dataclasses import asdict

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from app.core import config
from infrastructure.persistence.csv_punto_repository import CsvPuntoRepository
from infrastructure.elevation.srtm_elevation_repository import SrtmElevationRepository
from interface.presenters.cobertura_presenter import GenerarPoligonoCoberturaPresenter
from application.use_cases.generar_poligono_cobertura import (
    GenerarPoligonoCoberturaUseCase,
    GenerarPoligonoCoberturaRequest,
)

router = APIRouter()

_repo = CsvPuntoRepository(config.DIR_INPUT)


class CoberturaRequest(BaseModel):
    ubigeo: int
    numero_de_ldv: int = config.NUMERO_DE_LDV
    muestras: int = config.MUESTRAS
    distancia_km: float = config.DISTANCIA_KM
    altura_torre_fantasma: float = config.ALTURA_TORRE_FANTASMA


@router.post("")
def post_cobertura(body: CoberturaRequest):
    distancia_grados = config.de_km_a_grados(body.distancia_km)
    elevation_repo = SrtmElevationRepository(body.muestras)
    presenter = GenerarPoligonoCoberturaPresenter()

    use_case = GenerarPoligonoCoberturaUseCase(
        elevation_repo=elevation_repo,
        punto_repo=_repo,
        output_boundary=presenter,
        numero_de_ldv=body.numero_de_ldv,
        muestras=body.muestras,
        distancia_grados=distancia_grados,
        altura_torre_fantasma=body.altura_torre_fantasma,
    )

    try:
        view_model = use_case.ejecutar(GenerarPoligonoCoberturaRequest(ubigeo=body.ubigeo))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return asdict(view_model)
