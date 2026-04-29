from typing import Optional

from sqlmodel import Field, SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB


class PuntoTypeTable(SQLModel, table=True):
    __tablename__ = "punto_type"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)


class PuntoTable(SQLModel, table=True):
    __tablename__ = "punto"

    ubigeo: int = Field(primary_key=True)
    nombre: str
    longitud: float
    latitud: float
    altura_antena: float
    punto_type_id: int = Field(foreign_key="punto_type.id")
    metros_sobre_nivel_mar: float
    green_asociado: str = Field(default="")
    conectado: bool = Field(default=False)


class RelacionTable(SQLModel, table=True):
    __tablename__ = "relacion"

    id: Optional[int] = Field(default=None, primary_key=True)
    punto_inicial_id: int = Field(foreign_key="punto.ubigeo")
    punto_final_id: int = Field(foreign_key="punto.ubigeo")
    distancia: float


class MultipoligonoTable(SQLModel, table=True):
    __tablename__ = "multipoligono"

    id: Optional[int] = Field(default=None, primary_key=True)
    punto_ubigeo: int = Field(foreign_key="punto.ubigeo")
    geojson: dict = Field(default_factory=dict, sa_column=Column(JSONB, nullable=False))
