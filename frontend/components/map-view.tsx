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

// ─── 3D Map View ─────────────────────────────────────────────────────────────
/* eslint-disable @typescript-eslint/no-explicit-any */

function Map3DView({ puntos, relaciones }: { puntos: PuntoData[]; relaciones: RelacionData[] }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const apiLoaded = useApiIsLoaded();

  useEffect(() => {
    if (!apiLoaded || !containerRef.current) return;

    const container = containerRef.current;
    let map3d: any;
    let cancelled = false;

    (async () => {
      // Igual al tutorial oficial: importLibrary('maps3d') → new Map3DElement
      const { Map3DElement, Marker3DElement, Polyline3DElement, AltitudeMode } =
        await (google.maps as any).importLibrary("maps3d");

      if (cancelled) return;

      // mode: 'HYBRID' activa los tiles fotorrealistas 3D con relieve real
      map3d = new Map3DElement({
        center: { lat: DEFAULT_CENTER.lat, lng: DEFAULT_CENTER.lng, altitude: 3500 },
        tilt: 67.5,
        range: 18000,
        heading: 20,
        mode: "HYBRID",
      });
      map3d.style.cssText = "width:100%;height:100%;display:block;";
      container.appendChild(map3d);

      // Índice de puntos para polilíneas
      const idx: Record<string, PuntoData> = {};
      puntos.forEach((p) => { idx[p.nombre] = p; });

      // Marcadores extruídos a la altitud real de cada antena
      puntos.forEach((p) => {
        const marker = new Marker3DElement({
          position: {
            lat: p.latitud,
            lng: p.longitud,
            altitude: p.metros_sobre_nivel_mar + p.altura_antena,
          },
          altitudeMode: AltitudeMode.ABSOLUTE,
          extruded: true,
          label: p.nombre,
        });
        map3d.appendChild(marker);
      });

      // Polilíneas que unen antenas flotando a su altitud real
      relaciones.forEach((r) => {
        const ini = idx[r.punto_inicial];
        const fin = idx[r.punto_final];
        if (!ini || !fin) return;
        const line = new Polyline3DElement({
          altitudeMode: AltitudeMode.ABSOLUTE,
          strokeColor: "#22D3EE",
          strokeWidth: 6,
          geodesic: true,
          drawsWhenOccluded: true,
        });
        line.coordinates = [
          { lat: ini.latitud, lng: ini.longitud, altitude: ini.metros_sobre_nivel_mar + ini.altura_antena },
          { lat: fin.latitud, lng: fin.longitud, altitude: fin.metros_sobre_nivel_mar + fin.altura_antena },
        ];
        map3d.appendChild(line);
      });
    })().catch(console.error);

    return () => {
      cancelled = true;
      if (map3d && container.contains(map3d)) container.removeChild(map3d);
    };
  }, [apiLoaded, puntos, relaciones]);

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
          <Map3DView puntos={puntos} relaciones={relaciones} />
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
    </div>
  );
}
