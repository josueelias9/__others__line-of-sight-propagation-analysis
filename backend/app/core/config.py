"""
Configuración centralizada de la aplicación FastAPI.
"""

import logging
import os
import secrets
import warnings
from typing import Any, Literal

from pydantic import EmailStr, computed_field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_ignore_empty=True,
        extra="ignore",
    )

    # ── Auth ───────────────────────────────────────────────────────────────────
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    FIRST_SUPERUSER: EmailStr = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "changethis"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

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

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("DB_PASSWORD", self.DB_PASSWORD)
        self._check_default_secret("FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD)
        return self


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
