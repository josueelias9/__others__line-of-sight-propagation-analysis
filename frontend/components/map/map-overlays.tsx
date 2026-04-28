"use client";

import { useEffect, useRef } from "react";
import { useMap } from "@vis.gl/react-google-maps";
import type { PuntoData, RelacionData } from "./types";

export function MapOverlays({
  puntos,
  relaciones,
}: {
  puntos: PuntoData[];
  relaciones: RelacionData[];
}) {
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
