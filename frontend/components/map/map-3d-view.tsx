"use client";

/* eslint-disable @typescript-eslint/no-explicit-any */

import { useEffect, useRef, useState } from "react";
import { useApiIsLoaded } from "@vis.gl/react-google-maps";
import type { PuntoData, RelacionData, CoberturaViewModel } from "./types";
import { DEFAULT_CENTER } from "./config";

export function Map3DView({
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
