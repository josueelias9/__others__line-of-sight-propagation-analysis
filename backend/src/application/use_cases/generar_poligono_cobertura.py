from __future__ import annotations

from dataclasses import dataclass, field
import logging
from typing import Any, Protocol

from domain.entities.estructura import Estructura
from domain.entities.poligonos import Poligonos
from domain.entities.punto import Punto
from application.gateways.elevation_gateway import ElevationGateway

logger = logging.getLogger(__name__)

@dataclass
class GenerarPoligonoCoberturaRequest:
    punto: Punto


@dataclass
class GenerarPoligonoCoberturaResponse:
    poligono: Poligonos
    estructura: Estructura


class CoberturaOutputBoundary(Protocol):
    """
    Puerto de salida del caso de uso GenerarPoligonoCoberturaUseCase.

    Cualquier adaptador (presenter, passtrhrought, etc.) que implemente
    `presentar()` satisface este protocolo estructuralmente.

    Pertenece a la capa de Aplicación.
    """

    def presentar(self, response: GenerarPoligonoCoberturaResponse) -> Any:
        ...


class GenerarPoligonoCoberturaUseCase:
    """
    Caso de uso: generar el polígono de cobertura de un punto dado.

    1. Construye la Estructura (grilla polar).
    2. Llena la matriz de LOS consultando el repositorio de elevación.
    3. Ejecuta el algoritmo de análisis de polígonos (dominio).
    4. Convierte el resultado a un Polygon de Shapely.
    5. Opcionalmente escribe el KML de salida.

    Pertenece a la capa de Aplicación.
    """

    def __init__(
        self,
        elevation_repo: ElevationGateway,
        output_boundary: CoberturaOutputBoundary,
        numero_de_ldv: int,
        muestras: int,
        distancia_grados: float,
        altura_torre_fantasma: float,
    ) -> None:
        self._elevation_repo = elevation_repo
        self._output_boundary = output_boundary
        self._numero_de_ldv = numero_de_ldv
        self._muestras = muestras
        self._distancia_grados = distancia_grados
        self._altura_torre_fantasma = altura_torre_fantasma

    def ejecutar(self, request: GenerarPoligonoCoberturaRequest) -> Any:
        """Calcula el polígono de cobertura y delega la presentación al output boundary."""
        logger.info("🟢")
        estructura = Estructura(
            n=self._numero_de_ldv,
            m=self._muestras,
            r=self._distancia_grados,
            punto_cero=request.punto,
            altura_torre_fantasma=self._altura_torre_fantasma,
        )

        self._llenar_matriz_los(estructura)

        poligonos = estructura.extraer_poligonos()
        logger.debug(f"Polígonos extraídos: {len(poligonos.lista_de_poligonitos)}")

        response = GenerarPoligonoCoberturaResponse(poligono=poligonos, estructura=estructura)
        logger.info("🔴")
        return self._output_boundary.presentar(response)

    # ------------------------------------------------------------------ privado

    def _llenar_matriz_los(self, estructura: Estructura) -> None:
        """
        Rellena estructura.estructura_matricial consultando la elevación
        real del terreno entre el punto central y cada punto de la grilla.
        """
        for i in range(estructura.n):
            punto_extremo = estructura.estructura_linea_de_vista[i][estructura.m - 1]
            alturas, _ = self._elevation_repo.obtener_perfil_de_alturas(
                estructura.punto_cero, punto_extremo, estructura.m
            )

            for j in range(estructura.m):
                y_0 = alturas[0] + estructura.punto_cero.altura_antena
                y_f = alturas[j] + estructura.altura_torre_fantasma
                x_f = float(j)

                for k in range(j):
                    x_k = float(k)
                    y_k = (y_f - y_0) / x_f * x_k + y_0 if x_f != 0 else y_0
                    if y_k < alturas[k]:
                        estructura.estructura_matricial[i][j] = 0
                        break

        # la columna 0 (el propio punto central) no tiene cobertura
        for i in range(estructura.n):
            estructura.estructura_matricial[i][0] = 0
