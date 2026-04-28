"use client";

import { useEffect, useState } from "react";
import {
  APIProvider,
  Map,
  AdvancedMarker,
} from "@vis.gl/react-google-maps";

import type { PuntoData, RelacionData, CoberturaViewModel } from "./map/types";
import { BACKEND_URL, DEFAULT_CENTER } from "./map/config";
import { MapOverlays } from "./map/map-overlays";
import { CoberturaOverlays } from "./map/cobertura-overlays";
import { CoberturaPanel } from "./map/cobertura-panel";
import { Map3DView } from "./map/map-3d-view";
import { Legend } from "./map/legend";
import { MapControls } from "./map/map-controls";
import { MarkerPin } from "./map/marker-pin";


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
