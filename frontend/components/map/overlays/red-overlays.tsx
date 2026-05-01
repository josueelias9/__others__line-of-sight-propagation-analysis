'use client'

import { useEffect, useRef } from 'react'
import { useMap } from '@vis.gl/react-google-maps'
import type { RedData } from '@/app/lib/types'
import { ITEM_COLORS } from '@/app/lib/utils'

export function RedOverlays({ redes }: { redes: RedData[] }) {
    const map = useMap()
    const linesRef = useRef<google.maps.Polyline[]>([])

    useEffect(() => {
        linesRef.current.forEach(l => l.setMap(null))
        linesRef.current = []

        if (!map || redes.length === 0) return

        redes.forEach(red => {
            const color = ITEM_COLORS[red.id % ITEM_COLORS.length]
            red.geojson.coordinates.forEach(coords => {
                if (coords.length < 2) return
                const [lng0, lat0] = coords[0]
                const [lng1, lat1] = coords[coords.length - 1]
                const line = new google.maps.Polyline({
                    path: [{ lat: lat0, lng: lng0 }, { lat: lat1, lng: lng1 }],
                    geodesic: true,
                    strokeColor: color,
                    strokeOpacity: 0.9,
                    strokeWeight: 3,
                    map
                })
                linesRef.current.push(line)
            })
        })

        return () => {
            linesRef.current.forEach(l => l.setMap(null))
            linesRef.current = []
        }
    }, [map, redes])

    return null
}
