import logging

from sqlmodel import Session, select, SQLModel

from src.infrastructure.persistence.database import engine
from src.infrastructure.persistence.csv_data_loader import load_csv_data
from app.models import PuntoTable, PuntoTypeTable, UserTable
import bcrypt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TIPOS_INICIALES = ["acceso", "transporte"]


def init_db(session: Session) -> None:
    SQLModel.metadata.create_all(engine)

    data = load_csv_data()

    # ── Seed punto_type if empty ───────────────────────────────────────────────
    existing_tipos = session.exec(select(PuntoTypeTable)).all()
    if not existing_tipos:
        for tipo in TIPOS_INICIALES:
            session.add(PuntoTypeTable(name=tipo))
        session.commit()
        logger.info("Seeded %d punto_type rows.", len(TIPOS_INICIALES))



def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
