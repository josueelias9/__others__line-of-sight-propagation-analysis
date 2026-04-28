"use client";

import { useEffect, useRef, useState } from "react";
import {
  APIProvider,
  Map,
  AdvancedMarker,
  useMap,
  useApiIsLoaded,
} from "@vis.gl/react-google-maps";

// ─── Backend types ─────────────────────────────────────────────────────────────

interface PuntoData {
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

interface RelacionData {
  punto_inicial: string;
  punto_final: string;
  distancia: number;
}

// ─── Cobertura types ───────────────────────────────────────────────────────────

interface CoordGeo {
  longitud: number;
  latitud: number;
}

interface PoligonoViewModel {
  nombre: string;
  coordenadas: CoordGeo[];
}

interface CeldaMallaViewModel {
  nombre: string;
  coordenadas: CoordGeo[];
}

interface CoberturaViewModel {
  nombre: string;
  poligonos: PoligonoViewModel[];
  malla: CeldaMallaViewModel[];
}

interface CoberturaForm {
  ubigeo: string;
  numero_de_ldv: string;
  muestras: string;
  distancia_km: string;
  altura_torre_fantasma: string;
}

// ─── Config ────────────────────────────────────────────────────────────────────

// Centro aproximado del área de datos (Chachapoyas, Perú)
const DEFAULT_CENTER = { lat: -6.91, lng: -78.44 };
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

// ─── Map overlays: relaciones como polilíneas ─────────────────────────────────

function MapOverlays({ puntos, relaciones }: { puntos: PuntoData[]; relaciones: RelacionData[] }) {
  const map = useMap();
  const linesRef = useRef<google.maps.Polyline[]>([]);

  useEffect(() => {
    if (!map) return;

    linesRef.current.forEach((l) => l.setMap(null));
    linesRef.current = [];

    const idx: Record<string, PuntoData> = {};
    puntos.forEach((p) => { idx[p.nombre] = p; });

    relaciones.forEach((r) => {
      const ini = idx[r.punto_inicial];
      const fin = idx[r.punto_final];
      if (!ini || !fin) return;
      const line = new google.maps.Polyline({
        path: [
          { lat: ini.latitud, lng: ini.longitud },
          { lat: fin.latitud, lng: fin.longitud },
        ],
        geodesic: true,
        strokeColor: "#22D3EE",
        strokeOpacity: 0.9,
        strokeWeight: 3,
        map,
      });
      linesRef.current.push(line);
    });

    return () => {
      linesRef.current.forEach((l) => l.setMap(null));
      linesRef.current = [];
    };
  }, [map, puntos, relaciones]);

  return null;
}

// ─── Cobertura overlays ────────────────────────────────────────────────────────

function CoberturaOverlays({ data }: { data: CoberturaViewModel | null }) {
  const map = useMap();
  const mallaCellsRef = useRef<google.maps.Polygon[]>([]);
  const poligonosRef = useRef<google.maps.Polygon[]>([]);

  useEffect(() => {
    mallaCellsRef.current.forEach((p) => p.setMap(null));
    poligonosRef.current.forEach((p) => p.setMap(null));
    mallaCellsRef.current = [];
    poligonosRef.current = [];

    if (!map || !data) return;

    mallaCellsRef.current = data.malla.map(
      (celda) =>
        new google.maps.Polygon({
          paths: celda.coordenadas.map((c) => ({ lat: c.latitud, lng: c.longitud })),
          strokeColor: "#34D399",
          strokeOpacity: 0.4,
          strokeWeight: 1,
          fillColor: "#34D399",
          fillOpacity: 0.25,
          map,
        })
    );

    poligonosRef.current = data.poligonos.map(
      (poli) =>
        new google.maps.Polygon({
          paths: poli.coordenadas.map((c) => ({ lat: c.latitud, lng: c.longitud })),
          strokeColor: "#FBBF24",
          strokeOpacity: 0.9,
          strokeWeight: 2,
          fillOpacity: 0,
          map,
        })
    );

    return () => {
      mallaCellsRef.current.forEach((p) => p.setMap(null));
      poligonosRef.current.forEach((p) => p.setMap(null));
    };
  }, [map, data]);

  return null;
}

// ─── Cobertura panel (sidebar form) ───────────────────────────────────────────

interface CoberturaPanel {
  puntos: PuntoData[];
  onResult: (data: CoberturaViewModel) => void;
}

function CoberturaPanel({ puntos, onResult }: CoberturaPanel) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [form, setForm] = useState<CoberturaForm>({
    ubigeo: "",
    numero_de_ldv: "72",
    muestras: "100",
    distancia_km: "15",
    altura_torre_fantasma: "15",
  });

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const body = {
        ubigeo: parseInt(form.ubigeo),
        numero_de_ldv: parseInt(form.numero_de_ldv),
        muestras: parseInt(form.muestras),
        distancia_km: parseFloat(form.distancia_km),
        altura_torre_fantasma: parseFloat(form.altura_torre_fantasma),
      };

