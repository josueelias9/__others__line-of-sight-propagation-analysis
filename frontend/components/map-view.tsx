'use client'

import { useEffect, useMemo, useState, useActionState } from 'react'
import { APIProvider, Map, AdvancedMarker } from '@vis.gl/react-google-maps'
import { signOutAction, poblarDatosUsuario, type SeedState } from '@/app/lib/actions'
import { fetchPuntos } from '@/app/lib/data'

import type {
    PuntoData,
    CoberturaViewModel,
    ArbolResult,
    MultipoligonoData,
    RedData
} from '../app/lib/types'
import { DEFAULT_CENTER } from '../app/lib/config'
import { MapOverlays } from './map/overlays/map-overlays'
import { RedOverlays } from './map/overlays/red-overlays'
import { CoberturaOverlays } from './map/overlays/cobertura-overlays'
import { CoberturaPanel } from './map/paneles/cobertura-panel'
import { ArbolPanel } from './map/paneles/arbol-panel'
import { Map3DView } from './map/map-3d-view'
import { Legend } from './map/legend'
import { MapControls } from './map/map-controls'
import { MarkerPin } from './map/marker-pin'
import { AddPuntoPanel } from './map/paneles/add-punto-panel'
import { SavedItemsPanel } from './map/paneles/generic-panel'
import { MultipoligonoOverlays } from './map/overlays/multipoligono-overlays'

const API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY ?? ''
// "90f87356969d889c" es el Map ID demo público de Google (vector map con tilt/rotation)
const MAP_ID = process.env.NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID || '90f87356969d889c'

interface MapViewProps {
    initialPuntos: PuntoData[]
    initialRedes: RedData[]
    initialCoberturas: MultipoligonoData[]
}

