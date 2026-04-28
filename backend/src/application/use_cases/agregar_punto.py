from __future__ import annotations

from dataclasses import dataclass

from domain.entities.punto import Punto
from application.gateways.punto_gateway import PuntoGateway


@dataclass
class AgregarPuntoRequest:
    nombre: str
    longitud: float
    latitud: float
    altura_antena: float
    tipo: str
    green_asociado: str = ""


@dataclass
class AgregarPuntoResponse:
    punto: Punto


class AgregarPuntoUseCase:
    """
    Caso de uso: agregar un nuevo Punto a la red.

    Pertenece a la capa de Aplicación.
    """

    def __init__(self, punto_repo: PuntoGateway) -> None:
        self._punto_repo = punto_repo

    def ejecutar(self, request: AgregarPuntoRequest) -> AgregarPuntoResponse:
        nuevo = Punto(
            nombre=request.nombre,
            ubigeo=0,  # será asignado por el repositorio
            longitud=request.longitud,
            latitud=request.latitud,
            altura_antena=request.altura_antena,
            tipo=request.tipo,
            metros_sobre_nivel_mar=0.0,
        )
        nuevo.green_asociado = request.green_asociado
        nuevo.conectado = False

        guardado = self._punto_repo.agregar_punto(nuevo)
        return AgregarPuntoResponse(punto=guardado)
