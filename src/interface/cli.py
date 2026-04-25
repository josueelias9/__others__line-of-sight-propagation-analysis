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
from application.use_cases.asignar_alturas import AsignarAlturasUseCase
from application.use_cases.encontrar_relaciones import EncontrarRelacionesUseCase
from application.use_cases.encontrar_torre_fantasma import EncontrarTorreFantasmaUseCase
from application.use_cases.generar_poligono_cobertura import (
    GenerarPoligonoCoberturaUseCase,
)
from infrastructure.elevation.srtm_elevation_repository import SrtmElevationRepository
from infrastructure.output.kml_writer import KmlWriter
from infrastructure.output.txt_writer import TxtWriter
from infrastructure.persistence.txt_punto_repository import TxtPuntoRepository


# ── Ensamblado del contenedor de dependencias ─────────────────────────────────


def _construir_contenedor():
    """
    Instancia y conecta todas las dependencias.
    Devuelve un diccionario con los casos de uso listos para usar.
    """
    os.makedirs(config.DIR_OUTPUT, exist_ok=True)

    elevation_repo = SrtmElevationRepository(muestras=config.MUESTRAS)
    punto_repo = TxtPuntoRepository(directorio=config.DIR_INPUT)
    kml_output = KmlWriter(directorio=config.DIR_OUTPUT)
    txt_output = TxtWriter(directorio=config.DIR_OUTPUT)

    asignar_alturas_uc = AsignarAlturasUseCase(
        punto_repo=punto_repo,
        elevation_repo=elevation_repo,
        txt_output=txt_output,
    )

    encontrar_relaciones_uc = EncontrarRelacionesUseCase(
        punto_repo=punto_repo,
        elevation_repo=elevation_repo,
        kml_output=kml_output,
        txt_output=txt_output,
        muestras=config.MUESTRAS,
    )

    generar_poligono_uc = GenerarPoligonoCoberturaUseCase(
        elevation_repo=elevation_repo,
        kml_output=kml_output,
        numero_de_ldv=config.NUMERO_DE_LDV,
        muestras=config.MUESTRAS,
        distancia_grados=config.de_km_a_grados(config.DISTANCIA_KM),
        altura_torre_fantasma=config.ALTURA_TORRE_FANTASMA,
    )

    encontrar_torre_uc = EncontrarTorreFantasmaUseCase(
        punto_repo=punto_repo,
        cobertura_uc=generar_poligono_uc,
        kml_output=kml_output,
        txt_output=txt_output,
        distancia_maxima=config.DISTANCIA_KM,
    )

    return {
        "asignar_alturas": asignar_alturas_uc,
        "encontrar_relaciones": encontrar_relaciones_uc,
        "generar_poligono": generar_poligono_uc,
        "encontrar_torre": encontrar_torre_uc,
        "punto_repo": punto_repo,
        "kml_output": kml_output,
        "txt_output": txt_output,
    }


# ── Menú interactivo ──────────────────────────────────────────────────────────

_MENU = """
╔══════════════════════════════════════════════════════════╗
║  Visualizador de zonas de cobertura en zonas accidentadas ║
╠══════════════════════════════════════════════════════════╣
║  1. Asignar alturas a puntos (un archivo)                ║
║  2. Encontrar relaciones posibles con LOS (un archivo)   ║
║  3. Generar polígono de cobertura (un punto por ubigeo)  ║
║  4. Buscar ubicación de torre fantasma (un archivo)      ║
║  5. Árbol de conexión (dos archivos: conectados/no)      ║
║  6. Clusterizar puntos                                   ║
║  0. Salir                                                ║
╚══════════════════════════════════════════════════════════╝
"""


def run() -> None:
    """Bucle principal del CLI."""
    uc = _construir_contenedor()

    while True:
        print(_MENU)
        opcion = input("Opción: ").strip()

        if opcion == "0":
            print("Hasta luego.")
            break

        elif opcion == "1":
            archivo = input("Nombre del archivo de puntos (sin .txt): ").strip()
            uc["asignar_alturas"].ejecutar(archivo)

        elif opcion == "2":
            archivo = input("Nombre del archivo de puntos (sin .txt): ").strip()
            dist = float(input(f"Distancia máxima en km [{config.DISTANCIA_KM}]: ").strip() or config.DISTANCIA_KM)
            salida = input("Nombre del archivo de salida (sin extensión): ").strip()
            uc["encontrar_relaciones"].ejecutar_un_archivo(archivo, dist, salida)

        elif opcion == "3":
            archivo = input("Nombre del archivo de puntos (sin .txt): ").strip()
            puntos = uc["punto_repo"].leer_puntos(archivo)
            ubigeo = int(input("Ubigeo del punto: ").strip())
            try:
                punto = next(p for p in puntos if p.ubigeo == ubigeo)
            except StopIteration:
                print(f"No se encontró un punto con ubigeo={ubigeo}.")
                continue
            uc["generar_poligono"].ejecutar(punto, escribir_kml=True)
            print(f"KML generado en {config.DIR_OUTPUT}{punto.nombre}.kml")

        elif opcion == "4":
            archivo = input("Nombre del archivo de puntos (sin .txt): ").strip()
            salida = input("Prefijo de archivos de salida: ").strip()
            uc["encontrar_torre"].ejecutar(archivo, salida)

        elif opcion == "5":
            conectados = input("Archivo de puntos CONECTADOS (sin .txt): ").strip()
            no_conectados = input("Archivo de puntos NO CONECTADOS (sin .txt): ").strip()
            salida = input("Nombre del archivo de salida (sin extensión): ").strip()
            dist = float(input(f"Distancia máxima en km [{config.DISTANCIA_KM}]: ").strip() or config.DISTANCIA_KM)
            uc["encontrar_relaciones"].ejecutar_dos_archivos_arbol(
                conectados, no_conectados, dist, salida
            )

        elif opcion == "6":
            archivo = input("Nombre del archivo de puntos (sin .txt): ").strip()
            dist = float(input(f"Distancia máxima en km [{config.DISTANCIA_KM}]: ").strip() or config.DISTANCIA_KM)
            salida = input("Prefijo de archivos de salida: ").strip()
            uc["encontrar_relaciones"].ejecutar_clusterizar(archivo, dist, salida)

        else:
            print("Opción no válida, intenta de nuevo.")
