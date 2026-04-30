import logging
from typing import Dict, List, Optional

from sqlmodel import Session, delete, select

from domain.entities.punto import Punto
from domain.entities.relacion import Relacion
from application.interface.db.punto import PuntoGateway
from infrastructure.persistence.models import PuntoTable, PuntoTypeTable, RelacionTable

logger = logging.getLogger(__name__)


def _load_tipo_map(session: Session) -> Dict[int, str]:
    """Returns a mapping of punto_type.id -> punto_type.name."""
    rows = session.exec(select(PuntoTypeTable)).all()
    return {r.id: r.name for r in rows}


def _get_tipo_id(session: Session, tipo_name: str) -> int:
    """Returns the punto_type.id for the given name, raising ValueError if not found."""
    row = session.exec(select(PuntoTypeTable).where(PuntoTypeTable.name == tipo_name)).first()
    if row is None:
        raise ValueError(f"Unknown punto type: '{tipo_name}'")
    return row.id


def _table_to_punto(row: PuntoTable, tipo_map: Dict[int, str]) -> Punto:
    punto = Punto(
        nombre=row.nombre,
        ubigeo=row.ubigeo,
        longitud=row.longitud,
        latitud=row.latitud,
        altura_antena=row.altura_antena,
        tipo=tipo_map.get(row.punto_type_id, ""),
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

    def leer_puntos(self, tipo: Optional[str] = None) -> List[Punto]:
        tipo_map = _load_tipo_map(self._session)
        stmt = select(PuntoTable).order_by(PuntoTable.ubigeo)
        if tipo is not None:
            tipo_row = self._session.exec(
                select(PuntoTypeTable).where(PuntoTypeTable.name == tipo)
            ).first()
            if tipo_row is None:
                return []
            stmt = stmt.where(PuntoTable.punto_type_id == tipo_row.id)
        rows = self._session.exec(stmt).all()
        return [_table_to_punto(r, tipo_map) for r in rows]

    def obtener_punto_por_ubigeo(self, ubigeo: int) -> Punto:
        tipo_map = _load_tipo_map(self._session)
        row = self._session.exec(
            select(PuntoTable).where(PuntoTable.ubigeo == ubigeo)
        ).first()
        if row is None:
            raise ValueError(f"No se encontró un punto con ubigeo={ubigeo}")
        return _table_to_punto(row, tipo_map)

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
            tipo_id = _get_tipo_id(self._session, p.tipo)
            self._session.add(PuntoTable(
                ubigeo=p.ubigeo, nombre=p.nombre, longitud=p.longitud,
                latitud=p.latitud, altura_antena=p.altura_antena,
                punto_type_id=tipo_id,
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
        tipo_id = _get_tipo_id(self._session, punto.tipo)
        rows = self._session.exec(select(PuntoTable)).all()
        punto.ubigeo = max((r.ubigeo for r in rows), default=0) + 1
        self._session.add(PuntoTable(
            ubigeo=punto.ubigeo, nombre=punto.nombre, longitud=punto.longitud,
            latitud=punto.latitud, altura_antena=punto.altura_antena,
            punto_type_id=tipo_id,
            metros_sobre_nivel_mar=punto.metros_sobre_nivel_mar,
            green_asociado=punto.green_asociado, conectado=punto.conectado,
        ))
        self._session.commit()
        return punto

