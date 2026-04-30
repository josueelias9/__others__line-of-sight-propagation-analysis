'use client'

import { useEffect } from 'react'
import { useMap } from '@vis.gl/react-google-maps'

export function MapControls() {
    const map = useMap()

    useEffect(() => {
        if (!map) return

        const buttons: [string, string, number, google.maps.ControlPosition][] = [
            ['Rotate Left', 'rotate', 20, google.maps.ControlPosition.LEFT_CENTER],
            ['Rotate Right', 'rotate', -20, google.maps.ControlPosition.RIGHT_CENTER],
            ['Tilt Down', 'tilt', 20, google.maps.ControlPosition.TOP_CENTER],
            ['Tilt Up', 'tilt', -20, google.maps.ControlPosition.BOTTOM_CENTER]
        ]

        const addedDivs: { position: google.maps.ControlPosition; div: HTMLDivElement }[] = []

        buttons.forEach(([text, mode, amount, position]) => {
            const div = document.createElement('div')
            const btn = document.createElement('button')
            btn.textContent = text
            btn.style.cssText =
                'background:#fff;border:none;border-radius:4px;box-shadow:0 2px 6px rgba(0,0,0,.3);' +
                'cursor:pointer;font-size:14px;font-weight:600;margin:8px;padding:8px 12px;'
            btn.addEventListener('click', () => {
                if (mode === 'rotate') map.setHeading((map.getHeading() ?? 0) + amount)
                if (mode === 'tilt') map.setTilt((map.getTilt() ?? 0) + amount)
            })
            div.appendChild(btn)
            map.controls[position].push(div)
            addedDivs.push({ position, div })
        })

        // ── Middle-mouse drag → rotate ─────────────────────────────────────────────
        const container = map.getDiv()
        let activePointerId: number | null = null
        let lastX = 0

        const onPointerDown = (e: PointerEvent) => {
            if (e.button !== 1) return
            e.preventDefault()
            activePointerId = e.pointerId
            lastX = e.clientX
            container.setPointerCapture(e.pointerId)
        }
        const onPointerMove = (e: PointerEvent) => {
            if (e.pointerId !== activePointerId) return
            map.setHeading((map.getHeading() ?? 0) + (e.clientX - lastX) * 0.5)
            lastX = e.clientX
        }
        const onPointerUp = (e: PointerEvent) => {
            if (e.pointerId !== activePointerId) return
            activePointerId = null
            container.releasePointerCapture(e.pointerId)
        }

        container.addEventListener('pointerdown', onPointerDown)
        container.addEventListener('pointermove', onPointerMove)
        container.addEventListener('pointerup', onPointerUp)
        container.addEventListener('pointercancel', onPointerUp)

        return () => {
            addedDivs.forEach(({ position, div }) => {
                const arr = map.controls[position]
                for (let i = 0; i < arr.getLength(); i++) {
                    if (arr.getAt(i) === div) {
                        arr.removeAt(i)
                        break
                    }
                }
            })
            container.removeEventListener('pointerdown', onPointerDown)
            container.removeEventListener('pointermove', onPointerMove)
            container.removeEventListener('pointerup', onPointerUp)
            container.removeEventListener('pointercancel', onPointerUp)
        }
    }, [map])

    return null
}
