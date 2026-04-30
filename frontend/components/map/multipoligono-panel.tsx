'use client'

import { useEffect, useState } from 'react'
import type { MultipoligonoData } from './types'
import { BACKEND_URL } from './config'

const ITEM_COLORS = [
    '#60A5FA',
    '#F472B6',
    '#A78BFA',
    '#FB923C',
    '#34D399',
    '#FACC15',
    '#F87171',
    '#2DD4BF'
]

interface MultipoligonoPanelProps {
    onVisibleItemsChange: (items: MultipoligonoData[]) => void
}

export function MultipoligonoPanel({ onVisibleItemsChange }: MultipoligonoPanelProps) {
    const [open, setOpen] = useState(false)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [items, setItems] = useState<MultipoligonoData[]>([])
    const [visibleIds, setVisibleIds] = useState<Set<number>>(new Set())
    const [expandedId, setExpandedId] = useState<number | null>(null)

    async function load() {
        setLoading(true)
        setError(null)
        try {
            const res = await fetch(`${BACKEND_URL}/api/cobertura`)
            if (!res.ok) throw new Error(`HTTP ${res.status}`)
            const data: MultipoligonoData[] = await res.json()
            setItems(data)
            // auto-enable all newly loaded items
            setVisibleIds(new Set(data.map(d => d.id)))
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : String(err))
        } finally {
            setLoading(false)
        }
    }

    async function handleDelete(id: number) {
        await fetch(`${BACKEND_URL}/api/cobertura/${id}`, { method: 'DELETE' })
        const next = items.filter(i => i.id !== id)
        setItems(next)
        setVisibleIds(prev => {
            const s = new Set(prev)
            s.delete(id)
            return s
        })
    }

    function toggleItem(id: number) {
        setVisibleIds(prev => {
            const s = new Set(prev)
            s.has(id) ? s.delete(id) : s.add(id)
            return s
        })
    }

    // Notify parent whenever visible set or items change
    useEffect(() => {
        onVisibleItemsChange(items.filter(i => visibleIds.has(i.id)))
    }, [items, visibleIds, onVisibleItemsChange])

    useEffect(() => {
        if (open && items.length === 0) load()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [open])

    return (
        <div className='w-72 rounded-2xl overflow-hidden shadow-2xl'>
            <button
                onClick={() => setOpen(v => !v)}
                className='w-full bg-gray-900/90 backdrop-blur-xl border border-white/10 px-5 py-4 text-left'
            >
                <span className='text-white font-bold text-base tracking-tight'>
                    Coberturas guardadas
                </span>
                <p className='text-gray-400 text-xs mt-0.5'>
                    {open ? '▲ Cerrar' : '▼ Ver y seleccionar'}
                </p>
            </button>

            {open && (
                <>
                    <div className='h-px bg-white/10' />
                    <div className='bg-gray-900/85 backdrop-blur-xl border-x border-b border-white/10 rounded-b-2xl px-5 py-4 space-y-3 max-h-[60vh] overflow-y-auto'>
                        <div className='flex items-center justify-between'>
                            <span className='text-gray-400 text-xs'>
                                {items.length} cobertura{items.length !== 1 ? 's' : ''}
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

                        {!loading && items.length === 0 && (
                            <p className='text-gray-500 text-xs text-center py-2'>
                                Sin coberturas guardadas
                            </p>
                        )}

                        {items.map(item => {
                            const color = ITEM_COLORS[item.id % ITEM_COLORS.length]
                            const active = visibleIds.has(item.id)
                            const expanded = expandedId === item.id
                            return (
                                <div
                                    key={item.id}
                                    className='bg-gray-800/40 rounded-xl overflow-hidden'
                                >
                                    <div className='flex items-center gap-3 px-3 py-2'>
                                        {/* color swatch + toggle */}
                                        <button
                                            onClick={() => toggleItem(item.id)}
                                            className='shrink-0 w-4 h-4 rounded-sm border-2 transition-opacity'
                                            style={{
                                                backgroundColor: active ? color : 'transparent',
                                                borderColor: color,
                                                opacity: active ? 1 : 0.6
                                            }}
                                            title={active ? 'Ocultar' : 'Mostrar'}
                                        />

                                        {/* info — click to expand */}
                                        <button
                                            onClick={() => setExpandedId(expanded ? null : item.id)}
                                            className='flex-1 min-w-0 text-left'
                                        >
                                            <p className='text-white text-xs font-medium truncate'>
                                                {item.punto_nombre}
                                            </p>
                                            <p className='text-gray-500 text-xs'>
                                                #{item.id} · {item.distancia_km} km ·{' '}
                                                {expanded ? '▲' : '▼'}
                                            </p>
                                        </button>

                                        {/* delete */}
                                        <button
                                            onClick={() => handleDelete(item.id)}
                                            className='shrink-0 text-red-400 hover:text-red-300 text-xs px-1.5 py-1 rounded-lg hover:bg-red-400/10 transition-colors'
                                            title='Eliminar'
                                        >
                                            ✕
                                        </button>
                                    </div>

                                    {expanded && (
                                        <div className='border-t border-white/5 px-3 pb-2 pt-1.5 grid grid-cols-2 gap-x-4 gap-y-1'>
                                            <span className='text-gray-500 text-xs'>Punto</span>
                                            <span className='text-gray-200 text-xs font-medium'>
                                                {item.punto_nombre}
                                            </span>
                                            <span className='text-gray-500 text-xs'>Distancia</span>
                                            <span className='text-gray-200 text-xs'>
                                                {item.distancia_km} km
                                            </span>
                                            <span className='text-gray-500 text-xs'>
                                                Torre fantasma
                                            </span>
                                            <span className='text-gray-200 text-xs'>
                                                {item.altura_torre_fantasma} m
                                            </span>
                                            <span className='text-gray-500 text-xs'>
                                                Líneas de vista
                                            </span>
                                            <span className='text-gray-200 text-xs'>
                                                {item.numero_de_ldv}
                                            </span>
                                            <span className='text-gray-500 text-xs'>Muestras</span>
                                            <span className='text-gray-200 text-xs'>
                                                {item.muestras}
                                            </span>
                                        </div>
                                    )}
                                </div>
                            )
                        })}
                    </div>
                </>
            )}
        </div>
    )
}
