from __future__ import annotations

from dataclasses import dataclass
from typing import List

from application.interface.db.cobertura_guardada import (
    CoberturaGuardada,
    CoberturaGuardadaGateway,
)


@dataclass
class ListarCoberturasRequest:
    pass

  
class ListarCoberturasUseCase:
    """
    Caso de uso: recuperar las coberturas guardadas en la base de datos.

    Pertenece a la capa de Aplicación.
    """

    def __init__(self, repo: CoberturaGuardadaGateway) -> None:
        self._repo = repo

    def ejecutar(self, request: ListarCoberturasRequest) -> List[CoberturaGuardada]:
        return self._repo.listar()
