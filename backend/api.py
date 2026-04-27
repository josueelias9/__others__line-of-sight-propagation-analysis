import os
import sys

_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from infrastructure.persistence.csv_punto_repository import CsvPuntoRepository

app = FastAPI(title="Line of Sight API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

_IN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "in") + "/"
_repo = CsvPuntoRepository(_IN_DIR)


class PuntoOut(BaseModel):
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
