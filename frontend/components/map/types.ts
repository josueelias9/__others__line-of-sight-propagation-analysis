// ─── Backend types ─────────────────────────────────────────────────────────────

export interface PuntoData {
  ubigeo: number;
  nombre: string;
  longitud: number;
  latitud: number;
  altura_antena: number;
  tipo: string;
  metros_sobre_nivel_mar: number;
  green_asociado: string;
  conectado: boolean;
}

export interface RelacionData {
  punto_inicial: string;
  punto_final: string;
  distancia: number;
}

// ─── Cobertura types ───────────────────────────────────────────────────────────

export interface CoordGeo {
  longitud: number;
  latitud: number;
}

export interface PoligonoViewModel {
  nombre: string;
  coordenadas: CoordGeo[];
}

export interface CeldaMallaViewModel {
  nombre: string;
  coordenadas: CoordGeo[];
}

export interface CoberturaViewModel {
  nombre: string;
  poligonos: PoligonoViewModel[];
  malla: CeldaMallaViewModel[];
}

export interface CoberturaForm {
  ubigeo: string;
  numero_de_ldv: string;
  muestras: string;
  distancia_km: string;
  altura_torre_fantasma: string;
}
