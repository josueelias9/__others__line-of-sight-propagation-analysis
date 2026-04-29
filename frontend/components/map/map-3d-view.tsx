"use client";

/* eslint-disable @typescript-eslint/no-explicit-any */

import { useEffect, useRef, useState } from "react";
import { useApiIsLoaded } from "@vis.gl/react-google-maps";
import type { PuntoData, RelacionData, CoberturaViewModel, RelacionArbolOut } from "./types";
import { DEFAULT_CENTER } from "./config";

export function Map3DView({
  puntos,
  relaciones,
  cobertura,
  arbolRelaciones = [],
}: {
  puntos: PuntoData[];
  relaciones: RelacionData[];
  cobertura: CoberturaViewModel | null;
  arbolRelaciones?: RelacionArbolOut[];
}) {
  const containerRef = useRef<HTMLDivElement>(null);
  const map3dRef = useRef<any>(null);
  const libRef = useRef<any>(null);
  const coberturaElemsRef = useRef<any[]>([]);
  const arbolLinesRef = useRef<any[]>([]);
  const apiLoaded = useApiIsLoaded();
  const [mapReady, setMapReady] = useState(false);

  // ── Efecto 1: construye mapa, marcadores y líneas (estable) ───────────────
  useEffect(() => {
    if (!apiLoaded || !containerRef.current) return;
    const container = containerRef.current;
    let cancelled = false;

    (async () => {
      const lib = await (google.maps as any).importLibrary("maps3d");
      if (cancelled) return;
      libRef.current = lib;
      const { Map3DElement, Marker3DElement, Polyline3DElement, AltitudeMode } = lib;

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

        const svgImg = document.createElement("img");
        svgImg.src = p.tipo === "transporte" ? "/transporte.svg" : "/acceso.svg";
        svgImg.width = 32;
        svgImg.height = 32;
        const tmpl = document.createElement("template");
        tmpl.content.append(svgImg);
        marker.append(tmpl);

        map3d.appendChild(marker);
      });

      relaciones.forEach((r) => {
        const ini = idx[r.punto_inicial];
        const fin = idx[r.punto_final];
        if (!ini || !fin) return;
        const line = new Polyline3DElement({
          altitudeMode: "ABSOLUTE",
          strokeColor: "#22D3EE",
          strokeWidth: 6,
          geodesic: true,
          drawsOccludedSegments: true,
        });
        line.coordinates = [
          { lat: ini.latitud, lng: ini.longitud, altitude: ini.metros_sobre_nivel_mar + ini.altura_antena },
          { lat: fin.latitud, lng: fin.longitud, altitude: fin.metros_sobre_nivel_mar + fin.altura_antena },
        ];
        map3d.append(line);
      });

      setMapReady(true);
    })().catch(console.error);

    return () => {
      cancelled = true;
      if (map3dRef.current && container.contains(map3dRef.current)) {
        container.removeChild(map3dRef.current);
      }
      map3dRef.current = null;
      libRef.current = null;
      setMapReady(false);
    };
  }, [apiLoaded, puntos, relaciones]);

  // ── Efecto 2: agrega/elimina líneas del árbol de conexión ──────────────────
  useEffect(() => {
    arbolLinesRef.current.forEach((el) => el.remove());
    arbolLinesRef.current = [];

    if (!mapReady || !map3dRef.current || !libRef.current || arbolRelaciones.length === 0) return;
    const map3d = map3dRef.current;
    const { Polyline3DElement } = libRef.current;

    const idx: Record<string, PuntoData> = {};
    puntos.forEach((p) => { idx[p.nombre] = p; });

    arbolRelaciones.forEach((r) => {
      const ini = idx[r.punto_inicial];
      const fin = idx[r.punto_final];
      if (!ini || !fin) return;
      const line = new Polyline3DElement({
        altitudeMode: "ABSOLUTE",
        strokeColor: "#FACC15",
        strokeWidth: 8,
        geodesic: true,
        drawsOccludedSegments: true,
      });
      line.coordinates = [
        { lat: ini.latitud, lng: ini.longitud, altitude: ini.metros_sobre_nivel_mar + ini.altura_antena },
        { lat: fin.latitud, lng: fin.longitud, altitude: fin.metros_sobre_nivel_mar + fin.altura_antena },
      ];
      map3d.append(line);
      arbolLinesRef.current.push(line);
    });
  }, [mapReady, arbolRelaciones, puntos]);

  // ── Efecto 3: agrega/elimina polígonos de cobertura sin tocar el mapa ─────
  useEffect(() => {
    coberturaElemsRef.current.forEach((el) => el.remove());
    coberturaElemsRef.current = [];

    if (!mapReady || !map3dRef.current || !cobertura) return;
    const map3d = map3dRef.current;

    (async () => {
      const { Polygon3DElement } =
        await (google.maps as any).importLibrary("maps3d");

      cobertura.malla.forEach((celda) => {
        const poly = new Polygon3DElement({
          altitudeMode: "CLAMP_TO_GROUND",
          fillColor: "rgba(52,211,153,0.45)",
          strokeColor: "#34D399",
          strokeWidth: 2,
          outerCoordinates: celda.coordenadas.map((c) => ({
            lat: c.latitud,
            lng: c.longitud,
          })),
        });
        map3d.append(poly);
        coberturaElemsRef.current.push(poly);
      });

      const { geometry } = cobertura.geojson;
      if (geometry) {
        const polygons: [number, number][][][] =
          geometry.type === "Polygon"
            ? [geometry.coordinates]
            : geometry.coordinates;

        polygons.forEach(([outerRing, ...innerRings]) => {
          const poly = new Polygon3DElement({
            altitudeMode: "CLAMP_TO_GROUND",
            fillColor: "rgba(251,191,36,0.2)",
            strokeColor: "#FBBF24",
            strokeWidth: 4,
          });
          poly.outerCoordinates = outerRing.map(([lng, lat]) => ({ lat, lng }));
          if (innerRings.length > 0) {
            poly.innerCoordinates = innerRings.map((ring) =>
              ring.map(([lng, lat]) => ({ lat, lng }))
            );
          }
          map3d.append(poly);
          coberturaElemsRef.current.push(poly);
        });
      }
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
