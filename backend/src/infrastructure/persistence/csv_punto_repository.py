import logging
import csv
from typing import List, Optional

from domain.entities.punto import Punto
from domain.entities.relacion import Relacion
from application.gateways.punto_gateway import PuntoGateway

logger = logging.getLogger(__name__)


class CsvPuntoRepository(PuntoGateway):
    """
    Adaptador de infraestructura que implementa PuntoGateway
    leyendo archivos CSV con cabecera.

    Formato esperado (9 columnas):
        nombre,ubigeo,longitud,latitud,altura_antena,tipo,metros_sobre_nivel_mar,green_asociado,conectado

    Pertenece a la capa de Infraestructura.
    """

    def __init__(self, directorio: str) -> None:
        # directorio debe terminar con '/'
        self._directorio = directorio

    # ------------------------------------------------------------------ PuntoGateway

    def leer_puntos(self, tipo: Optional[str] = None) -> List[Punto]:
        puntos: List[Punto] = []
        ruta = self._directorio + "punto.csv"
        with open(ruta, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for numero_linea, fila in enumerate(reader, start=2):
                try:
                    punto = Punto(
                        nombre=fila["nombre"],
                        ubigeo=int(fila["ubigeo"]),
                        longitud=float(fila["longitud"]),
                        latitud=float(fila["latitud"]),
                        altura_antena=float(fila["altura_antena"]),
                        tipo=fila["tipo"],
                        metros_sobre_nivel_mar=float(fila["metros_sobre_nivel_mar"]),
                    )
                    punto.green_asociado = fila.get("green_asociado", "").strip()
                    punto.conectado = fila.get("conectado", "False").strip().lower() == "true"
                    puntos.append(punto)
                except (KeyError, ValueError) as exc:
                    logger.warning("línea %d ignorada: %s", numero_linea, exc)
        if tipo is not None:
            puntos = [p for p in puntos if p.tipo == tipo]
        return puntos

    def obtener_punto_por_ubigeo(self, ubigeo: int) -> Punto:
        try:
            return next(p for p in self.leer_puntos() if p.ubigeo == ubigeo)
        except StopIteration:
            raise ValueError(f"No se encontró un punto con ubigeo={ubigeo}")

    def leer_relaciones(self) -> List[Relacion]:
        puntos_dict = {p.nombre: p for p in self.leer_puntos()}
        relaciones: List[Relacion] = []
        ruta = self._directorio + "relacion.csv"
        with open(ruta, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for numero_linea, fila in enumerate(reader, start=2):
                try:
                    p_ini = puntos_dict[fila["punto_inicial_id"]]
                    p_fin = puntos_dict[fila["punto_final_id"]]
                    relaciones.append(Relacion(p_ini, p_fin))
                except (KeyError, ValueError) as exc:
                    logger.warning("línea %d ignorada: %s", numero_linea, exc)
        return relaciones

    def guardar_puntos(self, puntos: List[Punto]) -> None:
        ruta = self._directorio + "punto.csv"
        _CAMPOS = [
            "nombre", "ubigeo", "longitud", "latitud",
            "altura_antena", "tipo", "metros_sobre_nivel_mar", "green_asociado", "conectado",
        ]
        with open(ruta, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=_CAMPOS)
            writer.writeheader()
            for p in puntos:
                writer.writerow({
                    "nombre": p.nombre,
                    "ubigeo": p.ubigeo,
                    "longitud": p.longitud,
                    "latitud": p.latitud,
                    "altura_antena": p.altura_antena,
                    "tipo": p.tipo,
                    "metros_sobre_nivel_mar": p.metros_sobre_nivel_mar,
                    "green_asociado": p.green_asociado,
                    "conectado": p.conectado,
                })

    def guardar_relaciones(self, relaciones: List[Relacion]) -> None:
        ruta = self._directorio + "relacion.csv"
        _CAMPOS = ["punto_inicial_id", "punto_final_id", "distancia"]
        with open(ruta, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=_CAMPOS)
            writer.writeheader()
            for r in relaciones:
                writer.writerow({
                    "punto_inicial_id": r.punto_inicial.ubigeo,
                    "punto_final_id": r.punto_final.ubigeo,
                    "distancia": r.distancia,
                })

    def actualizar_conectado(self, puntos: List[Punto]) -> None:
        """Lee punto.csv completo, parchea solo la columna `conectado` para los
        ubigeos presentes en *puntos*, y reescribe el archivo."""
        conectado_map = {p.ubigeo: p.conectado for p in puntos}
        todos = self.leer_puntos()
        for p in todos:
            if p.ubigeo in conectado_map:
                p.conectado = conectado_map[p.ubigeo]
        self.guardar_puntos(todos)

    def agregar_punto(self, punto: Punto) -> Punto:
        """Agrega un nuevo Punto al CSV asignándole el siguiente ubigeo disponible."""
        todos = self.leer_puntos()
        siguiente_ubigeo = max((p.ubigeo for p in todos), default=0) + 1
        punto.ubigeo = siguiente_ubigeo
        todos.append(punto)
        self.guardar_puntos(todos)
        return punto
