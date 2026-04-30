'use client'

import { useEffect, useRef, useState } from 'react'
import type { RedData, RelacionRedData } from '../types'
import { BACKEND_URL } from '../config'
import { PanelFrame } from '../panel-frame'

const NET_COLORS = [
    '#60A5FA',
    '#F472B6',
    '#A78BFA',
    '#FB923C',
    '#34D399',
    '#FACC15',
    '#F87171',
    '#2DD4BF'
]

interface RedPanelProps {
    refreshKey?: number
    onSelectionChange: (relaciones: RelacionRedData[]) => void
}

export function RedPanel({ refreshKey = 0, onSelectionChange }: RedPanelProps) {
    const [open, setOpen] = useState(false)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [redes, setRedes] = useState<RedData[]>([])
    const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set())
    const loadedOnceRef = useRef(false)

    async function load() {
        setLoading(true)
        setError(null)
        try {
            const res = await fetch(`${BACKEND_URL}/api/redes`)
            if (!res.ok) throw new Error(`HTTP ${res.status}`)
            const data: RedData[] = await res.json()
            setRedes(data)
            setSelectedIds(new Set(data.map(r => r.id)))
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : String(err))
        } finally {
            setLoading(false)
        }
    }

    async function handleDelete(id: number) {
        await fetch(`${BACKEND_URL}/api/redes/${id}`, { method: 'DELETE' })
        const next = redes.filter(r => r.id !== id)
        setRedes(next)
        setSelectedIds(prev => {
            const s = new Set(prev)
            s.delete(id)
            return s
        })
    }

    function toggleRed(id: number) {
        setSelectedIds(prev => {
            const s = new Set(prev)
            s.has(id) ? s.delete(id) : s.add(id)
            return s
        })
    }

    // Propagate selected relaciones to parent
    useEffect(() => {
        const relaciones: RelacionRedData[] = []
        for (const red of redes) {
            if (selectedIds.has(red.id)) {
                relaciones.push(...red.relaciones)
            }
        }
        onSelectionChange(relaciones)
    }, [redes, selectedIds, onSelectionChange])

    // Load only once on first open (ref prevents repeated fetches even if data is empty)
    useEffect(() => {
        if (open && !loadedOnceRef.current) {
            loadedOnceRef.current = true
            load()
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [open])

    // Force reload when a new red is saved externally
    useEffect(() => {
        if (refreshKey > 0) load()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [refreshKey])

    return (
        <PanelFrame
            title='Redes guardadas'
            closedLabel='Ver y seleccionar'
            open={open}
            onToggle={() => setOpen(v => !v)}
            contentClassName='max-h-[60vh] overflow-y-auto'
        >
                        <div className='flex items-center justify-between'>
                            <span className='text-gray-400 text-xs'>
                                {redes.length} red{redes.length !== 1 ? 'es' : ''}
                            </span>
                            <button
                                onClick={load}
                                disabled={loading}
                                className='text-gray-400 hover:text-white text-xs disabled:opacity-50 transition-colors'
                            >
                                {loading ? '…' : '↺ Recargar'}
                            </button>
                        </div>

                        {error && (
                            <p className='text-red-400 text-xs bg-red-400/10 rounded-lg px-3 py-2'>
                                {error}
                            </p>
                        )}

                        {!loading && redes.length === 0 && (
                            <p className='text-gray-500 text-xs text-center py-2'>
                                Sin redes guardadas
                            </p>
                        )}

                        {redes.map(red => {
                            const color = NET_COLORS[red.id % NET_COLORS.length]
                            const active = selectedIds.has(red.id)
                            return (
                                <div
                                    key={red.id}
                                    className='bg-gray-800/40 rounded-xl overflow-hidden'
                                >
                                    <div className='flex items-center gap-3 px-3 py-2.5'>
                                        {/* color swatch + toggle */}
                                        <button
                                            onClick={() => toggleRed(red.id)}
                                            className='shrink-0 w-4 h-4 rounded-sm border-2 transition-all'
                                            style={{
                                                backgroundColor: active ? color : 'transparent',
                                                borderColor: color,
                                                opacity: active ? 1 : 0.5
                                            }}
                                            title={active ? 'Ocultar en mapa' : 'Mostrar en mapa'}
                                        />

                                        {/* info */}
                                        <div className='flex-1 min-w-0'>
                                            <p className='text-white text-xs font-medium truncate'>
                                                {red.nombre || (
                                                    <span className='text-gray-500 italic'>
                                                        sin nombre
                                                    </span>
                                                )}
                                            </p>
                                            <p className='text-gray-500 text-xs'>
                                                #{red.id} · {red.relaciones.length} enlace
                                                {red.relaciones.length !== 1 ? 's' : ''}
                                            </p>
                                        </div>

                                        {/* delete */}
                                        <button
                                            onClick={() => handleDelete(red.id)}
                                            className='shrink-0 text-red-400 hover:text-red-300 text-xs px-1.5 py-1 rounded-lg hover:bg-red-400/10 transition-colors'
                                            title='Eliminar'
                                        >
                                            ✕
                                        </button>
                                    </div>
                                </div>
                            )
                        })}
        </PanelFrame>
    )
}
