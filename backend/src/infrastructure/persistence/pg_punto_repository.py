import logging
from typing import List

from sqlmodel import Session, delete, select

from domain.entities.punto import Punto
from domain.entities.relacion import Relacion
from application.gateways.punto_gateway import PuntoGateway
from infrastructure.persistence.models import PuntoTable, RelacionTable

logger = logging.getLogger(__name__)


def _table_to_punto(row: PuntoTable) -> Punto:
    punto = Punto(
        nombre=row.nombre,
        ubigeo=row.ubigeo,
        longitud=row.longitud,
        latitud=row.latitud,
        altura_antena=row.altura_antena,
        tipo=row.tipo,
        metros_sobre_nivel_mar=row.metros_sobre_nivel_mar,
    )
    punto.green_asociado = row.green_asociado or ""
    punto.conectado = row.conectado
    return punto


class PgPuntoRepository(PuntoGateway):
    """
    Adaptador de infraestructura que implementa PuntoGateway
    usando SQLModel (SQLAlchemy + Pydantic) con una Session inyectada.

    Pertenece a la capa de Infraestructura.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    # ------------------------------------------------------------------ PuntoGateway

    def leer_puntos(self) -> List[Punto]:
        rows = self._session.exec(select(PuntoTable).order_by(PuntoTable.ubigeo)).all()
        return [_table_to_punto(r) for r in rows]

    def leer_puntos_por_tipo(self, tipo: str) -> List[Punto]:
        rows = self._session.exec(
            select(PuntoTable).where(PuntoTable.tipo == tipo).order_by(PuntoTable.ubigeo)
        ).all()
        return [_table_to_punto(r) for r in rows]

    def leer_relaciones(self) -> List[Relacion]:
        puntos_dict = {p.ubigeo: p for p in self.leer_puntos()}
        rows = self._session.exec(select(RelacionTable)).all()
        relaciones: List[Relacion] = []
        for row in rows:
            try:
                p_ini = puntos_dict[row.punto_inicial_id]
                p_fin = puntos_dict[row.punto_final_id]
                relaciones.append(Relacion(p_ini, p_fin))
            except KeyError as exc:
                logger.warning("relacion ignorada: %s", exc)
        return relaciones

    def guardar_puntos(self, puntos: List[Punto]) -> None:
        self._session.exec(delete(RelacionTable))
        self._session.exec(delete(PuntoTable))
        for p in puntos:
            self._session.add(PuntoTable(
                ubigeo=p.ubigeo, nombre=p.nombre, longitud=p.longitud,
                latitud=p.latitud, altura_antena=p.altura_antena, tipo=p.tipo,
                metros_sobre_nivel_mar=p.metros_sobre_nivel_mar,
                green_asociado=p.green_asociado, conectado=p.conectado,
            ))
        self._session.commit()

    def guardar_relaciones(self, relaciones: List[Relacion]) -> None:
        self._session.exec(delete(RelacionTable))
        for r in relaciones:
            self._session.add(RelacionTable(
                punto_inicial_id=r.punto_inicial.ubigeo,
                punto_final_id=r.punto_final.ubigeo,
                distancia=r.distancia,
            ))
        self._session.commit()

    def actualizar_conectado(self, puntos: List[Punto]) -> None:
        for p in puntos:
            db_punto = self._session.get(PuntoTable, p.ubigeo)
            if db_punto:
                db_punto.conectado = p.conectado
                self._session.add(db_punto)
        self._session.commit()

    def agregar_punto(self, punto: Punto) -> Punto:
        rows = self._session.exec(select(PuntoTable)).all()
        punto.ubigeo = max((r.ubigeo for r in rows), default=0) + 1
        self._session.add(PuntoTable(
            ubigeo=punto.ubigeo, nombre=punto.nombre, longitud=punto.longitud,
            latitud=punto.latitud, altura_antena=punto.altura_antena, tipo=punto.tipo,
            metros_sobre_nivel_mar=punto.metros_sobre_nivel_mar,
            green_asociado=punto.green_asociado, conectado=punto.conectado,
        ))
        self._session.commit()
        return punto
