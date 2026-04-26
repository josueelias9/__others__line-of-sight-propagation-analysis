"use client";

import { useEffect, useRef } from "react";
import {
  APIProvider,
  Map,
  AdvancedMarker,
  useMap,
} from "@vis.gl/react-google-maps";

// ─── Demo geometry – Lima, Perú ───────────────────────────────────────────────

const CENTER = { lat: -12.0453, lng: -77.0311 };

// 1. Punto — Plaza Mayor de Lima
const POINT: google.maps.LatLngLiteral = { lat: -12.0453, lng: -77.0311 };

// 2. Línea — recorrido por el centro histórico
const LINE_PATH: google.maps.LatLngLiteral[] = [
  { lat: -12.0453, lng: -77.0311 },
  { lat: -12.043, lng: -77.034 },
  { lat: -12.041, lng: -77.036 },
  { lat: -12.039, lng: -77.039 },
];

// 3. Polígono — área alrededor de la plaza
const POLYGON_PATH: google.maps.LatLngLiteral[] = [
  { lat: -12.0435, lng: -77.0290 },
  { lat: -12.0435, lng: -77.0335 },
  { lat: -12.0475, lng: -77.0335 },
  { lat: -12.0475, lng: -77.0290 },
];

// ─── Map overlays rendered imperatively ───────────────────────────────────────

function MapOverlays() {
  const map = useMap();
  const polylineRef = useRef<google.maps.Polyline | null>(null);
  const polygonRef = useRef<google.maps.Polygon | null>(null);

  useEffect(() => {
    if (!map) return;

    polylineRef.current = new google.maps.Polyline({
      path: LINE_PATH,
      geodesic: true,
      strokeColor: "#22D3EE",
      strokeOpacity: 1,
      strokeWeight: 4,
      map,
    });

    polygonRef.current = new google.maps.Polygon({
      paths: POLYGON_PATH,
      strokeColor: "#34D399",
      strokeOpacity: 0.9,
      strokeWeight: 2,
      fillColor: "#34D399",
      fillOpacity: 0.2,
      map,
    });

    return () => {
      polylineRef.current?.setMap(null);
      polygonRef.current?.setMap(null);
    };
  }, [map]);

  return null;
}

// ─── Legend panel ─────────────────────────────────────────────────────────────

function Legend() {
  return (
    <div className="absolute top-5 left-5 z-10 w-64 rounded-2xl overflow-hidden shadow-2xl">
      {/* Glass header */}
      <div className="bg-gray-900/90 backdrop-blur-xl border border-white/10 px-5 py-4">
        <div className="flex items-center gap-2 mb-0.5">
          <span className="text-white font-bold text-base tracking-tight">
            3D Map Viewer
          </span>
        </div>
        <p className="text-gray-400 text-xs">Lima, Perú · Vista satelital</p>
      </div>

      {/* Divider */}
      <div className="h-px bg-white/10" />

      {/* Items */}
      <div className="bg-gray-900/85 backdrop-blur-xl border-x border-b border-white/10 rounded-b-2xl px-5 py-4 space-y-4">
        {/* Punto */}
        <div className="flex items-center gap-3">
          <div className="flex-shrink-0 relative">
            <div className="w-4 h-4 rounded-full bg-amber-400 shadow-lg shadow-amber-400/60 ring-2 ring-amber-300/40" />
          </div>
          <div>
            <p className="text-white text-sm font-semibold leading-none mb-0.5">
              Punto
            </p>
            <p className="text-gray-400 text-xs">Plaza Mayor de Lima</p>
          </div>
          <span className="ml-auto text-xs font-mono text-amber-400/70 bg-amber-400/10 px-1.5 py-0.5 rounded">
            marker
          </span>
        </div>

        {/* Línea */}
        <div className="flex items-center gap-3">
          <div className="flex-shrink-0 flex items-center justify-center w-4 h-4">
            <div className="w-4 h-1 rounded-full bg-cyan-400 shadow-lg shadow-cyan-400/60" />
          </div>
          <div>
            <p className="text-white text-sm font-semibold leading-none mb-0.5">
              Línea
            </p>
            <p className="text-gray-400 text-xs">Ruta — centro histórico</p>
          </div>
          <span className="ml-auto text-xs font-mono text-cyan-400/70 bg-cyan-400/10 px-1.5 py-0.5 rounded">
            polyline
          </span>
        </div>

        {/* Polígono */}
        <div className="flex items-center gap-3">
          <div className="flex-shrink-0 w-4 h-4 rounded-sm border-2 border-emerald-400 bg-emerald-400/20 shadow-lg shadow-emerald-400/30" />
          <div>
            <p className="text-white text-sm font-semibold leading-none mb-0.5">
              Polígono
            </p>
            <p className="text-gray-400 text-xs">Área de cobertura</p>
          </div>
          <span className="ml-auto text-xs font-mono text-emerald-400/70 bg-emerald-400/10 px-1.5 py-0.5 rounded">
            polygon
          </span>
        </div>

        {/* Footer */}
        <div className="pt-2 border-t border-white/10">
          <p className="text-gray-600 text-xs text-center">
            Google Maps JavaScript API
          </p>
        </div>
      </div>
    </div>
  );
}

// ─── Custom marker pin ─────────────────────────────────────────────────────────

function MarkerPin() {
  return (
    <div className="relative flex items-center justify-center">
      {/* Pulse ring */}
      <div className="absolute w-8 h-8 rounded-full bg-amber-400/30 animate-ping" />
      {/* Outer ring */}
      <div className="absolute w-6 h-6 rounded-full bg-amber-400/20 ring-1 ring-amber-400/40" />
      {/* Core dot */}
      <div className="relative w-4 h-4 rounded-full bg-amber-400 shadow-lg shadow-amber-500/70 ring-2 ring-white" />
    </div>
  );
}

// ─── Root component ────────────────────────────────────────────────────────────

const API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY ?? "";
const MAP_ID = process.env.NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID ?? "";

export default function MapView() {
  return (
    <div className="relative w-full h-full bg-gray-950">
      <APIProvider apiKey={API_KEY}>
        <Map
          mapId={MAP_ID || undefined}
          defaultZoom={16}
          defaultCenter={CENTER}
          mapTypeId="satellite"
          tilt={45}
          heading={20}
          disableDefaultUI={false}
          gestureHandling="greedy"
          style={{ width: "100%", height: "100%" }}
        >
          <MapOverlays />

          <AdvancedMarker position={POINT} title="Plaza Mayor de Lima">
            <MarkerPin />
          </AdvancedMarker>
        </Map>
      </APIProvider>

      <Legend />
    </div>
  );
}
