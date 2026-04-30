import sys
from typing import List

from application.interface.ports.geometry import AreaGeometrica
from application.interface.ports.output import KmlOutputPort
from domain.entities.estructura import Estructura
from domain.entities.poligonos import Poligonos
from domain.entities.punto import Punto
from domain.entities.relacion import Relacion
from interface.presenters.cobertura_presenter import CoberturaViewModel

# ── plantillas KML ────────────────────────────────────────────────────────────

_KML_HEADER = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<kml xmlns="http://www.opengis.net/kml/2.2"'
    ' xmlns:gx="http://www.google.com/kml/ext/2.2"'
    ' xmlns:kml="http://www.opengis.net/kml/2.2"'
    ' xmlns:atom="http://www.w3.org/2005/Atom">\n'
)

_KML_FOOTER = "</kml>\n"


class KmlWriter(KmlOutputPort):
    """
    Adaptador de infraestructura para escritura de archivos KML.

    Implementa KmlOutputPort.
    Pertenece a la capa de Infraestructura.
    """

    def __init__(self, directorio: str) -> None:
        self._directorio = directorio

    # ------------------------------------------------------------------ KmlOutputPort

    def escribir_rutas(
        self,
        relaciones: List[Relacion],
        nombre: str,
        altitud_absoluta: bool = True,
    ) -> None:
        tipo = "absolute" if altitud_absoluta else ""
        ruta = self._directorio + nombre + ".kml"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(_KML_HEADER)
            f.write(
                "<Document>\n"
                "\t<name>rutas.kml</name>\n"
                '\t<Style id="sh_ylw-pushpin">\n'
                "\t\t<LineStyle><color>ff00ff00</color></LineStyle>\n"
                "\t</Style>\n"
                "\t<Folder>\n"
                "\t\t<name>Mis sitios</name><open>1</open>\n"
            )
            for re in relaciones:
                pi, pf = re.punto_inicial, re.punto_final
                alt_i = pi.metros_sobre_nivel_mar + pi.altura_antena
                alt_f = pf.metros_sobre_nivel_mar + pf.altura_antena
                dist = str(re.distancia)[:5]
                f.write(
                    "<Placemark>\n"
                    f"\t<name>{pi.nombre}->{pf.nombre}</name>\n"
                    "<description>"
                    f"inicio:\t{pi.nombre}\nfin:\t{pf.nombre}\ndistancia:\t{dist} km\n"
                    "</description>\n"
                    "\t<LineString>\n"
                    "\t\t<tessellate>1</tessellate>\n"
                    f"\t\t<altitudeMode>{tipo}</altitudeMode>\n"
                    "\t\t<coordinates>\n"
                    f"{pi.longitud},{pi.latitud},{alt_i} "
                    f"{pf.longitud},{pf.latitud},{alt_f}"
                    "\t\t</coordinates>\n"
                    "\t</LineString>\n"
                    "</Placemark>\n"
                )
            f.write("\t</Folder>\n</Document>\n")
            f.write(_KML_FOOTER)

    def escribir_puntos(self, puntos: List[Punto], nombre: str) -> None:
        ruta = self._directorio + nombre + ".kml"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(_KML_HEADER)
            f.write(
                "<Document>\n"
                f"\t<name>{nombre}.kml</name>\n"
                '\t<Style id="s_ylw-pushpin">\n'
                '\t\t<IconStyle><scale>1.1</scale>'
                "<Icon><href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href></Icon>"
                "</IconStyle>\n"
                "\t</Style>\n"
                "\t<Folder><name>Mis sitios</name><open>1</open>\n"
            )
            for p in puntos:
                f.write(
                    "\t\t<Placemark>\n"
                    f"\t\t\t<name>{p.nombre}</name>\n"
                    "\t\t\t<description>"
                    f"altura:\t{p.altura_antena}\nidentificador:\t{p.ubigeo}\ntipo:\t{p.tipo}"
                    "</description>\n"
                    '\t\t\t<styleUrl>#s_ylw-pushpin</styleUrl>\n'
                    "\t\t\t<Point>\n"
                    f"\t\t\t\t<coordinates>{p.longitud},{p.latitud},{p.altura_antena}</coordinates>\n"
                    "\t\t\t</Point>\n"
                    "\t\t</Placemark>\n"
                )
            f.write("\t</Folder>\n</Document>\n")
            f.write(_KML_FOOTER)

    def escribir_estructura_puntos(
        self,
        matriz_de_puntos: List[List[Punto]],
        nombre: str,
        forma: str = "arrow",
    ) -> None:
        ruta = self._directorio + nombre + ".kml"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(_KML_HEADER)
            f.write(
                "<Document>\n"
                "\t<name>estructuraLineaDeVista.kml</name>\n"
                '\t<Style id="s_ylw-pushpin">\n'
                f'\t\t<IconStyle><scale>1.1</scale><Icon>'
                f'<href>http://maps.google.com/mapfiles/kml/shapes/{forma}.png</href>'
                "</Icon></IconStyle>\n"
                "\t</Style>\n"
                "\t<Folder><name>Mis sitios</name><open>1</open>\n"
            )
            for i, fila in enumerate(matriz_de_puntos):
                for j, p in enumerate(fila):
                    f.write(
                        "\t\t<Placemark>\n"
                        f"\t\t\t<name>{i}-{j}</name>\n"
                        '\t\t\t<styleUrl>#s_ylw-pushpin</styleUrl>\n'
                        "\t\t\t<Point>\n"
                        f"\t\t\t\t<coordinates>{p.longitud},{p.latitud},{p.altura_antena}</coordinates>\n"
                        "\t\t\t</Point>\n"
                        "\t\t</Placemark>\n"
                    )
            f.write("\t</Folder>\n</Document>\n")
            f.write(_KML_FOOTER)

    def escribir_malla_cobertura(
        self,
        estructura: Estructura,
        nombre: str,
    ) -> None:
        ruta = self._directorio + nombre + ".kml"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(_KML_HEADER)
            f.write(
                "<Document>\n"
                "\t<name>cuadrilateros.kml</name>\n"
                '\t<Style id="sh_ylw-pushpin">\n'
                "\t\t<PolyStyle><color>80ffffff</color></PolyStyle>\n"
                "\t</Style>\n"
                "\t<Folder><name>Lugares temporales</name><open>1</open>\n"
            )
            fg = estructura.estructura_figuras_geome
            ultimo_i = len(fg) - 1
            for i in range(estructura.n):
                for j in range(1, estructura.m):
                    if estructura.estructura_matricial[i][j] != 1:
                        continue
                    if i == ultimo_i:
                        p00, p0m = fg[i][j], fg[i][j - 1]
                        ppm, pp0 = fg[0][j - 1], fg[0][j]
                    else:
                        p00, p0m = fg[i][j], fg[i][j - 1]
                        ppm, pp0 = fg[i + 1][j - 1], fg[i + 1][j]
                    coords = (
                        f"{p00.longitud},{p00.latitud},0 "
                        f"{p0m.longitud},{p0m.latitud},0 "
                        f"{ppm.longitud},{ppm.latitud},0 "
                        f"{pp0.longitud},{pp0.latitud},0 "
                        f"{p00.longitud},{p00.latitud},0"
                    )
                    f.write(
                        f'\t\t<Placemark>\n'
                        f'\t\t\t<name>poligono{i}-{j}</name>\n'
                        '\t\t\t<styleUrl>#sh_ylw-pushpin</styleUrl>\n'
                        "\t\t\t<Polygon><tessellate>1</tessellate>\n"
                        "\t\t\t\t<outerBoundaryIs><LinearRing>\n"
                        f"\t\t\t\t\t<coordinates>{coords}</coordinates>\n"
                        "\t\t\t\t</LinearRing></outerBoundaryIs>\n"
                        "\t\t\t</Polygon>\n"
                        "\t\t</Placemark>\n"
                    )
            f.write("\t</Folder>\n</Document>\n")
            f.write(_KML_FOOTER)

    def escribir_poligonos(
        self,
        poligonos: Poligonos,
        estructura: Estructura,
        nombre: str,
    ) -> None:
        ruta = self._directorio + nombre + ".kml"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(_KML_HEADER)
            f.write(
                "<Document>\n"
                f"\t<name>{nombre}.kml</name>\n"
                '\t<Style id="s_ylw-pushpin">\n'
                '\t\t<IconStyle><scale>1.1</scale></IconStyle>\n'
                "\t</Style>\n"
                "\t<Folder><name>ww</name><open>1</open>\n"
            )
            for idx, poli in enumerate(poligonos.lista_de_poligonitos):
                f.write(
                    f"<Placemark><name>{idx}</name>\n"
                    '\t<styleUrl>#s_ylw-pushpin</styleUrl>\n'
                    "\t<Polygon><tessellate>1</tessellate>\n"
                    "\t\t<outerBoundaryIs><LinearRing><coordinates>\n"
                )
                for coord in poli.lista_de_puntos:
                    pt = estructura.estructura_figuras_geome[coord[0]][coord[1]]
                    f.write(f"{pt.longitud},{pt.latitud},0 ")
                f.write(
                    "\n\t\t</coordinates></LinearRing></outerBoundaryIs>\n"
                    "\t</Polygon>\n</Placemark>\n"
                )
            f.write("\t</Folder>\n</Document>\n")
            f.write(_KML_FOOTER)

    def escribir_area(self, area: AreaGeometrica, nombre: str) -> None:
        ruta = self._directorio + nombre + ".kml"

        with open(ruta, "w", encoding="utf-8") as f:
            f.write(_KML_HEADER)
            f.write(
                "<Placemark>\n"
                "\t<Style><LineStyle><color>ff0000ff</color></LineStyle></Style>\n"
            )

            if len(area.anillos) > 1:
                f.write("\t<MultiGeometry>\n")
                for poligono in area.anillos:
                    f.write(
                        "\t\t<Polygon>\n"
                        "\t\t\t<outerBoundaryIs><LinearRing><coordinates>\n"
                    )
                    for c in poligono[0]:
                        f.write(f"{c[0]},{c[1]} ")
                    f.write("</coordinates></LinearRing></outerBoundaryIs>\n")
                    for anillo in poligono[1:]:
                        f.write("\t\t\t<innerBoundaryIs><LinearRing><coordinates>\n")
                        for c in anillo:
                            f.write(f"{c[0]},{c[1]} ")
                        f.write("</coordinates></LinearRing></innerBoundaryIs>\n")
                    f.write("\t\t</Polygon>\n")
                f.write("\t</MultiGeometry>\n")
            elif area.anillos:
                poligono = area.anillos[0]
                f.write(
                    "\t<Polygon>\n"
                    "\t\t<outerBoundaryIs><LinearRing><coordinates>\n"
                )
                for c in poligono[0]:
                    f.write(f"{c[0]},{c[1]} ")
                f.write("</coordinates></LinearRing></outerBoundaryIs>\n")
                for anillo in poligono[1:]:
                    f.write("\t\t<innerBoundaryIs><LinearRing><coordinates>\n")
                    for c in anillo:
                        f.write(f"{c[0]},{c[1]} ")
                    f.write("</coordinates></LinearRing></innerBoundaryIs>\n")
                f.write("\t</Polygon>\n")

            f.write("</Placemark>\n")
            f.write(_KML_FOOTER)

    # ------------------------------------------------------------------ adaptador de ViewModel

    def escribir_cobertura(self, viewmodel: CoberturaViewModel) -> None:
        """
        Punto de entrada para el presenter de cobertura.

        Escribe dos archivos KML a partir del CoberturaViewModel:
          - <nombre>.kml       : polígonos de cobertura.
          - <nombre>_malla.kml : cuadriláteros de la malla polar.
        """
        self._escribir_poligonos_vm(viewmodel, viewmodel.nombre)
        self._escribir_malla_vm(viewmodel, viewmodel.nombre + "_malla")

    def _escribir_poligonos_vm(self, viewmodel: CoberturaViewModel, nombre: str) -> None:
        ruta = self._directorio + nombre + ".kml"
        geom = viewmodel.geojson.get("geometry") or {}
        tipo = geom.get("type", "")
        coords = geom.get("coordinates", [])

        # Normalizar a lista de polígonos (cada uno es lista de anillos)
        if tipo == "Polygon":
            poligonos_coords = [coords]
        elif tipo == "MultiPolygon":
            poligonos_coords = coords
        else:
            poligonos_coords = []

        with open(ruta, "w", encoding="utf-8") as f:
            f.write(_KML_HEADER)
            f.write(
                "<Document>\n"
                f"\t<name>{nombre}.kml</name>\n"
                '\t<Style id="s_ylw-pushpin">\n'
                '\t\t<IconStyle><scale>1.1</scale></IconStyle>\n'
                "\t</Style>\n"
                "\t<Folder><name>ww</name><open>1</open>\n"
            )
            for idx, anillos in enumerate(poligonos_coords):
                exterior = anillos[0]
                f.write(
                    f"<Placemark><name>{idx}</name>\n"
                    '\t<styleUrl>#s_ylw-pushpin</styleUrl>\n'
                    "\t<Polygon><tessellate>1</tessellate>\n"
                    "\t\t<outerBoundaryIs><LinearRing><coordinates>\n"
                )
                for lng, lat in exterior:
                    f.write(f"{lng},{lat},0 ")
                f.write(
                    "\n\t\t</coordinates></LinearRing></outerBoundaryIs>\n"
                )
                for hueco in anillos[1:]:
                    f.write("\t\t<innerBoundaryIs><LinearRing><coordinates>\n")
                    for lng, lat in hueco:
                        f.write(f"{lng},{lat},0 ")
                    f.write("\n\t\t</coordinates></LinearRing></innerBoundaryIs>\n")
                f.write("\t</Polygon>\n</Placemark>\n")
            f.write("\t</Folder>\n</Document>\n")
            f.write(_KML_FOOTER)

    def _escribir_malla_vm(self, viewmodel: CoberturaViewModel, nombre: str) -> None:
        ruta = self._directorio + nombre + ".kml"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(_KML_HEADER)
            f.write(
                "<Document>\n"
                "\t<name>cuadrilateros.kml</name>\n"
                '\t<Style id="sh_ylw-pushpin">\n'
                "\t\t<PolyStyle><color>80ffffff</color></PolyStyle>\n"
                "\t</Style>\n"
                "\t<Folder><name>Lugares temporales</name><open>1</open>\n"
            )
            for celda in viewmodel.malla:
                coords = " ".join(
                    f"{c.longitud},{c.latitud},0" for c in celda.coordenadas
                )
                f.write(
                    f'\t\t<Placemark>\n'
                    f'\t\t\t<name>{celda.nombre}</name>\n'
                    '\t\t\t<styleUrl>#sh_ylw-pushpin</styleUrl>\n'
                    "\t\t\t<Polygon><tessellate>1</tessellate>\n"
                    "\t\t\t\t<outerBoundaryIs><LinearRing>\n"
                    f"\t\t\t\t\t<coordinates>{coords}</coordinates>\n"
                    "\t\t\t\t</LinearRing></outerBoundaryIs>\n"
                    "\t\t\t</Polygon>\n"
                    "\t\t</Placemark>\n"
                )
            f.write("\t</Folder>\n</Document>\n")
            f.write(_KML_FOOTER)

    # ------------------------------------------------------------------ consola helper
    # TODO esto no tiene nada que con KML, revisar
    def imprimir_matriz(self, matriz: List[List[int]]) -> None:
        """Imprime la matriz de estado en consola (creciendo de abajo a arriba)."""
        filas = len(matriz)
        for i in range(filas - 1, -1, -1):
            sys.stdout.write(" ".join(str(v) for v in matriz[i]) + "\n")