export default function MapView({ initialPuntos, initialRedes, initialCoberturas }: MapViewProps) {
    const [puntos, setPuntos] = useState<PuntoData[]>(initialPuntos)
    const [view3D, setView3D] = useState(false)
    const [cobertura, setCobertura] = useState<CoberturaViewModel | null>(null)
    const [showMalla, setShowMalla] = useState(false)
    const [arbolResult, setArbolResult] = useState<ArbolResult | null>(null)
    const [multipoligonos, setMultipoligonos] = useState<MultipoligonoData[]>(initialCoberturas)
    const [pickingMode, setPickingMode] = useState(false)
    const [pickedCoords, setPickedCoords] = useState<{ lat: number; lng: number } | null>(null)
    const [tipoFiltro, setTipoFiltro] = useState('')
    const [redes, setRedes] = useState<RedData[]>(initialRedes)

    const seedInitialState: SeedState = { puntosCreados: null, error: null }
    const [seedState, seedAction, seedPending] = useActionState(
        poblarDatosUsuario,
        seedInitialState
    )

    const highlightedUbigeos = useMemo(() => {
        const s = new Set<number>()
        for (const red of redes) {
            for (const rel of red.relaciones) {
                s.add(rel.punto_inicial_ubigeo)
                s.add(rel.punto_final_ubigeo)
            }
        }
        return s
    }, [redes])

    useEffect(() => {
        if (!tipoFiltro) return
        fetchPuntos(tipoFiltro).then(setPuntos).catch(console.error)
    }, [tipoFiltro])

    // Reload puntos after a successful seed
    useEffect(() => {
        if (seedState.puntosCreados !== null && seedState.puntosCreados > 0) {
            fetchPuntos().then(setPuntos).catch(console.error)
        }
    }, [seedState])

    return (
        <div className='relative w-full h-full bg-gray-950'>
            {/* Top-center bar: logout + seed */}
            {/* TODO this two form can be asigned to component */}
            <div className='absolute top-3 left-1/2 -translate-x-1/2 z-20 flex items-center gap-2'>
                <form action={seedAction}>
                    <button
                        type='submit'
                        disabled={seedPending}
                        className='text-xs text-gray-400 hover:text-white bg-gray-900/70 hover:bg-gray-800 border border-white/10 rounded-lg px-3 py-1 transition-colors disabled:opacity-50'
                        title='Carga puntos de ejemplo para comenzar a explorar la app'
                    >
                        {seedPending
                            ? 'Cargando...'
                            : seedState.puntosCreados === 0
                              ? '✓ Datos ya cargados'
                              : seedState.puntosCreados !== null
                                ? `✓ ${seedState.puntosCreados} puntos cargados`
                                : '¿Cómo usar la app? Cargar datos de ejemplo'}
                    </button>
                </form>
                {seedState.error && <span className='text-xs text-red-400'>{seedState.error}</span>}
                <form action={signOutAction}>
                    <button
                        type='submit'
                        className='text-xs text-gray-500 hover:text-white bg-gray-900/70 hover:bg-gray-800 border border-white/10 rounded-lg px-3 py-1 transition-colors'
                    >
                        Cerrar sesión
                    </button>
                </form>
            </div>
            <APIProvider apiKey={API_KEY}>
                <Map3DView
                    puntos={puntos}
                    redes={redes}
                    cobertura={cobertura}
                    arbolRedGeojson={arbolResult?.red_geojson ?? null}
                    showMalla={showMalla}
                    multipoligonos={multipoligonos}
                />
                {/* {view3D ? (
                    <Map3DView
                        puntos={puntos}
                        redes={redes}
                        cobertura={cobertura}
                        arbolRedGeojson={arbolResult?.red_geojson ?? null}
                        showMalla={showMalla}
                        multipoligonos={multipoligonos}
                    />
                ) : (
                    <Map
                        mapId={MAP_ID}
                        defaultZoom={13}
                        defaultCenter={DEFAULT_CENTER}
                        mapTypeId='satellite'
                        defaultTilt={45}
                        defaultHeading={20}
                        gestureHandling='greedy'
                        rotateControl={true}
                        mapTypeControl={true}
                        mapTypeControlOptions={{
                            mapTypeIds: ['satellite', 'hybrid', 'terrain', 'roadmap']
                        }}
                        style={{
                            width: '100%',
                            height: '100%',
                            cursor: pickingMode ? 'crosshair' : ''
                        }}
                        onClick={e => {
                            if (pickingMode && e.detail.latLng) {
                                setPickedCoords({
                                    lat: e.detail.latLng.lat,
                                    lng: e.detail.latLng.lng
                                })
                                setPickingMode(false)
                            }
                        }}
                    >
                        <MapOverlays
                            puntos={puntos}
                            arbolRedGeojson={arbolResult?.red_geojson ?? null}
                        />
                        <RedOverlays redes={redes} />
                        <CoberturaOverlays data={cobertura} showMalla={showMalla} />
                        <MultipoligonoOverlays items={multipoligonos} />
                        {puntos.map(p => (
                            <AdvancedMarker
                                key={p.nombre}
                                position={{ lat: p.latitud, lng: p.longitud }}
                                title={`${p.nombre} (${p.tipo})`}
                            >
                                <MarkerPin
                                    tipo={p.tipo}
                                    highlighted={highlightedUbigeos.has(p.ubigeo)}
                                />
                            </AdvancedMarker>
                        ))}
                        <MapControls />
                    </Map>
                )} */}
            </APIProvider>

            {pickingMode && (
                <div className='absolute inset-x-0 top-5 z-10 flex justify-center pointer-events-none'>
                    <div className='bg-cyan-500 text-gray-950 font-bold text-sm px-5 py-2.5 rounded-2xl shadow-xl shadow-cyan-500/40'>
                        Haz clic en el mapa para ubicar el punto
                    </div>
                </div>
            )}

            <Legend
                puntos={puntos}
                redesRelacionCount={redes.reduce((acc, r) => acc + r.relaciones.length, 0)}
                view3D={view3D}
                onToggle3D={() => setView3D(v => !v)}
                tipoFiltro={tipoFiltro}
                onFiltroChange={setTipoFiltro}
            />
            <div className='absolute top-5 right-5 z-10 flex flex-col gap-2 w-72'>
                <CoberturaPanel puntos={puntos} onResult={setCobertura} />
                {cobertura && (
                    <button
                        onClick={() => setShowMalla(v => !v)}
                        className={`w-full rounded-xl px-4 py-2 text-sm font-semibold transition-colors border ${
                            showMalla
                                ? 'bg-emerald-500/20 border-emerald-400/40 text-emerald-300 hover:bg-emerald-500/30'
                                : 'bg-gray-800/60 border-white/10 text-gray-400 hover:bg-gray-700/60'
                        }`}
                    >
                        {showMalla ? '✓ Malla visible' : '○ Malla oculta'}
                    </button>
                )}
                <ArbolPanel puntos={puntos} onResult={setArbolResult} />
                <SavedItemsPanel
                    kind='redes'
                    initialItems={redes}
                    onVisibleItemsChange={setRedes}
                />
                <SavedItemsPanel
                    kind='coberturas'
                    initialItems={multipoligonos}
                    onVisibleItemsChange={setMultipoligonos}
                />
            </div>
            <AddPuntoPanel
                onAdded={nuevo => setPuntos(prev => [...prev, nuevo])}
                onRequestPick={() => setPickingMode(true)}
                pickedCoords={pickedCoords}
                onPickConsumed={() => setPickedCoords(null)}
            />
        </div>
    )
}
