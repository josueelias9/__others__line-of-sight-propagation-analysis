import logging
from typing import List

from sqlmodel import Session, select

from domain.entities.punto import Punto
from domain.entities.red import Red
from domain.entities.relacion import Relacion
from application.interface.db.red import RedGateway
from infrastructure.persistence.models import RedTable, RedRelacionTable
from infrastructure.geometry.shapely_geometry_repository import (
    ShapelyGeometryRepository,
)

logger = logging.getLogger(__name__)


class PgRedRepository(RedGateway):
    """
    Adaptador de infraestructura que implementa RedGateway
    usando SQLModel con una Session inyectada.

    Pertenece a la capa de Infraestructura.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def guardar_red(self, geojson: dict, red: Red) -> Red:
        red_row = RedTable(nombre=red.nombre, geojson=geojson)
        self._session.add(red_row)
        self._session.flush()  # populate red_row.id

        for rel in red.lista_de_relaciones:
            self._session.add(
                RedRelacionTable(
                    red_id=red_row.id,
                    punto_inicial_ubigeo=rel.punto_inicial.ubigeo,
                    punto_final_ubigeo=rel.punto_final.ubigeo,
                    distancia=rel.distancia,
                )
            )

        self._session.commit()
        red.id = red_row.id
        logger.info(
            "Red '%s' guardada con id=%d y %d relaciones",
            red.nombre,
            red.id,
            len(red.lista_de_relaciones),
        )
        return red

    def listar_redes(self) -> List[Red]:
        red_rows = self._session.exec(select(RedTable).order_by(RedTable.id)).all()
        redes: List[Red] = []
        for row in red_rows:
            rel_rows = self._session.exec(
                select(RedRelacionTable).where(RedRelacionTable.red_id == row.id)
            ).all()
            relaciones = []
            for rr in rel_rows:
                p_ini = Punto(
                    nombre="",
                    ubigeo=rr.punto_inicial_ubigeo,
                    longitud=0,
                    latitud=0,
                    altura_antena=0,
                    tipo="",
                    metros_sobre_nivel_mar=0,
                )
                p_fin = Punto(
                    nombre="",
                    ubigeo=rr.punto_final_ubigeo,
                    longitud=0,
                    latitud=0,
                    altura_antena=0,
                    tipo="",
                    metros_sobre_nivel_mar=0,
                )
                rel = Relacion(p_ini, p_fin)
                rel.distancia = rr.distancia
                relaciones.append(rel)
            redes.append(
                Red(
                    id=row.id,
                    nombre=row.nombre,
                    lista_de_relaciones=relaciones,
                    geojson=row.geojson,
                )
            )
        return redes

    def eliminar_red(self, red_id: int) -> None:
        row = self._session.get(RedTable, red_id)
        if row:
            self._session.delete(row)
            self._session.commit()
            logger.info("Red id=%d eliminada", red_id)
