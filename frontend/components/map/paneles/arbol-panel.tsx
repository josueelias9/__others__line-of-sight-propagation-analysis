'use client'

import { useEffect, useState } from 'react'
import { useFormState as useActionState } from 'react-dom'
import type { PuntoData, ArbolResult } from '@/app/lib/types'
import { calcularArbol, type ArbolState } from '@/app/lib/actions'
import { PanelFrame } from '@/components/map/panel-layout'

interface ArbolPanelProps {
    puntos: PuntoData[]
    onResult: (data: ArbolResult) => void
}

const initialState: ArbolState = { result: null, error: null }

export function ArbolPanel({ puntos, onResult }: ArbolPanelProps) {
    const [open, setOpen] = useState(false)
    const [state, formAction, isPending] = useActionState(calcularArbol, initialState)

    const tipos = Array.from(new Set(puntos.map(p => p.tipo))).sort()

    const [tipoConectados, setTipoConectados] = useState('')
    const [tipoNoConectados, setTipoNoConectados] = useState('')

    useEffect(() => {
        if (state.result) {
            onResult(state.result)
            setOpen(false)
        }
    }, [state.result]) // eslint-disable-line react-hooks/exhaustive-deps

    const canSubmit = tipoConectados && tipoNoConectados && tipoConectados !== tipoNoConectados

    return (
        <PanelFrame
            title='Árbol de Conexión LOS'
            closedLabel='Seleccionar tipos y calcular'
            open={open}
            onToggle={() => setOpen(v => !v)}
        >
            <form action={formAction} className='space-y-3'>
                <div>
                    <label className='text-gray-400 text-xs block mb-0.5'>
                        Tipo BASE / Conectados
                    </label>
                    <select
                        name='tipo_conectados'
                        value={tipoConectados}
                        onChange={e => setTipoConectados(e.target.value)}
                        required
                        className='w-full bg-gray-800/60 border border-white/10 rounded-lg px-3 py-1.5 text-white text-sm focus:outline-none focus:ring-1 focus:ring-cyan-400/60'
                    >
                        <option value='' disabled>
                            Seleccionar tipo…
                        </option>
                        {tipos.map(t => (
                            <option key={t} value={t}>
                                {t}
                            </option>
                        ))}
                    </select>
                </div>

                <div>
                    <label className='text-gray-400 text-xs block mb-0.5'>Tipo a CONECTAR</label>
                    <select
                        name='tipo_no_conectados'
                        value={tipoNoConectados}
                        onChange={e => setTipoNoConectados(e.target.value)}
                        required
                        className='w-full bg-gray-800/60 border border-white/10 rounded-lg px-3 py-1.5 text-white text-sm focus:outline-none focus:ring-1 focus:ring-cyan-400/60'
                    >
                        <option value='' disabled>
                            Seleccionar tipo…
                        </option>
                        {tipos.map(t => (
                            <option key={t} value={t}>
                                {t}
                            </option>
                        ))}
                    </select>
                    {tipoConectados && tipoNoConectados && tipoConectados === tipoNoConectados && (
                        <p className='text-amber-400 text-xs mt-1'>
                            Los tipos deben ser distintos.
                        </p>
                    )}
                </div>

                <div>
                    <label className='text-gray-400 text-xs block mb-0.5'>
                        Distancia máxima (km)
                    </label>
                    <input
                        type='number'
                        name='distancia_maxima'
                        step='any'
                        min='0.1'
                        defaultValue='20'
                        required
                        className='w-full bg-gray-800/60 border border-white/10 rounded-lg px-3 py-1.5 text-white text-sm focus:outline-none focus:ring-1 focus:ring-cyan-400/60'
                    />
                </div>

                <div>
                    <label className='text-gray-400 text-xs block mb-0.5'>
                        Muestras de elevación
                    </label>
                    <input
                        type='number'
                        name='muestras'
                        min='10'
                        defaultValue='100'
                        required
                        className='w-full bg-gray-800/60 border border-white/10 rounded-lg px-3 py-1.5 text-white text-sm focus:outline-none focus:ring-1 focus:ring-cyan-400/60'
                    />
                </div>

                <div>
                    <label className='text-gray-400 text-xs block mb-0.5'>
                        Nombre de la red (opcional)
                    </label>
                    <input
                        type='text'
                        name='nombre_red'
                        placeholder='Ej: Red norte…'
                        className='w-full bg-gray-800/60 border border-white/10 rounded-lg px-3 py-1.5 text-white text-sm placeholder-gray-600 focus:outline-none focus:ring-1 focus:ring-cyan-400/60'
                    />
                </div>

                {state.error && (
                    <p className='text-red-400 text-xs bg-red-400/10 rounded-lg px-3 py-2'>
                        {state.error}
                    </p>
                )}

                <button
                    type='submit'
                    disabled={isPending || !canSubmit}
                    className='w-full mt-1 bg-cyan-500 hover:bg-cyan-400 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold text-sm rounded-xl py-2 transition-colors'
                >
                    {isPending ? 'Calculando…' : 'Calcular árbol'}
                </button>
            </form>
        </PanelFrame>
    )
}
