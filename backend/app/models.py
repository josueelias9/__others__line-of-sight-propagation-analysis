from typing import Optional

from sqlmodel import Field, SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

from typing import Any, Dict, List

from app.core import config

# ── ORM tables ────────────────────────────────────────────────────────────────


class UserTable(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: Optional[str] = None
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
        sa_column=Column(JSONB, nullable=False, server_default="{}"),
    )
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")


class RedPuntoTable(SQLModel, table=True):
    __tablename__ = "red_punto"

    red_id: int = Field(foreign_key="red.id", primary_key=True)
    punto_inicial_ubigeo: int = Field(foreign_key="punto.ubigeo", primary_key=True)
    punto_final_ubigeo: int = Field(foreign_key="punto.ubigeo", primary_key=True)
    distancia: float


# ── Pydantic models ───────────────────────────────────────────────────────────

from pydantic import BaseModel


class PuntoOut(BaseModel):
    ubigeo: int
    nombre: str
    longitud: float
    latitud: float
    altura_antena: float
    tipo: str
    metros_sobre_nivel_mar: float
    green_asociado: str
    conectado: bool


class PuntoIn(BaseModel):
    nombre: str
    longitud: float
    latitud: float
    altura_antena: float = 15.0
    tipo: str
    green_asociado: Optional[str] = ""


class CoberturaRequest(BaseModel):
    ubigeo: int
    numero_de_ldv: int = Field(default=config.NUMERO_DE_LDV, ge=100, le=300)
    muestras: int = Field(default=config.MUESTRAS, ge=100, le=300)
    distancia_km: float = Field(default=config.DISTANCIA_KM, ge=1, le=15)
    altura_torre_fantasma: float = Field(
        default=config.ALTURA_TORRE_FANTASMA, ge=5, le=20
    )


class CoberturaGuardadaOut(BaseModel):
    id: int
    punto_ubigeo: int
    punto_nombre: str
    geojson: Dict[str, Any]
    numero_de_ldv: int
    muestras: int
    distancia_km: float
    altura_torre_fantasma: float


class RelacionRedOut(BaseModel):
    punto_inicial_ubigeo: int
    punto_final_ubigeo: int
    distancia: float


class RedOut(BaseModel):
    id: int
    nombre: str
    geojson: Dict[str, Any]
    relaciones: List[RelacionRedOut]


class ArbolRequest(BaseModel):
    tipo_conectados: str
    tipo_no_conectados: str
    distancia_maxima: float = config.DISTANCIA_KM
    muestras: int = config.MUESTRAS
    nombre_red: str = ""


class PuntoSinConexionOut(BaseModel):
    ubigeo: int
    nombre: str
    longitud: float
    latitud: float
    tipo: str


class ArbolResponse(BaseModel):
    red_geojson: Dict[str, Any]
    puntos_sin_conexion: List[PuntoSinConexionOut]
