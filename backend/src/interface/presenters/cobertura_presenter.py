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
from typing import Any, Dict

from application.ports.output_port import CoberturaOutputBoundary
from application.use_cases.generar_poligono_cobertura import (
    GenerarPoligonoCoberturaResponse,
)


# ── ViewModel ─────────────────────────────────────────────────────────────────

@dataclass
class CoberturaViewModel:
    nombre: str
    geojson: Dict[str, Any] = field(default_factory=dict)
    malla_geojson: Dict[str, Any] = field(default_factory=dict)


# ── Presenter ─────────────────────────────────────────────────────────────────

class GenerarPoligonoCoberturaPresenter(CoberturaOutputBoundary):
    """
    Implementa CoberturaOutputBoundary.

    Produce un CoberturaViewModel con el GeoJSON unificado (unary_union)
    y el FeatureCollection de la malla polar, listos para FastAPI o KmlWriter.
    """

    def presentar(self, response: GenerarPoligonoCoberturaResponse) -> CoberturaViewModel:
        return CoberturaViewModel(
            nombre=response.nombre,
            geojson=response.geojson,
            malla_geojson=response.malla_geojson,
        )