      const res = await fetch(`${BACKEND_URL}/api/cobertura`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (!res.ok) {
        const detail = await res.text();
        throw new Error(`HTTP ${res.status}: ${detail}`);
      }

      const data: CoberturaViewModel = await res.json();
      onResult(data);
      setOpen(false);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  }

  const paramFields: { name: keyof CoberturaForm; label: string }[] = [
    { name: "numero_de_ldv", label: "Líneas de vista" },
    { name: "muestras", label: "Muestras" },
    { name: "distancia_km", label: "Distancia (km)" },
    { name: "altura_torre_fantasma", label: "Torre fantasma (m)" },
  ];

  return (
    <div className="absolute top-5 right-5 z-10 w-72 rounded-2xl overflow-hidden shadow-2xl">
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full bg-gray-900/90 backdrop-blur-xl border border-white/10 px-5 py-4 text-left"
      >
        <span className="text-white font-bold text-base tracking-tight">
          Análisis de Cobertura
        </span>
        <p className="text-gray-400 text-xs mt-0.5">
          {open ? "▲ Cerrar" : "▼ Configurar y generar"}
        </p>
      </button>

      {open && (
        <>
          <div className="h-px bg-white/10" />
          <form
            onSubmit={handleSubmit}
            className="bg-gray-900/85 backdrop-blur-xl border-x border-b border-white/10 rounded-b-2xl px-5 py-4 space-y-3 max-h-[70vh] overflow-y-auto"
          >
            {/* Selector de punto */}
            <div>
              <label className="text-gray-400 text-xs block mb-0.5">Punto</label>
              <select
                name="ubigeo"
                value={form.ubigeo}
                onChange={handleChange}
                required
                className="w-full bg-gray-800/60 border border-white/10 rounded-lg px-3 py-1.5 text-white text-sm focus:outline-none focus:ring-1 focus:ring-emerald-400/60"
              >
                <option value="" disabled>Seleccionar punto…</option>
                {puntos.map((p) => (
                  <option key={p.ubigeo} value={p.ubigeo}>
                    [{p.ubigeo}] {p.nombre} ({p.tipo})
                  </option>
                ))}
              </select>
            </div>

            {/* Parámetros de análisis */}
            {paramFields.map(({ name, label }) => (
              <div key={name}>
                <label className="text-gray-400 text-xs block mb-0.5">{label}</label>
                <input
                  name={name}
                  value={form[name]}
                  onChange={handleChange}
                  type="number"
                  step="any"
                  required
                  className="w-full bg-gray-800/60 border border-white/10 rounded-lg px-3 py-1.5 text-white text-sm focus:outline-none focus:ring-1 focus:ring-emerald-400/60"
                />
              </div>
            ))}

            {error && (
              <p className="text-red-400 text-xs bg-red-400/10 rounded-lg px-3 py-2">
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={loading || !form.ubigeo}
              className="w-full mt-1 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold text-sm rounded-xl py-2 transition-colors"
            >
              {loading ? "Calculando…" : "Generar cobertura"}
            </button>
          </form>
        </>
      )}
    </div>
  );
}

// ─── 3D Map View ─────────────────────────────────────────────────────────────/* eslint-disable @typescript-eslint/no-explicit-any */

function Map3DView({
  puntos,
  relaciones,
  cobertura,
}: {
  puntos: PuntoData[];
  relaciones: RelacionData[];
  cobertura: CoberturaViewModel | null;
}) {
  const containerRef = useRef<HTMLDivElement>(null);
  const map3dRef = useRef<any>(null);
  const coberturaElemsRef = useRef<any[]>([]);
  const apiLoaded = useApiIsLoaded();
  const [mapReady, setMapReady] = useState(false);

  // ── Efecto 1: construye mapa, marcadores y líneas (estable) ───────────────
  useEffect(() => {
    if (!apiLoaded || !containerRef.current) return;
    const container = containerRef.current;
    let cancelled = false;

    (async () => {
      const { Map3DElement, Marker3DElement, Polyline3DElement, AltitudeMode } =
        await (google.maps as any).importLibrary("maps3d");
      if (cancelled) return;

      const map3d = new Map3DElement({
        center: { lat: DEFAULT_CENTER.lat, lng: DEFAULT_CENTER.lng, altitude: 3500 },
        tilt: 67.5,
        range: 18000,
        heading: 20,
        mode: "HYBRID",
      });
      map3d.style.cssText = "width:100%;height:100%;display:block;";
      container.appendChild(map3d);
      map3dRef.current = map3d;

      const idx: Record<string, PuntoData> = {};
      puntos.forEach((p) => { idx[p.nombre] = p; });

      puntos.forEach((p) => {
        const marker = new Marker3DElement({
          position: { lat: p.latitud, lng: p.longitud, altitude: p.altura_antena },
          altitudeMode: AltitudeMode.RELATIVE_TO_GROUND,
          extruded: true,
          label: p.nombre,
        });
        map3d.appendChild(marker);
      });

      relaciones.forEach((r) => {
        const ini = idx[r.punto_inicial];
        const fin = idx[r.punto_final];
        if (!ini || !fin) return;
        const line = new Polyline3DElement({
          altitudeMode: AltitudeMode.RELATIVE_TO_GROUND,
          strokeColor: "#22D3EE",
          strokeWidth: 6,
          geodesic: true,
          drawsWhenOccluded: true,
        });
        line.coordinates = [
          { lat: ini.latitud, lng: ini.longitud, altitude: ini.altura_antena },
          { lat: fin.latitud, lng: fin.longitud, altitude: fin.altura_antena },
        ];
        map3d.appendChild(line);
      });

      setMapReady(true);
    })().catch(console.error);

    return () => {
      cancelled = true;
      if (map3dRef.current && container.contains(map3dRef.current)) {
        container.removeChild(map3dRef.current);
      }
      map3dRef.current = null;
      setMapReady(false);
    };
  }, [apiLoaded, puntos, relaciones]);

  // ── Efecto 2: agrega/elimina polígonos de cobertura sin tocar el mapa ─────
  useEffect(() => {
    coberturaElemsRef.current.forEach((el) => el.remove());
    coberturaElemsRef.current = [];

    if (!mapReady || !map3dRef.current || !cobertura) return;
    const map3d = map3dRef.current;

    (async () => {
      const { Polygon3DElement, AltitudeMode } =
        await (google.maps as any).importLibrary("maps3d");

      cobertura.malla.forEach((celda) => {
        const poly = new Polygon3DElement({
          altitudeMode: AltitudeMode.RELATIVE_TO_GROUND,
          fillColor: "rgba(52,211,153,0.45)",
          strokeColor: "#34D399",
          strokeWidth: 2,
          outerCoordinates: celda.coordenadas.map((c) => ({
            lat: c.latitud,
            lng: c.longitud,
            altitude: 10,
          })),
        });
        map3d.appendChild(poly);
        coberturaElemsRef.current.push(poly);
      });

      cobertura.poligonos.forEach((poli) => {
        const poly = new Polygon3DElement({
          altitudeMode: AltitudeMode.RELATIVE_TO_GROUND,
          fillColor: "rgba(0,0,0,0)",
          strokeColor: "#FBBF24",
          strokeWidth: 4,
          outerCoordinates: poli.coordenadas.map((c) => ({
            lat: c.latitud,
            lng: c.longitud,
            altitude: 15,
          })),
        });
        map3d.appendChild(poly);
        coberturaElemsRef.current.push(poly);
      });
    })().catch(console.error);
  }, [mapReady, cobertura]);

  return (
    <div className="relative w-full h-full bg-gray-950">
      {!apiLoaded && (
        <div className="absolute inset-0 flex items-center justify-center">
          <p className="text-white/60 text-sm animate-pulse">Cargando vista 3D…</p>
        </div>
      )}
      <div ref={containerRef} className="w-full h-full" />
    </div>
  );
}

/* eslint-enable @typescript-eslint/no-explicit-any */

// ─── Legend panel ─────────────────────────────────────────────────────────────

function Legend({
  puntos,
  relaciones,
  view3D,
  onToggle3D,
}: {
  puntos: PuntoData[];
  relaciones: RelacionData[];
  view3D: boolean;
  onToggle3D: () => void;
}) {
  const transportes = puntos.filter((p) => p.tipo === "transporte").length;
  const accesos = puntos.filter((p) => p.tipo === "acceso").length;

  return (
    <div className="absolute top-5 left-5 z-10 w-64 rounded-2xl overflow-hidden shadow-2xl">
      <div className="bg-gray-900/90 backdrop-blur-xl border border-white/10 px-5 py-4">
        <span className="text-white font-bold text-base tracking-tight">Red de Antenas</span>
        <p className="text-gray-400 text-xs mt-0.5">Line of Sight Analysis</p>
      </div>

      <div className="h-px bg-white/10" />

      <div className="bg-gray-900/85 backdrop-blur-xl border-x border-b border-white/10 rounded-b-2xl px-5 py-4 space-y-3">
        {/* Transporte */}
        <div className="flex items-center gap-3">
          <div className="w-4 h-4 rounded-full bg-amber-400 shadow-lg shadow-amber-400/60 ring-2 ring-amber-300/40 flex-shrink-0" />
          <div>
            <p className="text-white text-sm font-semibold leading-none">Transporte</p>
            <p className="text-gray-400 text-xs">{transportes} punto{transportes !== 1 ? "s" : ""}</p>
          </div>
        </div>

        {/* Acceso */}
        <div className="flex items-center gap-3">
          <div className="w-4 h-4 rounded-full bg-cyan-400 shadow-lg shadow-cyan-400/60 ring-2 ring-cyan-300/40 flex-shrink-0" />
          <div>
            <p className="text-white text-sm font-semibold leading-none">Acceso</p>
            <p className="text-gray-400 text-xs">{accesos} punto{accesos !== 1 ? "s" : ""}</p>
          </div>
        </div>

        {/* Relaciones */}
        <div className="flex items-center gap-3">
          <div className="w-4 h-1 rounded-full bg-cyan-400 shadow-lg shadow-cyan-400/60 flex-shrink-0" />
          <div>
            <p className="text-white text-sm font-semibold leading-none">Relaciones</p>
            <p className="text-gray-400 text-xs">{relaciones.length} enlace{relaciones.length !== 1 ? "s" : ""}</p>
          </div>
        </div>

        <div className="pt-2 border-t border-white/10 space-y-2">
          <button
            onClick={onToggle3D}
            className={`w-full py-2 px-3 rounded-xl text-sm font-semibold transition-all ${
              view3D
                ? "bg-cyan-500 text-gray-950 shadow-lg shadow-cyan-500/40"
                : "bg-white/10 text-white hover:bg-white/20"
            }`}
          >
            {view3D ? "← Vista 2D" : "Vista 3D ↗"}
          </button>
          <p className="text-gray-500 text-xs text-center">
            {view3D
              ? "Clic + arrastrar para rotar y volar"
              : "Botón central + arrastrar para rotar"}
          </p>
        </div>
      </div>
    </div>
  );
}

// ─── Map controls: tilt/rotate buttons + middle-mouse rotation ───────────────

function MapControls() {
  const map = useMap();

  useEffect(() => {
    if (!map) return;

    // ── Tilt / Rotate buttons via native map.controls (igual que el ejemplo de Google) ──
    const buttons: [string, string, number, google.maps.ControlPosition][] = [
      ["Rotate Left",  "rotate",  20, google.maps.ControlPosition.LEFT_CENTER],
      ["Rotate Right", "rotate", -20, google.maps.ControlPosition.RIGHT_CENTER],
      ["Tilt Down",    "tilt",    20, google.maps.ControlPosition.TOP_CENTER],
      ["Tilt Up",      "tilt",   -20, google.maps.ControlPosition.BOTTOM_CENTER],
    ];

    const addedDivs: { position: google.maps.ControlPosition; div: HTMLDivElement }[] = [];

    buttons.forEach(([text, mode, amount, position]) => {
      const div = document.createElement("div");
      const btn = document.createElement("button");
      btn.textContent = text;
      btn.style.cssText =
        "background:#fff;border:none;border-radius:4px;box-shadow:0 2px 6px rgba(0,0,0,.3);" +
        "cursor:pointer;font-size:14px;font-weight:600;margin:8px;padding:8px 12px;";
      btn.addEventListener("click", () => {
        if (mode === "rotate") map.setHeading((map.getHeading() ?? 0) + amount);
        if (mode === "tilt")   map.setTilt((map.getTilt() ?? 0) + amount);
      });
      div.appendChild(btn);
      map.controls[position].push(div);
      addedDivs.push({ position, div });
    });

    // ── Middle-mouse drag → rotate ─────────────────────────────────────────────
    const container = map.getDiv();
    let activePointerId: number | null = null;
    let lastX = 0;

    const onPointerDown = (e: PointerEvent) => {
      if (e.button !== 1) return;
      e.preventDefault();
      activePointerId = e.pointerId;
      lastX = e.clientX;
      container.setPointerCapture(e.pointerId);
    };
    const onPointerMove = (e: PointerEvent) => {
      if (e.pointerId !== activePointerId) return;
      map.setHeading((map.getHeading() ?? 0) + (e.clientX - lastX) * 0.5);
      lastX = e.clientX;
    };
    const onPointerUp = (e: PointerEvent) => {
      if (e.pointerId !== activePointerId) return;
      activePointerId = null;
      container.releasePointerCapture(e.pointerId);
    };

    container.addEventListener("pointerdown", onPointerDown);
    container.addEventListener("pointermove", onPointerMove);
    container.addEventListener("pointerup", onPointerUp);
    container.addEventListener("pointercancel", onPointerUp);

    return () => {
      // Eliminar botones de los slots nativos
      addedDivs.forEach(({ position, div }) => {
        const arr = map.controls[position];
        for (let i = 0; i < arr.getLength(); i++) {
          if (arr.getAt(i) === div) { arr.removeAt(i); break; }
        }
      });
      container.removeEventListener("pointerdown", onPointerDown);
      container.removeEventListener("pointermove", onPointerMove);
      container.removeEventListener("pointerup", onPointerUp);
      container.removeEventListener("pointercancel", onPointerUp);
    };
  }, [map]);

  return null;
}

// ─── Custom marker pin ─────────────────────────────────────────────────────────

function MarkerPin({ tipo }: { tipo: string }) {
  const color = tipo === "transporte" ? "#FBBF24" : "#22D3EE"; // amber / cyan
  const shadow = tipo === "transporte" ? "rgba(251,191,36,0.6)" : "rgba(34,211,238,0.6)";
  return (
    <div className="relative flex items-center justify-center">
      <div
        className="absolute w-7 h-7 rounded-full animate-ping opacity-40"
        style={{ background: color }}
      />
      <div
        className="relative w-4 h-4 rounded-full ring-2 ring-white"
        style={{ background: color, boxShadow: `0 0 8px 2px ${shadow}` }}
      />
    </div>
  );
}

// ─── Root component ────────────────────────────────────────────────────────────

const API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY ?? "";
// "90f87356969d889c" es el Map ID demo público de Google (vector map con tilt/rotation)
const MAP_ID = process.env.NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID || "90f87356969d889c";

export default function MapView() {
  const [puntos, setPuntos] = useState<PuntoData[]>([]);
  const [relaciones, setRelaciones] = useState<RelacionData[]>([]);
  const [view3D, setView3D] = useState(false);
  const [cobertura, setCobertura] = useState<CoberturaViewModel | null>(null);

  useEffect(() => {
    const load = async () => {
      const [pRes, rRes] = await Promise.all([
        fetch(`${BACKEND_URL}/api/puntos`),
        fetch(`${BACKEND_URL}/api/relaciones`),
      ]);
      if (pRes.ok) setPuntos(await pRes.json());
      if (rRes.ok) setRelaciones(await rRes.json());
    };
    load().catch(console.error);
  }, []);

  return (
    <div className="relative w-full h-full bg-gray-950">
      <APIProvider apiKey={API_KEY}>
        {view3D ? (
          <Map3DView puntos={puntos} relaciones={relaciones} cobertura={cobertura} />
        ) : (
          <Map
            mapId={MAP_ID}
            defaultZoom={13}
            defaultCenter={DEFAULT_CENTER}
            mapTypeId="satellite"
            defaultTilt={45}
            defaultHeading={20}
            gestureHandling="greedy"
            rotateControl={true}
            mapTypeControl={true}
            mapTypeControlOptions={{
              mapTypeIds: ["satellite", "hybrid", "terrain", "roadmap"],
            }}
            style={{ width: "100%", height: "100%" }}
          >
            <MapOverlays puntos={puntos} relaciones={relaciones} />
            <CoberturaOverlays data={cobertura} />
            {puntos.map((p) => (
              <AdvancedMarker
                key={p.nombre}
                position={{ lat: p.latitud, lng: p.longitud }}
                title={`${p.nombre} (${p.tipo})`}
              >
                <MarkerPin tipo={p.tipo} />
              </AdvancedMarker>
            ))}
            <MapControls />
          </Map>
        )}
      </APIProvider>

      <Legend
        puntos={puntos}
        relaciones={relaciones}
        view3D={view3D}
        onToggle3D={() => setView3D((v) => !v)}
      />
      <CoberturaPanel puntos={puntos} onResult={setCobertura} />
    </div>
  );
}
