'use client'

import { Fragment, ReactNode, useEffect, useRef, useState } from 'react'
import type { MultipoligonoData, RedData } from '@/app/lib/types'
import { PanelFrame } from '@/components/map/panel-layout'
import { ITEM_COLORS } from '@/app/lib/utils'
import { eliminarRed, eliminarCobertura } from '@/app/lib/actions'
import { fetchRedes, fetchSavedCoberturas } from '@/app/lib/data'

// ─── Internal generic base ─────────────────────────────────────────────────────

interface GenericPanelProps<T extends { id: number }> {
    title: string
    reloadAction: () => Promise<T[]>
    deleteAction: (id: number) => Promise<void>
    countLabel: (n: number) => string
    emptyText: string
    renderRow: (item: T, expanded: boolean, onExpand: () => void) => ReactNode
    details?: (item: T) => Array<[string, string]>
    onVisibleItemsChange: (items: T[]) => void
    initialItems?: T[]
}

function GenericPanel<T extends { id: number }>({
    title,
    reloadAction,
    deleteAction,
    countLabel,
    emptyText,
    renderRow,
    details,
    onVisibleItemsChange,
    initialItems
}: GenericPanelProps<T>) {
    const [open, setOpen] = useState(false)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const [items, setItems] = useState<T[]>(initialItems ?? [])
    const [visibleIds, setVisibleIds] = useState<Set<number>>(
        new Set((initialItems ?? []).map(i => i.id))
    )
    const [expandedId, setExpandedId] = useState<number | null>(null)

    async function load() {
        setLoading(true)
        setError(null)
        try {
            const data = await reloadAction()
            setItems(data)
            setVisibleIds(new Set(data.map(d => d.id)))
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : String(err))
        } finally {
            setLoading(false)
        }
    }

    async function handleDelete(id: number) {
        await deleteAction(id)
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

    const onVisibleItemsChangeRef = useRef(onVisibleItemsChange)
    useEffect(() => {
        onVisibleItemsChangeRef.current = onVisibleItemsChange
    })

    useEffect(() => {
        onVisibleItemsChangeRef.current(items.filter(i => visibleIds.has(i.id)))
    }, [items, visibleIds])

    return (
        <PanelFrame
            title={title}
            closedLabel='Ver y seleccionar'
            open={open}
            onToggle={() => setOpen(v => !v)}
            contentClassName='max-h-[60vh] overflow-y-auto'
        >
            <div className='flex items-center justify-between'>
                <span className='text-gray-400 text-xs'>{countLabel(items.length)}</span>
                <button
                    onClick={load}
                    disabled={loading}
                    className='text-gray-400 hover:text-white text-xs disabled:opacity-50 transition-colors'
                >
                    {loading ? '…' : '↺ Recargar'}
                </button>
            </div>

            {error && (
                <p className='text-red-400 text-xs bg-red-400/10 rounded-lg px-3 py-2'>{error}</p>
            )}

            {!loading && items.length === 0 && (
                <p className='text-gray-500 text-xs text-center py-2'>{emptyText}</p>
            )}

            {items.map(item => {
                const color = ITEM_COLORS[item.id % ITEM_COLORS.length]
                const active = visibleIds.has(item.id)
                const expanded = expandedId === item.id
                return (
                    <div key={item.id} className='bg-gray-800/40 rounded-xl overflow-hidden'>
                        <div className='flex items-center gap-3 px-3 py-2'>
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
                            {renderRow(item, expanded, () =>
                                setExpandedId(expanded ? null : item.id)
                            )}
                            <button
                                onClick={() => handleDelete(item.id)}
                                className='shrink-0 text-red-400 hover:text-red-300 text-xs px-1.5 py-1 rounded-lg hover:bg-red-400/10 transition-colors'
                                title='Eliminar'
                            >
                                ✕
                            </button>
                        </div>
                        {expanded && details && (
                            <div className='border-t border-white/5 px-3 pb-2 pt-1.5 grid grid-cols-2 gap-x-4 gap-y-1'>
                                {details(item).map(([label, value]) => (
                                    <Fragment key={label}>
                                        <span className='text-gray-500 text-xs'>{label}</span>
                                        <span className='text-gray-200 text-xs'>{value}</span>
                                    </Fragment>
                                ))}
                            </div>
                        )}
                    </div>
                )
            })}
        </PanelFrame>
    )
}

// ─── Public API ───────────────────────────────────────────────────────────────

export type SavedItemsPanelProps =
    | {
          kind: 'coberturas'
          initialItems?: MultipoligonoData[]
          onVisibleItemsChange: (items: MultipoligonoData[]) => void
      }
    | {
          kind: 'redes'
          initialItems?: RedData[]
          onVisibleItemsChange: (items: RedData[]) => void
      }

export function SavedItemsPanel(props: SavedItemsPanelProps) {
    if (props.kind === 'coberturas') {
        return (
            <GenericPanel<MultipoligonoData>
                title='Coberturas guardadas'
                reloadAction={fetchSavedCoberturas}
                deleteAction={eliminarCobertura}
                initialItems={props.initialItems}
                countLabel={n => `${n} cobertura${n !== 1 ? 's' : ''}`}
                emptyText='Sin coberturas guardadas'
                onVisibleItemsChange={props.onVisibleItemsChange}
                renderRow={(item, expanded, onExpand) => (
                    <button onClick={onExpand} className='flex-1 min-w-0 text-left'>
                        <p className='text-white text-xs font-medium truncate'>
                            {item.punto_nombre}
                        </p>
                        <p className='text-gray-500 text-xs'>
                            #{item.id} · {item.distancia_km} km · {expanded ? '▲' : '▼'}
                        </p>
                    </button>
                )}
                details={item => [
                    ['Punto', item.punto_nombre],
                    ['Distancia', `${item.distancia_km} km`],
                    ['Torre fantasma', `${item.altura_torre_fantasma} m`],
                    ['Líneas de vista', String(item.numero_de_ldv)],
                    ['Muestras', String(item.muestras)]
                ]}
            />
        )
    }

    return (
        <GenericPanel<RedData>
            title='Redes guardadas'
            reloadAction={fetchRedes}
            deleteAction={eliminarRed}
            initialItems={props.initialItems}
            countLabel={n => `${n} red${n !== 1 ? 'es' : ''}`}
            emptyText='Sin redes guardadas'
            onVisibleItemsChange={props.onVisibleItemsChange}
            renderRow={(item, expanded, onExpand) => (
                <button onClick={onExpand} className='flex-1 min-w-0 text-left'>
                    <p className='text-white text-xs font-medium truncate'>
                        {item.nombre || 'sin nombre'}
                    </p>
                    <p className='text-gray-500 text-xs'>
                        #{item.id} · {item.relaciones.length} enlace
                        {item.relaciones.length !== 1 ? 's' : ''} · {expanded ? '▲' : '▼'}
                    </p>
                </button>
            )}
            details={item => [
                ['Nombre', item.nombre || 'sin nombre'],
                ['ID', String(item.id)],
                ['Enlaces', String(item.relaciones.length)]
            ]}
        />
    )
}

