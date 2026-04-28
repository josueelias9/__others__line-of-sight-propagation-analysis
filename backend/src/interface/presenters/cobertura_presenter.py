"""
Presenter para GenerarPoligonoCoberturaUseCase.

Transforma GenerarPoligonoCoberturaResponse en un CoberturaViewModel
agnóstico del destino de salida:
  - CLI/script : se pasa a KmlWriter.escribir_cobertura() para generar archivos.
  - FastAPI    : se serializa directamente como JSON en el endpoint.

Implementa CoberturaOutputBoundary (protocolo de la capa de Aplicación),
por lo que puede inyectarse directamente en el caso de uso.

Pertenece a la capa de Interfaz.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from application.ports.output_port import CoberturaOutputBoundary
from application.use_cases.generar_poligono_cobertura import (
    GenerarPoligonoCoberturaResponse,
)
from domain.entities.estructura import Estructura


# ── ViewModels (datos puros, sin entidades de dominio) ────────────────────────

@dataclass
class CoordGeo:
    longitud: float
    latitud: float


@dataclass
class PoligonoViewModel:
    nombre: str
    coordenadas: List[CoordGeo] = field(default_factory=list)


@dataclass
class CeldaMallaViewModel:
    """Un cuadrilátero de la malla de cobertura (anillo cerrado: 5 coords)."""
    nombre: str
    coordenadas: List[CoordGeo] = field(default_factory=list)


@dataclass
class CoberturaViewModel:
    nombre: str
    poligonos: List[PoligonoViewModel] = field(default_factory=list)
    malla: List[CeldaMallaViewModel] = field(default_factory=list)


# ── Presenter ─────────────────────────────────────────────────────────────────

class GenerarPoligonoCoberturaPresenter(CoberturaOutputBoundary):
    """
    Implementa CoberturaOutputBoundary.

    Extrae las coordenadas geográficas del response del caso de uso y
    produce un CoberturaViewModel con datos planos listos para cualquier
    adaptador de salida (KmlWriter o FastAPI).
    """

    def presentar(self, response: GenerarPoligonoCoberturaResponse) -> CoberturaViewModel:
        estructura = response.estructura
        fg = estructura.estructura_figuras_geome

        return CoberturaViewModel(
            nombre=estructura.punto_cero.nombre,
            poligonos=self._extraer_poligonos(response, fg),
            malla=self._extraer_malla(estructura, fg),
        )

    # ------------------------------------------------------------------ helpers

    def _extraer_poligonos(
        self,
        response: GenerarPoligonoCoberturaResponse,
        fg: list,
    ) -> List[PoligonoViewModel]:
        result: List[PoligonoViewModel] = []
        for idx, poli in enumerate(response.poligono.lista_de_poligonitos):
            coords = [
                CoordGeo(longitud=fg[c[0]][c[1]].longitud, latitud=fg[c[0]][c[1]].latitud)
                for c in poli.lista_de_puntos
            ]
            result.append(PoligonoViewModel(nombre=str(idx), coordenadas=coords))
        return result

    def _extraer_malla(
        self,
        estructura: Estructura,
        fg: list,
    ) -> List[CeldaMallaViewModel]:
        ultimo_i = len(fg) - 1
        result: List[CeldaMallaViewModel] = []

        for i in range(estructura.n):
            for j in range(1, estructura.m):
                if estructura.estructura_matricial[i][j] != 1:
                    continue

                if i == ultimo_i:
                    p00, p0m = fg[i][j], fg[i][j - 1]
                    ppm, pp0 = fg[0][j - 1], fg[0][j]
                else:
                    p00, p0m = fg[i][j], fg[i][j - 1]
                    ppm, pp0 = fg[i + 1][j - 1], fg[i + 1][j]

                result.append(
                    CeldaMallaViewModel(
                        nombre=f"poligono{i}-{j}",
                        coordenadas=[
                            CoordGeo(p00.longitud, p00.latitud),
                            CoordGeo(p0m.longitud, p0m.latitud),
                            CoordGeo(ppm.longitud, ppm.latitud),
                            CoordGeo(pp0.longitud, pp0.latitud),
                            CoordGeo(p00.longitud, p00.latitud),   # cierra el anillo
                        ],
                    )
                )

        return result
