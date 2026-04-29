"use client";

import { useEffect, useState } from "react";
import {
  APIProvider,
  Map,
  AdvancedMarker,
} from "@vis.gl/react-google-maps";

import type { PuntoData, RelacionData, CoberturaViewModel, ArbolResult } from "./map/types";
import { BACKEND_URL, DEFAULT_CENTER } from "./map/config";
import { MapOverlays } from "./map/map-overlays";
import { CoberturaOverlays } from "./map/cobertura-overlays";
import { CoberturaPanel } from "./map/cobertura-panel";
import { ArbolPanel } from "./map/arbol-panel";
import { Map3DView } from "./map/map-3d-view";
import { Legend } from "./map/legend";
import { MapControls } from "./map/map-controls";
import { MarkerPin } from "./map/marker-pin";
import { AddPuntoPanel } from "./map/add-punto-panel";


const API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY ?? "";
// "90f87356969d889c" es el Map ID demo público de Google (vector map con tilt/rotation)
const MAP_ID = process.env.NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID || "90f87356969d889c";

export default function MapView() {
  const [puntos, setPuntos] = useState<PuntoData[]>([]);
  const [relaciones, setRelaciones] = useState<RelacionData[]>([]);
  const [view3D, setView3D] = useState(false);
  const [cobertura, setCobertura] = useState<CoberturaViewModel | null>(null);
  const [arbolResult, setArbolResult] = useState<ArbolResult | null>(null);
  const [pickingMode, setPickingMode] = useState(false);
  const [pickedCoords, setPickedCoords] = useState<{ lat: number; lng: number } | null>(null);
  const [tipoFiltro, setTipoFiltro] = useState("");

  useEffect(() => {
    const load = async () => {
      const pUrl = tipoFiltro
        ? `${BACKEND_URL}/api/puntos?tipo=${encodeURIComponent(tipoFiltro)}`
        : `${BACKEND_URL}/api/puntos`;
      const [pRes, rRes] = await Promise.all([
        fetch(pUrl),
        fetch(`${BACKEND_URL}/api/relaciones`),
      ]);
      if (pRes.ok) setPuntos(await pRes.json());
      if (rRes.ok) setRelaciones(await rRes.json());
    };
    load().catch(console.error);
  }, [tipoFiltro]);

  return (
    <div className="relative w-full h-full bg-gray-950">
      <APIProvider apiKey={API_KEY}>
        {view3D ? (
          <Map3DView puntos={puntos} relaciones={relaciones} cobertura={cobertura} arbolRelaciones={arbolResult?.relaciones_exitosas ?? []} />
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
            style={{ width: "100%", height: "100%", cursor: pickingMode ? "crosshair" : "" }}
            onClick={(e) => {
              if (pickingMode && e.detail.latLng) {
                setPickedCoords({ lat: e.detail.latLng.lat, lng: e.detail.latLng.lng });
                setPickingMode(false);
              }
            }}
          >
            <MapOverlays
              puntos={puntos}
              relaciones={relaciones}
              arbolRelaciones={arbolResult?.relaciones_exitosas ?? []}
            
            />
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

      {pickingMode && (
        <div className="absolute inset-x-0 top-5 z-10 flex justify-center pointer-events-none">
          <div className="bg-cyan-500 text-gray-950 font-bold text-sm px-5 py-2.5 rounded-2xl shadow-xl shadow-cyan-500/40">
            Haz clic en el mapa para ubicar el punto
          </div>
        </div>
      )}

      <Legend
        puntos={puntos}
        relaciones={relaciones}
        view3D={view3D}
        onToggle3D={() => setView3D((v) => !v)}
        tipoFiltro={tipoFiltro}
        onFiltroChange={setTipoFiltro}
      />
      <div className="absolute top-5 right-5 z-10 flex flex-col gap-2 w-72">
        <CoberturaPanel puntos={puntos} onResult={setCobertura} />
        <ArbolPanel puntos={puntos} onResult={setArbolResult} />
      </div>
      <AddPuntoPanel
        onAdded={(nuevo) => setPuntos((prev) => [...prev, nuevo])}
        onRequestPick={() => setPickingMode(true)}
        pickedCoords={pickedCoords}
        onPickConsumed={() => setPickedCoords(null)}
      />
    </div>
  );
}
