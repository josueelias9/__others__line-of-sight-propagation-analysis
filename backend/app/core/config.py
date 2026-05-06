"""
Configuración centralizada de la aplicación FastAPI.
"""

import logging
import os

# ── Rutas ──────────────────────────────────────────────────────────────────────

# Directorio raíz del repositorio (dos niveles arriba: app/core/ -> app/ -> root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Directorio de archivos de entrada (.csv con puntos)
DIR_INPUT = os.path.join(BASE_DIR, "in") + os.sep

# Directorio de archivos de salida (.kml, .txt generados)
DIR_OUTPUT = os.path.join(BASE_DIR, "out") + os.sep

# ── Parámetros de análisis ─────────────────────────────────────────────────────

MUESTRAS: int = 200
NUMERO_DE_LDV: int = 200
DISTANCIA_KM: float = 20.0
ALTURA_TORRE_FANTASMA: float = 15.0

ARCHIVO_TRANSPORTE = "uno"
ARCHIVO_ACCESO = "dos"


def de_km_a_grados(km: float) -> float:
    """Convierte kilómetros a grados (aproximación esférica)."""
    return km / 111.11


def de_grados_a_km(grados: float) -> float:
    """Convierte grados a kilómetros (aproximación esférica)."""
    return grados * 111.11


# ── Base de datos ─────────────────────────────────────────────────────────────

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ── Auth ──────────────────────────────────────────────────────────────────────

SECRET_KEY: str = os.getenv("SECRET_KEY", "please-change-this-insecure-default-key")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
FIRST_SUPERUSER: str = os.getenv("FIRST_SUPERUSER", "admin@example.com")
FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD", "changeme123")

# ── Logging ────────────────────────────────────────────────────────────────────


def setup_logging() -> None:
    """Configura el logging: consola (INFO) y archivo app.log (DEBUG)."""
    logging.basicConfig(
        level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="myapp.log",
    )
