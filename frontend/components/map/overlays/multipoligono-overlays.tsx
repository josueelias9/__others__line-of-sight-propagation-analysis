'use client'

import { useEffect, useRef } from 'react'
import { useMap } from '@vis.gl/react-google-maps'
import type { MultipoligonoData } from '@/app/lib/types'
import { ITEM_COLORS } from '@/app/lib/utils'

function buildInfoContent(item: MultipoligonoData): string {
    return `
    <div style="font-family:sans-serif;font-size:12px;line-height:1.6;min-width:160px">
      <strong style="font-size:13px">${item.punto_nombre}</strong>
      <table style="margin-top:6px;border-collapse:collapse;width:100%">
        <tr><td style="color:#888;padding-right:8px">Distancia</td><td><b>${item.distancia_km} km</b></td></tr>
        <tr><td style="color:#888">Torre fantasma</td><td><b>${item.altura_torre_fantasma} m</b></td></tr>
        <tr><td style="color:#888">Líneas de vista</td><td><b>${item.numero_de_ldv}</b></td></tr>
        <tr><td style="color:#888">Muestras</td><td><b>${item.muestras}</b></td></tr>
      </table>
    </div>`
}

export function MultipoligonoOverlays({ items }: { items: MultipoligonoData[] }) {
    const map = useMap()
    const polysRef = useRef<google.maps.Polygon[]>([])
    const infoWindowRef = useRef<google.maps.InfoWindow | null>(null)

    useEffect(() => {
        polysRef.current.forEach(p => p.setMap(null))
        polysRef.current = []
        infoWindowRef.current?.close()

        if (!map || items.length === 0) return

        const infoWindow = new google.maps.InfoWindow()
        infoWindowRef.current = infoWindow

        items.forEach(item => {
            const color = ITEM_COLORS[item.id % ITEM_COLORS.length]
            const { geometry } = item.geojson
            if (!geometry) return

            const polygons =
                geometry.type === 'Polygon' ? [geometry.coordinates] : geometry.coordinates

            polygons.forEach(rings => {
                const paths = rings.map(ring => ring.map(([lng, lat]) => ({ lat, lng })))
                const poly = new google.maps.Polygon({
                    paths,
                    strokeColor: color,
                    strokeOpacity: 0.9,
                    strokeWeight: 2,
                    fillColor: color,
                    fillOpacity: 0.12,
                    map
                })
                poly.addListener('click', (e: google.maps.MapMouseEvent) => {
                    infoWindow.setContent(buildInfoContent(item))
                    infoWindow.setPosition(e.latLng)
                    infoWindow.open(map)
                })
                polysRef.current.push(poly)
            })
        })

        return () => {
            polysRef.current.forEach(p => p.setMap(null))
            infoWindow.close()
        }
    }, [map, items])

    return null
}
