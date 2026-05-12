import csv
import sys
from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "app" / "data"

# Some CSV fields (e.g. GeoJSON columns) can exceed the default 131072-byte limit.
csv.field_size_limit(sys.maxsize)


class CsvDataLoader:
    """Implementación de CsvDataLoaderPort que lee archivos CSV desde disco."""

    def __init__(self, data_dir: Path = _DATA_DIR) -> None:
        self._data_dir = data_dir

    def load(self, filename: str) -> list[dict[str, str]]:
        """
        Lee el archivo *filename*.csv de *data_dir* y devuelve la lista de filas
        representadas como dicts de strings (tal como las devuelve csv.DictReader).
        """
        csv_file = self._data_dir / f"{filename}.csv"
        with csv_file.open(newline="", encoding="utf-8") as fh:
            return [dict(row) for row in csv.DictReader(fh)]
