from __future__ import annotations

from application.interface.ports.output import CoberturaOutputBoundary
from application.use_cases.generar_poligono_cobertura import (
    GenerarPoligonoCoberturaResponse,
)


class PassthroughCoberturaPresenter(CoberturaOutputBoundary):
    """Implementa CoberturaOutputBoundary devolviendo el response tal cual.
    Usada por use cases internos que necesitan los objetos de dominio."""

    def presentar(
        self, response: GenerarPoligonoCoberturaResponse
    ) -> GenerarPoligonoCoberturaResponse:
        return response
