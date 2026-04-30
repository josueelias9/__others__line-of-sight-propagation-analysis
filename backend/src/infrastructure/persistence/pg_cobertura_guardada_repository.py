from typing import Any, Dict, List

from sqlmodel import Session, select

from application.interface.db.cobertura_guardada import (
    CoberturaGuardada,
    CoberturaGuardadaGateway,
)
from infrastructure.persistence.models import MultipoligonoTable, PuntoTable


class PgCoberturaGuardadaRepository(CoberturaGuardadaGateway):
    """
    Implementación de CoberturaGuardadaGateway sobre PostgreSQL via SQLModel.

    Pertenece a la capa de Infraestructura.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def guardar(
        self,
        punto_ubigeo: int,
        geojson: Dict[str, Any],
        numero_de_ldv: int,
        muestras: int,
        distancia_km: float,
        altura_torre_fantasma: float,
    ) -> int:
        existing = self._session.exec(
            select(MultipoligonoTable).where(
                MultipoligonoTable.punto_ubigeo == punto_ubigeo
            )
        ).first()

        if existing:
            existing.geojson = geojson
            existing.numero_de_ldv = numero_de_ldv
            existing.muestras = muestras
            existing.distancia_km = distancia_km
            existing.altura_torre_fantasma = altura_torre_fantasma
            self._session.add(existing)
            self._session.commit()
            self._session.refresh(existing)
            return existing.id

        row = MultipoligonoTable(
            punto_ubigeo=punto_ubigeo,
            geojson=geojson,
            numero_de_ldv=numero_de_ldv,
            muestras=muestras,
            distancia_km=distancia_km,
            altura_torre_fantasma=altura_torre_fantasma,
        )
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return row.id

    def listar(self) -> List[CoberturaGuardada]:
        rows = self._session.exec(select(MultipoligonoTable)).all()
        if not rows:
            return []

        ubigeos = {r.punto_ubigeo for r in rows}
        puntos_map: Dict[int, str] = {
            p.ubigeo: p.nombre
            for p in self._session.exec(
                select(PuntoTable).where(PuntoTable.ubigeo.in_(ubigeos))
            ).all()
        }

        return [
            CoberturaGuardada(
                id=r.id,
                punto_ubigeo=r.punto_ubigeo,
                punto_nombre=puntos_map.get(r.punto_ubigeo, str(r.punto_ubigeo)),
                geojson=r.geojson,
                numero_de_ldv=r.numero_de_ldv,
                muestras=r.muestras,
                distancia_km=r.distancia_km,
                altura_torre_fantasma=r.altura_torre_fantasma,
            )
            for r in rows
        ]

    def eliminar(self, id: int) -> None:
        row = self._session.get(MultipoligonoTable, id)
        if row is None:
            raise ValueError(f"Cobertura con id={id} no encontrada")
        self._session.delete(row)
        self._session.commit()
