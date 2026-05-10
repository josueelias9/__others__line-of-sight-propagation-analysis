'use client'

import { useEffect, useState } from 'react'
import { useFormState as useActionState } from 'react-dom'
import type { PuntoData, CoberturaForm } from '@/app/lib/types'
import { calcularCobertura, type CoberturaState } from '@/app/lib/actions'
import { PanelFrame } from '@/components/map/panel-layout'
import type { CoberturaViewModel } from '@/app/lib/types'

interface CoberturaPanelProps {
    puntos: PuntoData[]
    onResult: (data: CoberturaViewModel) => void
}

const initialState: CoberturaState = { result: null, error: null }

export function CoberturaPanel({ puntos, onResult }: CoberturaPanelProps) {
    const [open, setOpen] = useState(false)
    const [state, formAction, isPending] = useActionState(calcularCobertura, initialState)

    const [form, setForm] = useState<CoberturaForm>({
        ubigeo: '',
        numero_de_ldv: '100',
        muestras: '100',
        distancia_km: '15',
        altura_torre_fantasma: '15'
    })

    function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) {
        setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))
    }

    useEffect(() => {
        if (state?.result) {
            onResult(state.result)
            setOpen(false)
        }
    }, [state?.result]) // eslint-disable-line react-hooks/exhaustive-deps

    const paramFields: { name: keyof CoberturaForm; label: string }[] = [
        { name: 'numero_de_ldv', label: 'Líneas de vista' },
        { name: 'muestras', label: 'Muestras' },
        { name: 'distancia_km', label: 'Distancia (km)' },
        { name: 'altura_torre_fantasma', label: 'Torre fantasma (m)' }
    ]

    return (
        <PanelFrame
            title='Análisis de Cobertura'
            closedLabel='Configurar y generar'
            open={open}
            onToggle={() => setOpen(v => !v)}
            contentClassName='max-h-[70vh] overflow-y-auto'
        >
            <form action={formAction} className='space-y-3'>
                {/* Selector de punto */}
                <div>
                    <label className='text-gray-400 text-xs block mb-0.5'>Punto</label>
                    <select
                        name='ubigeo'
                        value={form.ubigeo}
                        onChange={handleChange}
                        required
                        className='w-full bg-gray-800/60 border border-white/10 rounded-lg px-3 py-1.5 text-white text-sm focus:outline-none focus:ring-1 focus:ring-emerald-400/60'
                    >
                        <option value='' disabled>
                            Seleccionar punto…
                        </option>
                        {puntos.map(p => (
                            <option key={p.ubigeo} value={p.ubigeo}>
                                [{p.ubigeo}] {p.nombre} ({p.tipo})
                            </option>
                        ))}
                    </select>
                </div>

                {/* Parámetros de análisis */}
                {paramFields.map(({ name, label }) => (
                    <div key={name}>
                        <label className='text-gray-400 text-xs block mb-0.5'>{label}</label>
                        <input
                            name={name}
                            value={form[name]}
                            onChange={handleChange}
                            type='number'
                            step='any'
                            required
                            className='w-full bg-gray-800/60 border border-white/10 rounded-lg px-3 py-1.5 text-white text-sm focus:outline-none focus:ring-1 focus:ring-emerald-400/60'
                        />
                    </div>
                ))}

                {state?.error && (
                    <p className='text-red-400 text-xs bg-red-400/10 rounded-lg px-3 py-2'>
                        {state?.error}
                    </p>
                )}

                <button
                    type='submit'
                    disabled={isPending || !form.ubigeo}
                    className='w-full mt-1 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold text-sm rounded-xl py-2 transition-colors'
                >
                    {isPending ? 'Calculando…' : 'Generar cobertura'}
                </button>
            </form>
        </PanelFrame>
    )
}
