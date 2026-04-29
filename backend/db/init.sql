-- Schema for the Line-of-Sight application.
-- Tables are created here; initial data is loaded by the backend-init container
-- running app/initial_data.py via prestart.sh.

CREATE TABLE IF NOT EXISTS punto_type (
    id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS punto (
    ubigeo                INTEGER PRIMARY KEY,
    nombre                VARCHAR(100) NOT NULL,
    longitud              DOUBLE PRECISION NOT NULL,
    latitud               DOUBLE PRECISION NOT NULL,
    altura_antena         DOUBLE PRECISION NOT NULL,
    punto_type_id         INTEGER NOT NULL REFERENCES punto_type(id),
    metros_sobre_nivel_mar DOUBLE PRECISION NOT NULL,
    green_asociado        VARCHAR(100) NOT NULL DEFAULT '',
    conectado             BOOLEAN      NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS relacion (
    id                INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    punto_inicial_id  INTEGER NOT NULL REFERENCES punto(ubigeo) ON DELETE CASCADE,
    punto_final_id    INTEGER NOT NULL REFERENCES punto(ubigeo) ON DELETE CASCADE,
    distancia         DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS multipoligono (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    punto_ubigeo INTEGER NOT NULL REFERENCES punto(ubigeo) ON DELETE CASCADE,
    geojson      JSONB NOT NULL
);
