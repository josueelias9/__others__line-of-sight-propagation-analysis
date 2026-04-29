import logging
import os
import sys


from sqlmodel import Session, select, SQLModel

from src.infrastructure.persistence.database import engine
from src.infrastructure.persistence.models import PuntoTable, PuntoTypeTable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TIPOS_INICIALES = [
    PuntoTypeTable(name="acceso"),
    PuntoTypeTable(name="transporte"),
]

# (ubigeo, nombre, longitud, latitud, altura_antena, tipo_name, msnm, green_asociado, conectado)
_PUNTOS_DATA = [
    (11, "transporte1", -78.426652, -6.884226, 15.0, "transporte", 3733.0, "",           True),
    (12, "transporte2", -78.438926, -6.900705, 15.0, "transporte", 3984.0, "",           True),
    (13, "transporte3", -78.454004, -6.937299, 15.0, "transporte", 4103.0, "",           True),
    (1,  "acceso1",     -78.397267, -6.898882, 15.0, "acceso",     3825.0, "",           False),
    (2,  "acceso2",     -78.424352, -6.893104, 15.0, "acceso",     3848.0, "",           False),
    (3,  "acceso3",     -78.420674, -6.922061, 15.0, "acceso",     3853.0, "",           False),
    (4,  "acceso4",     -78.447779, -6.890579, 15.0, "acceso",     3737.0, "",           False),
    (5,  "acceso5",     -78.461209, -6.886364, 15.0, "acceso",     3673.0, "transporte", False),
    (6,  "acceso6",     -78.455400, -6.918098, 15.0, "acceso",     3934.0, "",           False),
    (7,  "acceso7",     -78.477435, -6.914850, 15.0, "acceso",     4024.0, "",           False),
    (8,  "acceso8",     -78.504492, -6.901809, 15.0, "acceso",     3752.0, "",           False),
    (9,  "acceso9",     -78.431883, -6.915703, 15.0, "acceso",     4076.0, "transporte", False),
    (10, "acceso10",    -78.436611, -6.895702, 15.0, "acceso",     3870.0, "",           False),
]


def init_db(session: Session) -> None:
    SQLModel.metadata.create_all(engine)

    # Seed punto_type if empty
    existing_tipos = session.exec(select(PuntoTypeTable)).all()
    if not existing_tipos:
        for tipo in TIPOS_INICIALES:
            session.add(tipo)
        session.commit()
        logger.info("Seeded %d punto_type rows.", len(TIPOS_INICIALES))

    # Build id lookup map
    tipo_map = {t.name: t.id for t in session.exec(select(PuntoTypeTable)).all()}

    # Seed puntos if empty
    existing = session.exec(select(PuntoTable)).first()
    if existing:
        logger.info("Initial data already present, skipping seed.")
        return

    for ubigeo, nombre, longitud, latitud, altura_antena, tipo_name, msnm, green, conectado in _PUNTOS_DATA:
        session.add(PuntoTable(
            ubigeo=ubigeo,
            nombre=nombre,
            longitud=longitud,
            latitud=latitud,
            altura_antena=altura_antena,
            punto_type_id=tipo_map[tipo_name],
            metros_sobre_nivel_mar=msnm,
            green_asociado=green,
            conectado=conectado,
        ))
    session.commit()
    logger.info("Seeded %d puntos.", len(_PUNTOS_DATA))


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
