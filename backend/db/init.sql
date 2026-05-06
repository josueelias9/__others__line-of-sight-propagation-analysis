-- Schema for the Line-of-Sight application.
-- Tables are created here; initial data is loaded by the backend-init container
-- running app/initial_data.py via prestart.sh.

CREATE TABLE IF NOT EXISTS users (
    id               SERIAL PRIMARY KEY,
    email            VARCHAR(255) NOT NULL UNIQUE,
    hashed_password  VARCHAR(255) NOT NULL,
    is_active        BOOLEAN      NOT NULL DEFAULT TRUE,
    is_superuser     BOOLEAN      NOT NULL DEFAULT FALSE
);

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
    conectado             BOOLEAN      NOT NULL DEFAULT FALSE,
    user_id               INTEGER REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS multipoligono (
    id                    INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    punto_ubigeo          INTEGER          NOT NULL REFERENCES punto(ubigeo) ON DELETE CASCADE,
    geojson               JSONB            NOT NULL,
    numero_de_ldv         INTEGER          NOT NULL DEFAULT 0,
    muestras              INTEGER          NOT NULL DEFAULT 0,
    distancia_km          DOUBLE PRECISION NOT NULL DEFAULT 0,
    altura_torre_fantasma DOUBLE PRECISION NOT NULL DEFAULT 0,
    user_id               INTEGER REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS red (
    id      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre  VARCHAR(100) NOT NULL,
    geojson JSONB        NOT NULL DEFAULT '{}',
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS red_punto (
    red_id              INTEGER NOT NULL REFERENCES red(id) ON DELETE CASCADE,
    punto_inicial_ubigeo INTEGER NOT NULL REFERENCES punto(ubigeo) ON DELETE CASCADE,
    punto_final_ubigeo   INTEGER NOT NULL REFERENCES punto(ubigeo) ON DELETE CASCADE,
    distancia            DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (red_id, punto_inicial_ubigeo, punto_final_ubigeo)
);
