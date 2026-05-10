import logging
from typing import List, Optional

from sqlmodel import Session, select

from domain.entities.punto import Punto
from domain.entities.red import Red
from domain.entities.relacion import Relacion
from application.interface.db.red import RedGateway
from app.models import RedTable, RedPuntoTable

logger = logging.getLogger(__name__)


class PgRedRepository(RedGateway):
    """
    Adaptador de infraestructura que implementa RedGateway
    usando SQLModel con una Session inyectada.

    Pertenece a la capa de Infraestructura.
    """

    def __init__(self, session: Session, user_id: Optional[int] = None) -> None:
        self._session = session
        self._user_id = user_id

    def guardar_red(self, geojson: dict, red: Red) -> Red:
        red_row = RedTable(nombre=red.nombre, geojson=geojson, user_id=self._user_id)
        self._session.add(red_row)
        self._session.flush()  # populate red_row.id

        for rel in red.lista_de_relaciones:
            self._session.add(
                RedPuntoTable(
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
        stmt = select(RedTable).order_by(RedTable.id)
        if self._user_id is not None:
            stmt = stmt.where(RedTable.user_id == self._user_id)
        red_rows = self._session.exec(stmt).all()
        redes: List[Red] = []
        for row in red_rows:
            rel_rows = self._session.exec(
                select(RedPuntoTable).where(RedPuntoTable.red_id == row.id)
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
        stmt = select(RedTable).where(RedTable.id == red_id)
        if self._user_id is not None:
            stmt = stmt.where(RedTable.user_id == self._user_id)
        row = self._session.exec(stmt).first()
        if row:
            self._session.delete(row)
            self._session.commit()
            logger.info("Red id=%d eliminada", red_id)
