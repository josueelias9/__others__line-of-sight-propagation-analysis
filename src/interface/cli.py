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

# Asegura que src/ esté en el path para importaciones absolutas
_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.dirname(os.path.dirname(_SRC_DIR))
for _p in (_SRC_DIR, os.path.join(_SRC_DIR, ".."), _ROOT_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import config
from application.use_cases.asignar_alturas import AsignarAlturasRequest, AsignarAlturasUseCase
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
from infrastructure.elevation.srtm_elevation_repository import SrtmElevationRepository
from infrastructure.output.kml_writer import KmlWriter
from infrastructure.output.txt_writer import TxtWriter
from infrastructure.persistence.csv_punto_repository import CsvPuntoRepository


# ── Ensamblado del contenedor de dependencias ─────────────────────────────────

os.makedirs(config.DIR_OUTPUT, exist_ok=True)

elevation_repo = SrtmElevationRepository(muestras=config.MUESTRAS)
punto_repo = CsvPuntoRepository(directorio=config.DIR_INPUT)
kml_output = KmlWriter(directorio=config.DIR_OUTPUT)
txt_output = TxtWriter(directorio=config.DIR_OUTPUT)

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

generar_poligono_cobertura_uc = GenerarPoligonoCoberturaUseCase(
    elevation_repo=elevation_repo,
    kml_output=kml_output,
    numero_de_ldv=config.NUMERO_DE_LDV,
    muestras=config.MUESTRAS,
    distancia_grados=config.de_km_a_grados(config.DISTANCIA_KM),
    altura_torre_fantasma=config.ALTURA_TORRE_FANTASMA,
)

encontrar_torre_fantasma_uc = EncontrarTorreFantasmaUseCase(
    punto_repo=punto_repo,
    cobertura_uc=generar_poligono_cobertura_uc,
    kml_output=kml_output,
    txt_output=txt_output,
    distancia_maxima=config.DISTANCIA_KM,
)


# ── Menú interactivo ──────────────────────────────────────────────────────────

_MENU = """
╔═════════════════════════════════════════════════════════════════╗
║ Visualizador de zonas de cobertura en zonas accidentadas        ║
╠═════════════════════════════════════════════════════════════════╣
║  1. Asignar alturas a puntos (un archivo)               -> ok   ║
║  2. Encontrar relaciones posibles con LOS (un archivo)          ║
║  3. Generar polígono de cobertura (un punto por ubigeo) -> ok   ║
║  4. Buscar ubicación de torre fantasma (un archivo)             ║
║  5. Árbol de conexión (dos archivos: conectados/no)     -> ok   ║
║  6. Clusterizar puntos                                          ║
║  0. Salir                                                       ║
╚═════════════════════════════════════════════════════════════════╝
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
            asignar_alturas_uc.ejecutar(AsignarAlturasRequest(nombre_archivo="punto"))

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
            archivo = input("Nombre del archivo de puntos (sin .txt): ").strip()
            puntos = punto_repo.leer_puntos(archivo)
            ubigeo = int(input("Ubigeo del punto: ").strip())
            try:
                punto = next(p for p in puntos if p.ubigeo == ubigeo)
            except StopIteration:
                print(f"No se encontró un punto con ubigeo={ubigeo}.")
                continue
            generar_poligono_cobertura_uc.ejecutar(
                GenerarPoligonoCoberturaRequest(punto=punto, escribir_kml=True)
            )
            print(f"KML generado en {config.DIR_OUTPUT}{punto.nombre}.kml")

        elif opcion == "4":
            archivo = input("Nombre del archivo de puntos (sin .txt): ").strip()
            salida = input("Prefijo de archivos de salida: ").strip()
            encontrar_torre_fantasma_uc.ejecutar(
                EncontrarTorreFantasmaRequest(
                    nombre_archivo=archivo,
                    nombre_salida=salida,
                )
            )

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
