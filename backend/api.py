import os
import sys
from dataclasses import asdict

_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

import config
from infrastructure.persistence.csv_punto_repository import CsvPuntoRepository
from infrastructure.elevation.srtm_elevation_repository import SrtmElevationRepository
from interface.presenters.cobertura_presenter import GenerarPoligonoCoberturaPresenter
from application.use_cases.generar_poligono_cobertura import (
    GenerarPoligonoCoberturaUseCase,
    GenerarPoligonoCoberturaRequest,
)

app = FastAPI(title="Line of Sight API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_IN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "in") + "/"
_repo = CsvPuntoRepository(_IN_DIR)


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


class RelacionOut(BaseModel):
    punto_inicial: str
    punto_final: str
    distancia: float


@app.get("/api/puntos", response_model=List[PuntoOut])
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


@app.get("/api/relaciones", response_model=List[RelacionOut])
def get_relaciones():
    return [
        RelacionOut(
            punto_inicial=r.punto_inicial.nombre,
            punto_final=r.punto_final.nombre,
            distancia=r.distancia,
        )
        for r in _repo.leer_relaciones()
    ]


# ─── Cobertura ─────────────────────────────────────────────────────────────────

class CoberturaRequest(BaseModel):
    ubigeo: int
    numero_de_ldv: int = config.NUMERO_DE_LDV
    muestras: int = config.MUESTRAS
    distancia_km: float = config.DISTANCIA_KM
    altura_torre_fantasma: float = config.ALTURA_TORRE_FANTASMA


@app.post("/api/cobertura")
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
