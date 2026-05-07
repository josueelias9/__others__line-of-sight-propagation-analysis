"""
Configuración centralizada de la aplicación FastAPI.
"""

import logging
import os

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_ignore_empty=True,
        extra="ignore",
    )

    # ── Database ───────────────────────────────────────────────────────────────
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = int(os.getenv("DB_PORT"))
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # ── Logging ──────────────────────────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"


settings = Settings()  # type: ignore


# ── Análisis (constantes, no variables de entorno) ────────────────────────────

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIR_INPUT = os.path.join(BASE_DIR, "in") + os.sep
DIR_OUTPUT = os.path.join(BASE_DIR, "out") + os.sep

MUESTRAS: int = 200
NUMERO_DE_LDV: int = 200
DISTANCIA_KM: float = 20.0
ALTURA_TORRE_FANTASMA: float = 15.0

ARCHIVO_TRANSPORTE = "uno"
ARCHIVO_ACCESO = "dos"


def de_km_a_grados(km: float) -> float:
    return km / 111.11


def de_grados_a_km(grados: float) -> float:
    return grados * 111.11


# ── Logging ────────────────────────────────────────────────────────────────────


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="myapp.log",
    )
