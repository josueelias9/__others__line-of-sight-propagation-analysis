'use client'

import { useEffect, useRef } from 'react'
import { useMap } from '@vis.gl/react-google-maps'
import type { PuntoData, GeoJsonGeometryMultiLineString } from '@/app/lib/types'

import { ITEM_COLORS } from '@/app/lib/utils'

export function MapOverlays({
    puntos,
    arbolRedGeojson = null
}: {
    puntos: PuntoData[]
    arbolRedGeojson?: GeoJsonGeometryMultiLineString | null
}) {
    const map = useMap()
    const linesRef = useRef<google.maps.Polyline[]>([])

    useEffect(() => {
        if (!map) return

        linesRef.current.forEach(l => l.setMap(null))
        linesRef.current = []

        arbolRedGeojson?.coordinates.forEach(coords => {
            if (coords.length < 2) return
            const [lng0, lat0] = coords[0]
            const [lng1, lat1] = coords[coords.length - 1]
            const line = new google.maps.Polyline({
                path: [
                    { lat: lat0, lng: lng0 },
                    { lat: lat1, lng: lng1 }
                ],
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
    }, [map, puntos, arbolRedGeojson])

    return null
}
