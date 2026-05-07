// ─── Auth types ────────────────────────────────────────────────────────────────

export type User = {
    id: string
    email: string
    hashed_password: string
    is_active: boolean
    is_superuser: boolean
}

// ─── Backend types ─────────────────────────────────────────────────────────────

export interface PuntoData {
    ubigeo: number
    nombre: string
    longitud: number
    latitud: number
    altura_antena: number
    tipo: string
    metros_sobre_nivel_mar: number
    green_asociado: string
    conectado: boolean
}

// ─── Cobertura types ───────────────────────────────────────────────────────────

export interface GeoJsonGeometryLineString {
    type: 'LineString'
    coordinates: [number, number][]
}

export interface GeoJsonGeometryMultiLineString {
    type: 'MultiLineString'
    coordinates: [number, number, number?][][]
}

export interface GeoJsonGeometryPolygon {
    type: 'Polygon'
    coordinates: [number, number][][]
}

export interface GeoJsonGeometryMultiPolygon {
    type: 'MultiPolygon'
    coordinates: [number, number][][][]
}

export type GeoJsonGeometry = GeoJsonGeometryPolygon | GeoJsonGeometryMultiPolygon

export interface GeoJsonFeature {
    type: 'Feature'
    geometry: GeoJsonGeometry | null
    properties: Record<string, unknown>
}

export interface CoberturaViewModel {
    nombre: string
    geojson: GeoJsonFeature
    malla_geojson: GeoJsonFeature
}

export interface CoberturaForm {
    ubigeo: string
    numero_de_ldv: string
    muestras: string
    distancia_km: string
    altura_torre_fantasma: string
}

// ─── Árbol de conexión ─────────────────────────────────────────────────────────

export interface PuntoSinConexionOut {
    ubigeo: number
    nombre: string
    longitud: number
    latitud: number
    tipo: string
}

export interface ArbolResult {
    red_geojson: GeoJsonGeometryMultiLineString
    puntos_sin_conexion: PuntoSinConexionOut[]
}

// ─── Multipolígonos guardados ──────────────────────────────────────────────────

export interface MultipoligonoData {
    id: number
    punto_ubigeo: number
    punto_nombre: string
    geojson: GeoJsonFeature
    numero_de_ldv: number
    muestras: number
    distancia_km: number
    altura_torre_fantasma: number
}

// ─── Redes ─────────────────────────────────────────────────────────────────────

export interface RelacionRedData {
    punto_inicial_ubigeo: number
    punto_final_ubigeo: number
    distancia: number
}

export interface RedData {
    id: number
    nombre: string
    geojson: GeoJsonGeometryMultiLineString
    relaciones: RelacionRedData[]
}
