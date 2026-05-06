import logging
import os

from sqlmodel import Session, select, SQLModel

from src.infrastructure.persistence.database import engine
from src.infrastructure.persistence.models import PuntoTable, PuntoTypeTable, UserTable
from app.data import TIPOS_INICIALES, PUNTOS_DATA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db(session: Session) -> None:
    SQLModel.metadata.create_all(engine)

    # ── Superuser ─────────────────────────────────────────────────────────────
    first_superuser_email = os.getenv("FIRST_SUPERUSER", "admin@example.com")
    first_superuser_password = os.getenv("FIRST_SUPERUSER_PASSWORD", "changeme123")

    existing_superuser = session.exec(
        select(UserTable).where(UserTable.email == first_superuser_email)
    ).first()

    if not existing_superuser:
        from app.core.security import get_password_hash

        superuser = UserTable(
            email=first_superuser_email,
            hashed_password=get_password_hash(first_superuser_password),
            is_active=True,
            is_superuser=True,
        )
        session.add(superuser)
        session.commit()
        logger.info("Created superuser: %s", first_superuser_email)

    # ── Seed punto_type if empty ───────────────────────────────────────────────
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

    for (
        ubigeo,
        nombre,
        longitud,
        latitud,
        altura_antena,
        tipo_name,
        msnm,
        green,
        conectado,
    ) in PUNTOS_DATA:
        session.add(
            PuntoTable(
                ubigeo=ubigeo,
                nombre=nombre,
                longitud=longitud,
                latitud=latitud,
                altura_antena=altura_antena,
                punto_type_id=tipo_map[tipo_name],
                metros_sobre_nivel_mar=msnm,
                green_asociado=green,
                conectado=conectado,
            )
        )
    session.commit()
    logger.info("Seeded %d puntos.", len(PUNTOS_DATA))


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
