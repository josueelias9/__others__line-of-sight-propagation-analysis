from __future__ import annotations

from typing import Protocol


class CsvDataLoaderPort(Protocol):
    def load(self, filename: str) -> list[dict[str, str]]: ...
