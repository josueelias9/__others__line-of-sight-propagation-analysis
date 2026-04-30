'use client'

import type { PuntoData } from './types'

export function Legend({
    puntos,
    redesRelacionCount,
    view3D,
    onToggle3D,
    tipoFiltro,
    onFiltroChange
}: {
    puntos: PuntoData[]
    redesRelacionCount: number
    view3D: boolean
    onToggle3D: () => void
    tipoFiltro: string
    onFiltroChange: (tipo: string) => void
}) {
    const transportes = puntos.filter(p => p.tipo === 'transporte').length
    const accesos = puntos.filter(p => p.tipo === 'acceso').length

    return (
        <div className='absolute top-5 left-5 z-10 w-64 rounded-2xl overflow-hidden shadow-2xl'>
            <div className='bg-gray-900/90 backdrop-blur-xl border border-white/10 px-5 py-4'>
                <span className='text-white font-bold text-base tracking-tight'>
                    Red de Antenas
                </span>
                <p className='text-gray-400 text-xs mt-0.5'>Line of Sight Analysis</p>
            </div>

            <div className='h-px bg-white/10' />

            <div className='bg-gray-900/85 backdrop-blur-xl border-x border-b border-white/10 rounded-b-2xl px-5 py-4 space-y-3'>
                {/* Filtro de tipo */}
                <div className='flex gap-1.5'>
                    {(['', 'transporte', 'acceso'] as const).map(t => (
                        <button
                            key={t || 'todos'}
                            onClick={() => onFiltroChange(t)}
                            className={`flex-1 py-1 px-2 rounded-lg text-xs font-semibold transition-all ${
                                tipoFiltro === t
                                    ? t === 'transporte'
                                        ? 'bg-amber-400 text-gray-950'
                                        : t === 'acceso'
                                          ? 'bg-cyan-400 text-gray-950'
                                          : 'bg-white text-gray-950'
                                    : 'bg-white/10 text-gray-300 hover:bg-white/20'
                            }`}
                        >
                            {t === '' ? 'Todos' : t.charAt(0).toUpperCase() + t.slice(1)}
                        </button>
                    ))}
                </div>

                {/* Transporte */}
                <div className='flex items-center gap-3'>
                    <div className='w-4 h-4 rounded-full bg-amber-400 shadow-lg shadow-amber-400/60 ring-2 ring-amber-300/40 flex-shrink-0' />
                    <div>
                        <p className='text-white text-sm font-semibold leading-none'>Transporte</p>
                        <p className='text-gray-400 text-xs'>
                            {transportes} punto{transportes !== 1 ? 's' : ''}
                        </p>
                    </div>
                </div>

                {/* Acceso */}
                <div className='flex items-center gap-3'>
                    <div className='w-4 h-4 rounded-full bg-cyan-400 shadow-lg shadow-cyan-400/60 ring-2 ring-cyan-300/40 flex-shrink-0' />
                    <div>
                        <p className='text-white text-sm font-semibold leading-none'>Acceso</p>
                        <p className='text-gray-400 text-xs'>
                            {accesos} punto{accesos !== 1 ? 's' : ''}
                        </p>
                    </div>
                </div>

                {/* Relaciones */}
                <div className='flex items-center gap-3'>
                    <div className='w-4 h-1 rounded-full bg-cyan-400 shadow-lg shadow-cyan-400/60 flex-shrink-0' />
                    <div>
                        <p className='text-white text-sm font-semibold leading-none'>Relaciones</p>
                        <p className='text-gray-400 text-xs'>
                            {redesRelacionCount} enlace{redesRelacionCount !== 1 ? 's' : ''}
                        </p>
                    </div>
                </div>

                <div className='pt-2 border-t border-white/10 space-y-2'>
                    <button
                        onClick={onToggle3D}
                        className={`w-full py-2 px-3 rounded-xl text-sm font-semibold transition-all ${
                            view3D
                                ? 'bg-cyan-500 text-gray-950 shadow-lg shadow-cyan-500/40'
                                : 'bg-white/10 text-white hover:bg-white/20'
                        }`}
                    >
                        {view3D ? '← Vista 2D' : 'Vista 3D ↗'}
                    </button>
                    <p className='text-gray-500 text-xs text-center'>
                        {view3D
                            ? 'Clic + arrastrar para rotar y volar'
                            : 'Botón central + arrastrar para rotar'}
                    </p>
                </div>
            </div>
        </div>
    )
}
