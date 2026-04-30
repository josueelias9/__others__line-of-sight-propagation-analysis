'use client'

import { useEffect, useRef } from 'react'
import { useMap } from '@vis.gl/react-google-maps'
import type { CoberturaViewModel, GeoJsonFeature } from '../types'

function geojsonToGooglePolygons(
    geojson: GeoJsonFeature,
    map: google.maps.Map,
    options: Omit<google.maps.PolygonOptions, 'paths' | 'map'>
): google.maps.Polygon[] {
    const { geometry } = geojson
    if (!geometry) return []

    const ringToLatLng = (ring: [number, number][]) => ring.map(([lng, lat]) => ({ lat, lng }))

    if (geometry.type === 'Polygon') {
        const paths = geometry.coordinates.map(ringToLatLng)
        return [new google.maps.Polygon({ ...options, paths, map })]
    }

    if (geometry.type === 'MultiPolygon') {
        return geometry.coordinates.map(polygon => {
            const paths = polygon.map(ringToLatLng)
            return new google.maps.Polygon({ ...options, paths, map })
        })
    }

    return []
}

export function CoberturaOverlays({
    data,
    showMalla = false
}: {
    data: CoberturaViewModel | null
    showMalla?: boolean
}) {
    const map = useMap()
    const mallaCellsRef = useRef<google.maps.Polygon[]>([])
    const geojsonPolysRef = useRef<google.maps.Polygon[]>([])

    useEffect(() => {
        mallaCellsRef.current.forEach(p => p.setMap(null))
        geojsonPolysRef.current.forEach(p => p.setMap(null))
        mallaCellsRef.current = []
        geojsonPolysRef.current = []

        if (!map || !data) return

        if (showMalla) {
            mallaCellsRef.current = geojsonToGooglePolygons(data.malla_geojson, map, {
                strokeColor: '#34D399',
                strokeOpacity: 0.4,
                strokeWeight: 1,
                fillColor: '#34D399',
                fillOpacity: 0.25
            })
        }

        geojsonPolysRef.current = geojsonToGooglePolygons(data.geojson, map, {
            strokeColor: '#FBBF24',
            strokeOpacity: 0.9,
            strokeWeight: 2,
            fillColor: '#FBBF24',
            fillOpacity: 0.15
        })

        return () => {
            mallaCellsRef.current.forEach(p => p.setMap(null))
            geojsonPolysRef.current.forEach(p => p.setMap(null))
        }
    }, [map, data, showMalla])

    return null
}
