'use client'

import { useEffect, useRef } from 'react'
import { useMap } from '@vis.gl/react-google-maps'
import type { PuntoData, RelacionRedData, GeoJsonGeometryMultiLineString } from '@/app/lib/types'

import { ITEM_COLORS } from '@/app/lib/utils'

export function MapOverlays({
    puntos,
    redesRelaciones = [],
    arbolRedGeojson = null
}: {
    puntos: PuntoData[]
    redesRelaciones?: RelacionRedData[]
    arbolRedGeojson?: GeoJsonGeometryMultiLineString | null
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
            drawLine(
                byUbigeo[r.punto_inicial_ubigeo],
                byUbigeo[r.punto_final_ubigeo],
                ITEM_COLORS[9],
                3
            )
        )

        arbolRedGeojson?.coordinates.forEach(coords => {
            if (coords.length < 2) return
            const [lng0, lat0] = coords[0]
            const [lng1, lat1] = coords[coords.length - 1]
            const line = new google.maps.Polyline({
                path: [{ lat: lat0, lng: lng0 }, { lat: lat1, lng: lng1 }],
                geodesic: true,
                strokeColor: ITEM_COLORS[5],
                strokeOpacity: 0.9,
                strokeWeight: 5,
                map
            })
            linesRef.current.push(line)
        })

        return () => {
            linesRef.current.forEach(l => l.setMap(null))
            linesRef.current = []
        }
    }, [map, puntos, redesRelaciones, arbolRedGeojson])

    return null
}
