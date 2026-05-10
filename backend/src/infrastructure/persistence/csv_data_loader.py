import csv
import sys
from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "app" / "data"

# Some CSV fields (e.g. GeoJSON columns) can exceed the default 131072-byte limit.
csv.field_size_limit(sys.maxsize)


# TODO: it seems to me that this function load all csv files. This should receive as parameter which file to process, and return only the data of that file. Otherwise, if we have many csv files, we will be loading all of them into memory when we only need one.
def load_csv_data(data_dir: Path = _DATA_DIR) -> dict[str, list[dict[str, str]]]:
    """
    Lee todos los archivos *.csv de *data_dir* y devuelve un dict cuya clave
    es el nombre del archivo (sin extensión) y cuyo valor es la lista de filas
    representadas como dicts de strings (tal como las devuelve csv.DictReader).

    Es adaptable: cualquier CSV nuevo que se coloque en la carpeta será
    incluido automáticamente.
    """
    result: dict[str, list[dict[str, str]]] = {}
    for csv_file in sorted(data_dir.glob("*.csv")):
        with csv_file.open(newline="", encoding="utf-8") as fh:
            result[csv_file.stem] = [dict(row) for row in csv.DictReader(fh)]
    return result
