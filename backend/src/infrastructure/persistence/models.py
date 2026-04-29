from typing import Optional

from sqlmodel import Field, SQLModel


class PuntoTable(SQLModel, table=True):
    __tablename__ = "punto"

    ubigeo: int = Field(primary_key=True)
    nombre: str
    longitud: float
    latitud: float
    altura_antena: float
    tipo: str
    metros_sobre_nivel_mar: float
    green_asociado: str = Field(default="")
    conectado: bool = Field(default=False)


class RelacionTable(SQLModel, table=True):
    __tablename__ = "relacion"

    id: Optional[int] = Field(default=None, primary_key=True)
    punto_inicial_id: int = Field(foreign_key="punto.ubigeo")
    punto_final_id: int = Field(foreign_key="punto.ubigeo")
    distancia: float
