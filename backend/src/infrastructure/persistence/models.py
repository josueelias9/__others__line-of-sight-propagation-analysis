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


class MultipoligonoTable(SQLModel, table=True):
    __tablename__ = "multipoligono"

    id: Optional[int] = Field(default=None, primary_key=True)
    punto_ubigeo: int = Field(foreign_key="punto.ubigeo")
    geojson: dict = Field(default_factory=dict, sa_column=Column(JSONB, nullable=False))
    numero_de_ldv: int = Field(default=0)
    muestras: int = Field(default=0)
    distancia_km: float = Field(default=0.0)
    altura_torre_fantasma: float = Field(default=0.0)


class RedTable(SQLModel, table=True):
    __tablename__ = "red"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    geojson: dict = Field(
        default_factory=dict,
        sa_column=Column(JSONB, nullable=False, server_default="'{}'"),
    )


class RedRelacionTable(SQLModel, table=True):
    __tablename__ = "red_relacion"

    red_id: int = Field(foreign_key="red.id", primary_key=True)
    punto_inicial_ubigeo: int = Field(foreign_key="punto.ubigeo", primary_key=True)
    punto_final_ubigeo: int = Field(foreign_key="punto.ubigeo", primary_key=True)
    distancia: float
