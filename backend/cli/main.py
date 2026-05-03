"""
Punto de entrada del CLI.

Ejecutar desde la raíz del repositorio:

    python cli/main.py

Asegúrate de haber activado el entorno virtual y de que las carpetas
`in/` y `out/` existan (o serán creadas automáticamente en `out/`).
"""

import os
import sys

# Añade src/, proyecto/ y la raíz al path para importaciones absolutas
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SRC = os.path.join(_ROOT, "src")
_PROYECTO = os.path.join(_ROOT, "proyecto")
for _p in (_ROOT, _SRC, _PROYECTO):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import config
from cli.cli import run  # noqa: E402

if __name__ == "__main__":
    config.setup_logging()
    run()
