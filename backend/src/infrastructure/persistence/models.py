from typing import Optional

from sqlmodel import Field, SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB


# ── ORM tables ────────────────────────────────────────────────────────────────

class UserTable(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)


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
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")


class MultipoligonoTable(SQLModel, table=True):
    __tablename__ = "multipoligono"

    id: Optional[int] = Field(default=None, primary_key=True)
    punto_ubigeo: int = Field(foreign_key="punto.ubigeo")
    geojson: dict = Field(default_factory=dict, sa_column=Column(JSONB, nullable=False))
    numero_de_ldv: int = Field(default=0)
    muestras: int = Field(default=0)
    distancia_km: float = Field(default=0.0)
    altura_torre_fantasma: float = Field(default=0.0)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")


class RedTable(SQLModel, table=True):
    __tablename__ = "red"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    geojson: dict = Field(
        default_factory=dict,
        sa_column=Column(JSONB, nullable=False, server_default="'{}'"),
    )
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")


class RedPuntoTable(SQLModel, table=True):
    __tablename__ = "red_punto"

    red_id: int = Field(foreign_key="red.id", primary_key=True)
    punto_inicial_ubigeo: int = Field(foreign_key="punto.ubigeo", primary_key=True)
    punto_final_ubigeo: int = Field(foreign_key="punto.ubigeo", primary_key=True)
    distancia: float
