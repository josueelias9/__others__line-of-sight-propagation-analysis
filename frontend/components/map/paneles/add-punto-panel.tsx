'use client'

import { useEffect, useState } from 'react'
import { useActionState } from 'react'
import type { ChangeEvent } from 'react'
import type { PuntoData } from '@/app/lib/types'
import { agregarPunto, type PuntoState } from '@/app/lib/actions'

interface AddPuntoPanelProps {
    onAdded: (punto: PuntoData) => void
    onRequestPick: () => void
    pickedCoords: { lat: number; lng: number } | null
    onPickConsumed: () => void
}

interface AddPuntoForm {
    nombre: string
    longitud: string
    latitud: string
    altura_antena: string
    tipo: string
    green_asociado: string
}

const INITIAL_FORM: AddPuntoForm = {
    nombre: '',
    longitud: '',
    latitud: '',
    altura_antena: '15',
    tipo: 'acceso',
    green_asociado: ''
}

const initialState: PuntoState = { result: null, error: null }

export function AddPuntoPanel({
    onAdded,
    onRequestPick,
    pickedCoords,
    onPickConsumed
}: AddPuntoPanelProps) {
    const [open, setOpen] = useState(false)
    const [state, formAction, isPending] = useActionState(agregarPunto, initialState)
    const [form, setForm] = useState<AddPuntoForm>(INITIAL_FORM)

    // When coordinates are picked from the map, fill the form and open the panel
    useEffect(() => {
        if (pickedCoords) {
            setForm(prev => ({
                ...prev,
                latitud: pickedCoords.lat.toFixed(6),
                longitud: pickedCoords.lng.toFixed(6)
            }))
            setOpen(true)
            onPickConsumed()
        }
    }, [pickedCoords]) // eslint-disable-line react-hooks/exhaustive-deps

    useEffect(() => {
        if (state.result) {
            onAdded(state.result)
            setForm(INITIAL_FORM)
            setOpen(false)
        }
    }, [state.result]) // eslint-disable-line react-hooks/exhaustive-deps

    function handleChange(e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) {
        setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))
    }

    return (
        <>
            {/* Floating button */}
            <div className='absolute bottom-6 right-6 z-10 flex flex-col gap-2 items-end'>
                <button
                    onClick={() => {
                        setForm(INITIAL_FORM)
                        setOpen(true)
                    }}
                    className='flex items-center gap-2 px-4 py-2.5 rounded-2xl bg-cyan-500 hover:bg-cyan-400 text-gray-950 font-bold text-sm shadow-xl shadow-cyan-500/40 transition-all'
                >
                    <span className='text-lg leading-none'>+</span>
                    Agregar punto
                </button>
            </div>

            {/* Modal panel */}
            {open && (
                <div className='absolute inset-0 z-20 flex items-center justify-center bg-black/50 backdrop-blur-sm'>
                    <div className='w-full max-w-sm mx-4 bg-gray-900 border border-white/10 rounded-2xl shadow-2xl overflow-hidden'>
                        {/* Header */}
                        <div className='px-6 py-4 border-b border-white/10 flex items-center justify-between'>
                            <span className='text-white font-bold text-base'>Nuevo punto</span>
                            <button
                                onClick={() => setOpen(false)}
                                className='text-gray-400 hover:text-white text-xl leading-none transition-colors'
                            >
                                ×
                            </button>
                        </div>

                        {/* Form */}
                        <form action={formAction} className='px-6 py-4 space-y-4'>
                            {/* Nombre */}
                            <div className='space-y-1'>
                                <label className='text-gray-400 text-xs font-semibold uppercase tracking-wide'>
                                    Nombre
                                </label>
                                <input
                                    required
                                    name='nombre'
                                    value={form.nombre}
                                    onChange={handleChange}
                                    placeholder='ej. acceso11'
                                    className='w-full bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-white text-sm placeholder-gray-600 focus:outline-none focus:border-cyan-500 transition-colors'
                                />
                            </div>

                            {/* Tipo */}
                            <div className='space-y-1'>
                                <label className='text-gray-400 text-xs font-semibold uppercase tracking-wide'>
                                    Tipo
                                </label>
                                <select
                                    name='tipo'
                                    value={form.tipo}
                                    onChange={handleChange}
                                    className='w-full bg-gray-800 border border-white/10 rounded-xl px-3 py-2 text-white text-sm focus:outline-none focus:border-cyan-500 transition-colors'
                                >
                                    <option value='acceso'>Acceso</option>
                                    <option value='transporte'>Transporte</option>
                                </select>
                            </div>

                            {/* Longitud / Latitud */}
                            <div className='space-y-1'>
                                <div className='flex items-center justify-between'>
                                    <label className='text-gray-400 text-xs font-semibold uppercase tracking-wide'>
                                        Coordenadas
                                    </label>
                                    <button
                                        type='button'
                                        onClick={() => {
                                            setOpen(false)
                                            onRequestPick()
                                        }}
                                        className='flex items-center gap-1 text-xs text-cyan-400 hover:text-cyan-300 font-semibold transition-colors'
                                    >
                                        <svg
                                            xmlns='http://www.w3.org/2000/svg'
                                            viewBox='0 0 20 20'
                                            fill='currentColor'
                                            className='w-3.5 h-3.5'
                                        >
                                            <path
                                                fillRule='evenodd'
                                                d='M9.69 18.933l.003.001C9.89 19.02 10 19 10 19s.11.02.308-.066l.002-.001.006-.003.018-.008a5.741 5.741 0 00.281-.14c.186-.096.446-.24.757-.433.62-.384 1.445-.966 2.274-1.765C15.302 15.327 17 12.993 17 10a7 7 0 10-14 0c0 2.993 1.698 5.327 3.354 6.985a19.146 19.146 0 002.274 1.765 11.26 11.26 0 00.757.433 5.741 5.741 0 00.281.14l.018.008.006.003zM10 12a2 2 0 100-4 2 2 0 000 4z'
                                                clipRule='evenodd'
                                            />
                                        </svg>
                                        Seleccionar en mapa
                                    </button>
                                </div>
                                <div className='grid grid-cols-2 gap-3'>
                                    <input
                                        required
                                        type='number'
                                        step='any'
                                        name='longitud'
                                        value={form.longitud}
                                        onChange={handleChange}
                                        placeholder='Longitud'
                                        className='w-full bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-white text-sm placeholder-gray-600 focus:outline-none focus:border-cyan-500 transition-colors'
                                    />
                                    <input
                                        required
                                        type='number'
                                        step='any'
                                        name='latitud'
                                        value={form.latitud}
                                        onChange={handleChange}
                                        placeholder='Latitud'
                                        className='w-full bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-white text-sm placeholder-gray-600 focus:outline-none focus:border-cyan-500 transition-colors'
                                    />
                                </div>
                            </div>

                            {/* Altura antena */}
                            <div className='space-y-1'>
                                <label className='text-gray-400 text-xs font-semibold uppercase tracking-wide'>
                                    Altura antena (m)
                                </label>
                                <input
                                    required
                                    type='number'
                                    step='any'
                                    min='0'
                                    name='altura_antena'
                                    value={form.altura_antena}
                                    onChange={handleChange}
                                    className='w-full bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-white text-sm placeholder-gray-600 focus:outline-none focus:border-cyan-500 transition-colors'
                                />
                            </div>

                            {/* Green asociado */}
                            <div className='space-y-1'>
                                <label className='text-gray-400 text-xs font-semibold uppercase tracking-wide'>
                                    Green asociado{' '}
                                    <span className='normal-case text-gray-600'>(opcional)</span>
                                </label>
                                <input
                                    name='green_asociado'
                                    value={form.green_asociado}
                                    onChange={handleChange}
                                    placeholder='ej. transporte'
                                    className='w-full bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-white text-sm placeholder-gray-600 focus:outline-none focus:border-cyan-500 transition-colors'
                                />
                            </div>

                            {state.error && (
                                <p className='text-red-400 text-xs bg-red-400/10 border border-red-400/20 rounded-xl px-3 py-2'>
                                    {state.error}
                                </p>
                            )}

                            {/* Actions */}
                            <div className='flex gap-3 pt-1'>
                                <button
                                    type='button'
                                    onClick={() => setOpen(false)}
                                    className='flex-1 py-2 rounded-xl bg-white/10 text-white text-sm font-semibold hover:bg-white/20 transition-colors'
                                >
                                    Cancelar
                                </button>
                                <button
                                    type='submit'
                                    disabled={isPending}
                                    className='flex-1 py-2 rounded-xl bg-cyan-500 text-gray-950 text-sm font-bold hover:bg-cyan-400 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-lg shadow-cyan-500/30'
                                >
                                    {isPending ? 'Guardando…' : 'Agregar'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </>
    )
}
