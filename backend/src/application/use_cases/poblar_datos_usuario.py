from __future__ import annotations

import json
import logging
from dataclasses import dataclass

from sqlmodel import Session, select

from app.models import MultipoligonoTable, PuntoTable, UserTable
from application.interface.ports.data_loader import CsvDataLoaderPort

logger = logging.getLogger(__name__)


@dataclass
class PoblarDatosUsuarioRequest:
    email: str


@dataclass
class PoblarDatosUsuarioResponse:
    puntos_creados: int


class PoblarDatosUsuarioUseCase:
    """
    Caso de uso: poblar los datos de plantilla (CSVs de app/data/)
    asociándolos a un usuario específico identificado por su correo electrónico.

    Pertenece a la capa de Aplicación.
    """

    def __init__(self, session: Session, data_loader: CsvDataLoaderPort) -> None:
        self._session = session
        self._data_loader = data_loader

    def ejecutar(
        self, request: PoblarDatosUsuarioRequest
    ) -> PoblarDatosUsuarioResponse:
        user = self._session.exec(
            select(UserTable).where(UserTable.email == request.email)
        ).first()
        if user is None:
            raise ValueError(f"Usuario con email '{request.email}' no encontrado.")

        existing = self._session.exec(
            select(PuntoTable).where(PuntoTable.user_id == user.id)
        ).first()
        if existing:
            logger.info(
                "El usuario '%s' ya tiene datos poblados, se omite el seed.",
                request.email,
            )
            return PoblarDatosUsuarioResponse(puntos_creados=0)

        puntos = self._data_loader.load("punto")
        for row in puntos:
            self._session.add(
                PuntoTable(
                    ubigeo=int(row["ubigeo"]),
                    nombre=row["nombre"],
                    longitud=float(row["longitud"]),
                    latitud=float(row["latitud"]),
                    altura_antena=float(row["altura_antena"]),
                    punto_type_id=int(row["punto_type_id"]),
                    metros_sobre_nivel_mar=float(row["metros_sobre_nivel_mar"]),
                    green_asociado=row.get("green_asociado", ""),
                    conectado=row["conectado"].lower() in ("true", "1", "yes"),
                    user_id=user.id,
                )
            )
        self._session.commit()

        multipoligonos = self._data_loader.load("multipoligono")
        for row in multipoligonos:
            geojson_raw = row.get("geojson", "")
            geojson = json.loads(geojson_raw) if geojson_raw else {}
            self._session.add(
                MultipoligonoTable(
                    punto_ubigeo=int(row["punto_ubigeo"]),
                    geojson=geojson,
                    numero_de_ldv=int(row["numero_de_ldv"]),
                    muestras=int(row["muestras"]),
                    distancia_km=float(row["distancia_km"]),
                    altura_torre_fantasma=float(row["altura_torre_fantasma"]),
                    user_id=user.id,
                )
            )

        self._session.commit()
        logger.info(
            "Poblados %d puntos y %d multipolígonos para el usuario '%s'.",
            len(puntos),
            len(multipoligonos),
            request.email,
        )
        return PoblarDatosUsuarioResponse(puntos_creados=len(puntos))
