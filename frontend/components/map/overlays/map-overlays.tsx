'use client'

import { useEffect, useRef } from 'react'
import { useMap } from '@vis.gl/react-google-maps'
import type { PuntoData, RelacionRedData, RelacionArbolOut } from '@/app/lib/types'

export function MapOverlays({
    puntos,
    redesRelaciones = [],
    arbolRelaciones = []
}: {
    puntos: PuntoData[]
    redesRelaciones?: RelacionRedData[]
    arbolRelaciones?: RelacionArbolOut[]
}) {
    const map = useMap()
    const linesRef = useRef<google.maps.Polyline[]>([])

    useEffect(() => {
        if (!map) return

        linesRef.current.forEach(l => l.setMap(null))
        linesRef.current = []

        const byUbigeo: Record<number, PuntoData> = {}
        puntos.forEach(p => {
            byUbigeo[p.ubigeo] = p
        })

        const byNombre: Record<string, PuntoData> = {}
        puntos.forEach(p => {
            byNombre[p.nombre] = p
        })

        const drawLine = (
            ini: PuntoData | undefined,
            fin: PuntoData | undefined,
            color: string,
            weight: number
        ) => {
            if (!ini || !fin) return
            const line = new google.maps.Polyline({
                path: [
                    { lat: ini.latitud, lng: ini.longitud },
                    { lat: fin.latitud, lng: fin.longitud }
                ],
                geodesic: true,
                strokeColor: color,
                strokeOpacity: 0.9,
                strokeWeight: weight,
                map
            })
            linesRef.current.push(line)
        }

        redesRelaciones.forEach(r =>
            drawLine(byUbigeo[r.punto_inicial_ubigeo], byUbigeo[r.punto_final_ubigeo], '#22D3EE', 3)
        )
        arbolRelaciones.forEach(r =>
            drawLine(byNombre[r.punto_inicial], byNombre[r.punto_final], '#FACC15', 5)
        )

        return () => {
            linesRef.current.forEach(l => l.setMap(null))
            linesRef.current = []
        }
    }, [map, puntos, redesRelaciones, arbolRelaciones])

    return null
}
