# Visualizador de zonas de cobertura en zonas accidentadas

**Problemática:** al instalar antenas de radioenlace en zonas accidentadas, se necesita saber qué cobertura tendrá la antena considerando:
- altura de la antena y del equipo receptor
- zona de Fresnel
- distancia entre antena y receptor

**Alcance:** simplificar el trabajo del analista de cobertura de radioenlaces.

![](imagenes/resultado_1.png)

---

## Ejecución rápida

```bash
# 1. Clonar el repositorio y entrar a la raíz
git clone <url-del-repo>
cd linea-de-vista

# 2. Crear y activar el entorno virtual
python3 -m venv env
source env/bin/activate          # Linux / macOS
# env\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install shapely srtm.py geohelper requests

# 4. Poner el archivo de puntos en la carpeta in/
#    Formato de cada línea (separado por ;):
#    nombre;ubigeo;longitud;latitud;altura_antena;tipo;metros_sobre_nivel_mar

# 5. Ejecutar
python main.py
```

El programa muestra un menú interactivo:

```
1. Asignar alturas a puntos          → lee in/<archivo>.txt, consulta SRTM
2. Encontrar relaciones posibles      → LOS + distancia máxima entre puntos
3. Generar polígono de cobertura      → polígono KML para un punto por ubigeo
4. Buscar ubicación de torre fantasma → intersección de coberturas
5. Árbol de conexión (2 archivos)     → conectados ↔ no conectados
6. Clusterizar puntos                 → agrupa por LOS y distancia
0. Salir
```

Los archivos de salida (`.kml` y `.txt`) quedan en la carpeta `out/`.  
Ábrelos en [Google Earth](https://earth.google.com).

---

## Formato del archivo de entrada

Archivo `.txt` en `in/`, una línea por punto, campos separados por `;`:

```
nombre;ubigeo;longitud;latitud;altura_antena;tipo;metros_sobre_nivel_mar
transporte1;1;-78.426652;-6.884226;15.0;transporte;0
acceso1;2;-78.397267;-6.898882;15.0;acceso;0
```

> El campo `metros_sobre_nivel_mar` puede ser `0`; el caso de uso
> **Asignar alturas** lo completará automáticamente usando SRTM.

---

## Estructura del proyecto

```
linea-de-vista/
├── main.py               ← punto de entrada
├── config.py             ← parámetros y rutas (editar aquí)
├── requirements.txt
├── in/                   ← archivos .txt de entrada
├── out/                  ← archivos .kml/.txt generados
├── proyecto/             ← código original (conservado)
│   ├── srtm/             ← librería SRTM reutilizada por la nueva arquitectura
│   └── srtm.py-master/
└── src/                  ← código refactorizado (Clean Architecture)
    ├── domain/
    │   ├── entities/     ← Punto, Relacion, Red, Estructura, Grafo, Poligonos…
    │   ├── repositories/ ← interfaces: ElevationRepository, PuntoRepository
    │   └── services/     ← LineOfSightService, NetworkAnalysisService, PolygonAnalysisService
    ├── application/
    │   ├── ports/        ← KmlOutputPort, TxtOutputPort
    │   └── use_cases/    ← AsignarAlturas, EncontrarRelaciones,
    │                        GenerarPoligono, EncontrarTorreFantasma
    ├── infrastructure/
    │   ├── elevation/    ← SrtmElevationRepository
    │   ├── persistence/  ← TxtPuntoRepository
    │   └── output/       ← KmlWriter, TxtWriter
    └── interface/
        └── cli.py        ← menú interactivo
```

### Capas de Clean Architecture

| Capa | Responsabilidad | Depende de |
|------|----------------|-----------|
| `domain` | Entidades y lógica de negocio pura | Nadie |
| `application` | Casos de uso y puertos (interfaces) | `domain` |
| `infrastructure` | Acceso a disco, SRTM, KML | `domain`, `application` |
| `interface` | CLI, ensamblado de dependencias | Todas |

---

## SRTM

Los datos de elevación provienen de [tkrajina/srtm.py](https://github.com/tkrajina/srtm.py).  
La carpeta `proyecto/srtm/` contiene la librería; `main.py` la añade automáticamente al path.

---

## Parámetros

Edita `config.py` en la raíz para cambiar rutas y parámetros sin tocar el código:

| Variable | Default | Descripción |
|----------|---------|-------------|
| `DIR_INPUT` | `in/` | Carpeta de archivos de entrada |
| `DIR_OUTPUT` | `out/` | Carpeta de archivos de salida |
| `MUESTRAS` | `200` | Muestras para interpolación de elevación |
| `NUMERO_DE_LDV` | `200` | Direcciones de la grilla polar |
| `DISTANCIA_KM` | `20.0` | Distancia máxima de radioenlace (km) |
| `ALTURA_TORRE_FANTASMA` | `15.0` | Altura del repetidor hipotético (m) |