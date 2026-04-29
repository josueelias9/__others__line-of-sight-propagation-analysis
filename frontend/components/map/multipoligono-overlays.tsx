"use client";

import { useEffect, useRef } from "react";
import { useMap } from "@vis.gl/react-google-maps";
import type { MultipoligonoData } from "./types";

const COLORS = [
  "#60A5FA", // blue-400
  "#F472B6", // pink-400
  "#A78BFA", // violet-400
  "#FB923C", // orange-400
  "#34D399", // emerald-400
  "#FACC15", // yellow-400
  "#F87171", // red-400
  "#2DD4BF", // teal-400
];

export function MultipoligonoOverlays({ items }: { items: MultipoligonoData[] }) {
  const map = useMap();
  const polysRef = useRef<google.maps.Polygon[]>([]);

  useEffect(() => {
    polysRef.current.forEach((p) => p.setMap(null));
    polysRef.current = [];

    if (!map || items.length === 0) return;

    items.forEach((item) => {
      const color = COLORS[item.id % COLORS.length];
      const { geometry } = item.geojson;
      if (!geometry) return;

      const polygons =
        geometry.type === "Polygon"
          ? [geometry.coordinates]
          : geometry.coordinates;

      polygons.forEach((rings) => {
        const paths = rings.map((ring) =>
          ring.map(([lng, lat]) => ({ lat, lng }))
        );
        polysRef.current.push(
          new google.maps.Polygon({
            paths,
            strokeColor: color,
            strokeOpacity: 0.9,
            strokeWeight: 2,
            fillColor: color,
            fillOpacity: 0.12,
            map,
          })
        );
      });
    });

    return () => {
      polysRef.current.forEach((p) => p.setMap(null));
    };
  }, [map, items]);

  return null;
}
