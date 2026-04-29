"""
Interfaz de línea de comandos (CLI).

Punto de entrada que ensambla (wires) todas las capas siguiendo
el principio de inversión de dependencias de Clean Architecture:

    Interface  →  Application  →  Domain
                ↗
    Infrastructure

Modifica `_construir_contenedor()` para cambiar implementaciones concretas
sin tocar ninguna capa de dominio o aplicación.
"""
import os
import sys

# Asegura que src/ y la raíz estén en el path para importaciones absolutas
_CLI_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.dirname(_CLI_DIR)
_SRC_DIR = os.path.join(_ROOT_DIR, "src")
for _p in (_ROOT_DIR, _SRC_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import config
from application.use_cases.asignar_alturas import AsignarAlturasUseCase
from application.use_cases.encontrar_relaciones import (
    EncontrarRelacionesClusterizarRequest,
    EncontrarRelacionesArbolRequest,
    EncontrarRelacionesUnArchivoRequest,
    EncontrarRelacionesUseCase,
)
from application.use_cases.encontrar_torre_fantasma import (
    EncontrarTorreFantasmaRequest,
    EncontrarTorreFantasmaUseCase,
)
from application.use_cases.generar_poligono_cobertura import (
    GenerarPoligonoCoberturaRequest,
    GenerarPoligonoCoberturaUseCase,
)
from application.ports.output_port import CoberturaOutputBoundary
from interface.presenters.cobertura_presenter import GenerarPoligonoCoberturaPresenter
from interface.presenters.passthrough_presenter import PassthroughCoberturaPresenter
from infrastructure.elevation.srtm_elevation_repository import SrtmElevationRepository
from infrastructure.geometry.shapely_geometry_repository import ShapelyGeometryRepository
from infrastructure.output.kml_writer import KmlWriter
from infrastructure.output.txt_writer import TxtWriter
from infrastructure.persistence.csv_punto_repository import CsvPuntoRepository


import logging

logger = logging.getLogger(__name__)


# ── Ensamblado del contenedor de dependencias ─────────────────────────────────

os.makedirs(config.DIR_OUTPUT, exist_ok=True)

elevation_repo = SrtmElevationRepository(muestras=config.MUESTRAS)
punto_repo = CsvPuntoRepository(directorio=config.DIR_INPUT)
kml_output = KmlWriter(directorio=config.DIR_OUTPUT)
txt_output = TxtWriter(directorio=config.DIR_OUTPUT)
geometry_repo = ShapelyGeometryRepository()

asignar_alturas_uc = AsignarAlturasUseCase(
    punto_repo=punto_repo,
    elevation_repo=elevation_repo,
)

encontrar_relaciones_uc = EncontrarRelacionesUseCase(
    punto_repo=punto_repo,
    elevation_repo=elevation_repo,
    kml_output=kml_output,
    muestras=config.MUESTRAS,
)

# Instancia con el presenter real: devuelve CoberturaViewModel (CLI opción 3 / FastAPI)
generar_poligono_cobertura_uc = GenerarPoligonoCoberturaUseCase(
    elevation_repo=elevation_repo,
    punto_repo=punto_repo,
    output_boundary=GenerarPoligonoCoberturaPresenter(),
    numero_de_ldv=config.NUMERO_DE_LDV,
    muestras=config.MUESTRAS,
    distancia_grados=config.de_km_a_grados(config.DISTANCIA_KM),
    altura_torre_fantasma=config.ALTURA_TORRE_FANTASMA,
)

# Instancia con passthrough: devuelve GenerarPoligonoCoberturaResponse (callers internos)
_cobertura_uc_interno = GenerarPoligonoCoberturaUseCase(
    elevation_repo=elevation_repo,
    punto_repo=punto_repo,
    output_boundary=PassthroughCoberturaPresenter(),
    numero_de_ldv=config.NUMERO_DE_LDV,
    muestras=config.MUESTRAS,
    distancia_grados=config.de_km_a_grados(config.DISTANCIA_KM),
    altura_torre_fantasma=config.ALTURA_TORRE_FANTASMA,
)

encontrar_torre_fantasma_uc = EncontrarTorreFantasmaUseCase(
    punto_repo=punto_repo,
    cobertura_uc=_cobertura_uc_interno,
    geometry_gw=geometry_repo,
    kml_output=kml_output,
    txt_output=txt_output,
    distancia_maxima=config.DISTANCIA_KM,
)


# ── Menú interactivo ──────────────────────────────────────────────────────────

_MENU = """
╔══════════════════════════════════════════════════════════════════════╗
║ Visualizador de zonas de cobertura en zonas accidentadas             ║
╠══════════════════════════════════════════════════════════════════════╣
║  1. Asignar alturas a puntos (punto.csv)                       -> ok ║
║  2. Encontrar relaciones posibles con LOS (un archivo)               ║
║  3. Generar polígono de cobertura (un punto por ubigeo)        -> ok ║
║  4. Buscar ubicación de torre fantasma (un archivo)                  ║
║  5. Árbol de conexión (punto.csv: conectados vs no conectados) -> ok ║
║  6. Clusterizar puntos                                               ║
║  0. Salir                                                            ║
╚══════════════════════════════════════════════════════════════════════╝
"""


def run() -> None:
    """Bucle principal del CLI."""

    while True:
        print(_MENU)
        opcion = input("Opción: ").strip()

        if opcion == "0":
            print("Hasta luego.")
            break

        elif opcion == "1":
            asignar_alturas_uc.ejecutar()

        elif opcion == "2":
            archivo = input("Nombre del archivo de puntos (sin .csv): ").strip()
            dist = float(input(f"Distancia máxima en km [{config.DISTANCIA_KM}]: ").strip() or config.DISTANCIA_KM)
            encontrar_relaciones_uc.ejecutar_un_archivo(
                EncontrarRelacionesUnArchivoRequest(
                    nombre_archivo=archivo,
                    distancia_maxima=dist,
                )
            )

        elif opcion == "3":
            puntos = punto_repo.leer_puntos()
            print("\nPuntos disponibles:")
            for p in puntos:
                print(f"  [{p.ubigeo:>3}] {p.nombre} ({p.tipo})")
            ubigeo = int(input("\nUbigeo del punto: ").strip())
            response = generar_poligono_cobertura_uc.ejecutar(
                GenerarPoligonoCoberturaRequest(ubigeo=ubigeo)
            )  # returns CoberturaViewModel via presenter
            kml_output.escribir_cobertura(response)
            punto_nombre = next((p.nombre for p in puntos if p.ubigeo == ubigeo), str(ubigeo))
            print(f"KML generado en {config.DIR_OUTPUT}{punto_nombre}.kml")


        # TODO queda pendiente ya que hay problemas (ver bug.log)
        # elif opcion == "4":
        #     salida = input("Prefijo de archivos de salida: ").strip()
        #     ubigeos_raw = input("Ubigeos a filtrar (separados por coma, vacío = todos, ejemplo: 4,5,6): ").strip()
        #     ubigeos = [int(u) for u in ubigeos_raw.split(",") if u.strip()] or None
        #     encontrar_torre_fantasma_uc.ejecutar(
        #         EncontrarTorreFantasmaRequest(
        #             nombre_salida=salida,
        #             ubigeos=ubigeos,
        #         )
        #     )

        elif opcion == "5":
            tipo_conectados = input("Tipo de puntos BASE/CONECTADOS (ej: transporte): ").strip()
            tipo_no_conectados = input("Tipo de puntos a CONECTAR (ej: acceso): ").strip()
            dist = float(input(f"Distancia máxima en km [{config.DISTANCIA_KM}]: ").strip() or config.DISTANCIA_KM)
            encontrar_relaciones_uc.ejecutar_dos_archivos_arbol(
                EncontrarRelacionesArbolRequest(
                    tipo_conectados=tipo_conectados,
                    tipo_no_conectados=tipo_no_conectados,
                    distancia_maxima=dist,
                )
            )

        elif opcion == "6":
            archivo = input("Nombre del archivo de puntos (sin .csv): ").strip()
            dist = float(input(f"Distancia máxima en km [{config.DISTANCIA_KM}]: ").strip() or config.DISTANCIA_KM)
            encontrar_relaciones_uc.ejecutar_clusterizar(
                EncontrarRelacionesClusterizarRequest(
                    nombre_archivo=archivo,
                    distancia_maxima=dist,
                )
            )

        else:
            print("Opción no válida, intenta de nuevo.")
