"""
Configuración centralizada del proyecto.

Modifica este archivo para adaptar las rutas y parámetros a tu entorno.
"""

import logging
import os

# ── Rutas ──────────────────────────────────────────────────────────────────────

# Directorio raíz del repositorio
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directorio de archivos de entrada (.txt con puntos)
DIR_INPUT = os.path.join(BASE_DIR, "in") + os.sep

# Directorio de archivos de salida (.kml, .txt generados)
DIR_OUTPUT = os.path.join(BASE_DIR, "out") + os.sep

# ── Parámetros de análisis ─────────────────────────────────────────────────────

# Número de muestras para interpolación de perfil de elevación
MUESTRAS: int = 200

# Número de direcciones (lados) de la grilla polar
NUMERO_DE_LDV: int = 200

# Distancia máxima de radio-enlace en kilómetros
DISTANCIA_KM: float = 20.0

# Altura de la torre fantasma (repetidor hipotético) en metros
ALTURA_TORRE_FANTASMA: float = 15.0

# Nombres de archivos de entrada (sin extensión .txt)
ARCHIVO_TRANSPORTE = "uno"
ARCHIVO_ACCESO = "dos"


def de_km_a_grados(km: float) -> float:
    """Convierte kilómetros a grados (aproximación esférica)."""
    return km / 111.11


def de_grados_a_km(grados: float) -> float:
    """Convierte grados a kilómetros (aproximación esférica)."""
    return grados * 111.11


# ── Logging ────────────────────────────────────────────────────────────────────


def setup_logging() -> None:
    """Configura el logging: consola (INFO) y archivo app.log (DEBUG)."""
    logging.basicConfig(
        level=getattr(logging, os.getenv("LOG_LEVEL")),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="myapp.log",
    )
