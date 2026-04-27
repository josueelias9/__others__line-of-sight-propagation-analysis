"""
Punto de entrada principal del proyecto.

Ejecutar desde la raíz del repositorio:

    python main.py

Asegúrate de haber activado el entorno virtual y de que las carpetas
`in/` y `out/` existan (o serán creadas automáticamente en `out/`).
"""
import os
import sys

# Añade src/ al path de Python para permitir importaciones absolutas
_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

# También necesitamos el módulo srtm que vive en proyecto/
_PROYECTO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proyecto")
if _PROYECTO not in sys.path:
    sys.path.insert(0, _PROYECTO)

from interface.cli import run  # noqa: E402
import config

if __name__ == "__main__":
    config.setup_logging()
    run()
