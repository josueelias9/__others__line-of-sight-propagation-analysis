"use client";

import { useEffect, useRef } from "react";
import { useMap } from "@vis.gl/react-google-maps";
import type { PuntoData, RelacionData, RelacionArbolOut } from "./types";

export function MapOverlays({
  puntos,
  relaciones,
  arbolRelaciones = [],
}: {
  puntos: PuntoData[];
  relaciones: RelacionData[];
  arbolRelaciones?: RelacionArbolOut[];
}) {
  const map = useMap();
  const linesRef = useRef<google.maps.Polyline[]>([]);

  useEffect(() => {
    if (!map) return;

    linesRef.current.forEach((l) => l.setMap(null));
    linesRef.current = [];

    const idx: Record<string, PuntoData> = {};
    puntos.forEach((p) => { idx[p.nombre] = p; });

    const drawLine = (
      puntoInicial: string,
      puntoFinal: string,
      color: string,
      weight: number,
    ) => {
      const ini = idx[puntoInicial];
      const fin = idx[puntoFinal];
      if (!ini || !fin) return;
      const line = new google.maps.Polyline({
        path: [
          { lat: ini.latitud, lng: ini.longitud },
          { lat: fin.latitud, lng: fin.longitud },
        ],
        geodesic: true,
        strokeColor: color,
        strokeOpacity: 0.9,
        strokeWeight: weight,
        map,
      });
      linesRef.current.push(line);
    };

    relaciones.forEach((r) => drawLine(r.punto_inicial, r.punto_final, "#22D3EE", 3));
    arbolRelaciones.forEach((r) => drawLine(r.punto_inicial, r.punto_final, "#FACC15", 5));

    return () => {
      linesRef.current.forEach((l) => l.setMap(null));
      linesRef.current = [];
    };
  }, [map, puntos, relaciones, arbolRelaciones]);

  return null;
}
