'use client'

import { useState } from 'react'
import type { PuntoData, CoberturaForm, CoberturaViewModel } from './types'
import { BACKEND_URL } from './config'

interface CoberturaPanelProps {
    puntos: PuntoData[]
    onResult: (data: CoberturaViewModel) => void
}

export function CoberturaPanel({ puntos, onResult }: CoberturaPanelProps) {
    const [open, setOpen] = useState(false)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const [form, setForm] = useState<CoberturaForm>({
        ubigeo: '',
        numero_de_ldv: '72',
        muestras: '100',
        distancia_km: '15',
        altura_torre_fantasma: '15'
    })

    function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) {
        setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))
    }

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault()
        setLoading(true)
        setError(null)

        try {
            const body = {
                ubigeo: parseInt(form.ubigeo),
                numero_de_ldv: parseInt(form.numero_de_ldv),
                muestras: parseInt(form.muestras),
                distancia_km: parseFloat(form.distancia_km),
                altura_torre_fantasma: parseFloat(form.altura_torre_fantasma)
            }

            const res = await fetch(`${BACKEND_URL}/api/cobertura`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            })

            if (!res.ok) {
                const detail = await res.text()
                throw new Error(`HTTP ${res.status}: ${detail}`)
            }

            const data: CoberturaViewModel = await res.json()
            onResult(data)
            setOpen(false)
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : String(err))
        } finally {
            setLoading(false)
        }
    }

    const paramFields: { name: keyof CoberturaForm; label: string }[] = [
        { name: 'numero_de_ldv', label: 'Líneas de vista' },
        { name: 'muestras', label: 'Muestras' },
        { name: 'distancia_km', label: 'Distancia (km)' },
        { name: 'altura_torre_fantasma', label: 'Torre fantasma (m)' }
    ]

    return (
        <div className='w-72 rounded-2xl overflow-hidden shadow-2xl'>
            <button
                onClick={() => setOpen(v => !v)}
                className='w-full bg-gray-900/90 backdrop-blur-xl border border-white/10 px-5 py-4 text-left'
            >
                <span className='text-white font-bold text-base tracking-tight'>
                    Análisis de Cobertura
                </span>
                <p className='text-gray-400 text-xs mt-0.5'>
                    {open ? '▲ Cerrar' : '▼ Configurar y generar'}
                </p>
            </button>

            {open && (
                <>
                    <div className='h-px bg-white/10' />
                    <form
                        onSubmit={handleSubmit}
                        className='bg-gray-900/85 backdrop-blur-xl border-x border-b border-white/10 rounded-b-2xl px-5 py-4 space-y-3 max-h-[70vh] overflow-y-auto'
                    >
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
                                <label className='text-gray-400 text-xs block mb-0.5'>
                                    {label}
                                </label>
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

                        {error && (
                            <p className='text-red-400 text-xs bg-red-400/10 rounded-lg px-3 py-2'>
                                {error}
                            </p>
                        )}

                        <button
                            type='submit'
                            disabled={loading || !form.ubigeo}
                            className='w-full mt-1 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold text-sm rounded-xl py-2 transition-colors'
                        >
                            {loading ? 'Calculando…' : 'Generar cobertura'}
                        </button>
                    </form>
                </>
            )}
        </div>
    )
}
