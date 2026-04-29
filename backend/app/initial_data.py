import logging
import os
import sys


from sqlmodel import Session, select, SQLModel

from src.infrastructure.persistence.database import engine
from src.infrastructure.persistence.models import PuntoTable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PUNTOS_INICIALES = [
    PuntoTable(ubigeo=11, nombre="transporte1", longitud=-78.426652, latitud=-6.884226, altura_antena=15.0, tipo="transporte", metros_sobre_nivel_mar=3733.0, green_asociado="",           conectado=True),
    PuntoTable(ubigeo=12, nombre="transporte2", longitud=-78.438926, latitud=-6.900705, altura_antena=15.0, tipo="transporte", metros_sobre_nivel_mar=3984.0, green_asociado="",           conectado=True),
    PuntoTable(ubigeo=13, nombre="transporte3", longitud=-78.454004, latitud=-6.937299, altura_antena=15.0, tipo="transporte", metros_sobre_nivel_mar=4103.0, green_asociado="",           conectado=True),
    PuntoTable(ubigeo=1,  nombre="acceso1",     longitud=-78.397267, latitud=-6.898882, altura_antena=15.0, tipo="acceso",     metros_sobre_nivel_mar=3825.0, green_asociado="",           conectado=False),
    PuntoTable(ubigeo=2,  nombre="acceso2",     longitud=-78.424352, latitud=-6.893104, altura_antena=15.0, tipo="acceso",     metros_sobre_nivel_mar=3848.0, green_asociado="",           conectado=False),
    PuntoTable(ubigeo=3,  nombre="acceso3",     longitud=-78.420674, latitud=-6.922061, altura_antena=15.0, tipo="acceso",     metros_sobre_nivel_mar=3853.0, green_asociado="",           conectado=False),
    PuntoTable(ubigeo=4,  nombre="acceso4",     longitud=-78.447779, latitud=-6.890579, altura_antena=15.0, tipo="acceso",     metros_sobre_nivel_mar=3737.0, green_asociado="",           conectado=False),
    PuntoTable(ubigeo=5,  nombre="acceso5",     longitud=-78.461209, latitud=-6.886364, altura_antena=15.0, tipo="acceso",     metros_sobre_nivel_mar=3673.0, green_asociado="transporte", conectado=False),
    PuntoTable(ubigeo=6,  nombre="acceso6",     longitud=-78.455400, latitud=-6.918098, altura_antena=15.0, tipo="acceso",     metros_sobre_nivel_mar=3934.0, green_asociado="",           conectado=False),
    PuntoTable(ubigeo=7,  nombre="acceso7",     longitud=-78.477435, latitud=-6.914850, altura_antena=15.0, tipo="acceso",     metros_sobre_nivel_mar=4024.0, green_asociado="",           conectado=False),
    PuntoTable(ubigeo=8,  nombre="acceso8",     longitud=-78.504492, latitud=-6.901809, altura_antena=15.0, tipo="acceso",     metros_sobre_nivel_mar=3752.0, green_asociado="",           conectado=False),
    PuntoTable(ubigeo=9,  nombre="acceso9",     longitud=-78.431883, latitud=-6.915703, altura_antena=15.0, tipo="acceso",     metros_sobre_nivel_mar=4076.0, green_asociado="transporte", conectado=False),
    PuntoTable(ubigeo=10, nombre="acceso10",    longitud=-78.436611, latitud=-6.895702, altura_antena=15.0, tipo="acceso",     metros_sobre_nivel_mar=3870.0, green_asociado="",           conectado=False),
]


def init_db(session: Session) -> None:
    SQLModel.metadata.create_all(engine)

    existing = session.exec(select(PuntoTable)).first()
    if existing:
        logger.info("Initial data already present, skipping seed.")
        return

    for punto in PUNTOS_INICIALES:
        session.add(punto)
    session.commit()
    logger.info("Seeded %d puntos.", len(PUNTOS_INICIALES))


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
