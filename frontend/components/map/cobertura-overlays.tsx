"use client";

import { useEffect, useRef } from "react";
import { useMap } from "@vis.gl/react-google-maps";
import type { CoberturaViewModel } from "./types";

export function CoberturaOverlays({ data }: { data: CoberturaViewModel | null }) {
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
          fillColor: "#FBBF24",
          fillOpacity: 0.15,
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
