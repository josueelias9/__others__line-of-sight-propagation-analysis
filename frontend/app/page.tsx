import Link from 'next/link'

export default function Home() {
    return (
        <main className='min-h-screen bg-gray-950 text-white'>
            {/* Nav */}
            <nav className='flex items-center justify-between px-8 py-5 border-b border-gray-800'>
                <div className='flex items-center gap-3'>
                    <div className='w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-400 to-cyan-500 flex items-center justify-center'>
                        <svg
                            className='w-5 h-5 text-gray-950'
                            fill='none'
                            stroke='currentColor'
                            strokeWidth={2.5}
                            viewBox='0 0 24 24'
                        >
                            <path
                                strokeLinecap='round'
                                strokeLinejoin='round'
                                d='M9 6.75V15m6-6v8.25m.503 3.498 4.875-2.437c.381-.19.622-.58.622-1.006V4.82c0-.836-.88-1.38-1.628-1.006l-3.869 1.934c-.317.159-.69.159-1.006 0L9.503 3.252a1.125 1.125 0 0 0-1.006 0L3.622 5.689C3.24 5.88 3 6.27 3 6.695V19.18c0 .836.88 1.38 1.628 1.006l3.869-1.934c.317-.159.69-.159 1.006 0l4.994 2.497c.317.158.69.158 1.006 0Z'
                            />
                        </svg>
                    </div>
                    <span className='font-bold text-lg tracking-tight'>RedAnalyzer</span>
                </div>
                <div className='flex items-center gap-4'>
                    <Link
                        href='/login'
                        className='text-sm text-gray-400 hover:text-white transition-colors'
                    >
                        Iniciar sesión
                    </Link>
                    <Link
                        href='/analyzer'
                        className='text-sm px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-gray-950 font-semibold transition-colors'
                    >
                        Abrir Analizador
                    </Link>
                </div>
            </nav>

            {/* Hero */}
            <section className='relative overflow-hidden px-8 pt-24 pb-32 text-center'>
                {/* Background glow */}
                <div className='absolute inset-0 pointer-events-none'>
                    <div className='absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] bg-emerald-500/10 rounded-full blur-3xl' />
                    <div className='absolute top-1/2 left-1/4 -translate-y-1/2 w-[300px] h-[300px] bg-cyan-500/10 rounded-full blur-3xl' />
                </div>

                <div className='relative max-w-4xl mx-auto'>
                    <span className='inline-block mb-6 px-3 py-1 text-xs font-semibold uppercase tracking-widest text-emerald-400 bg-emerald-400/10 border border-emerald-400/20 rounded-full'>
                        Análisis de Redes Telecomunicaciones
                    </span>
                    <h1 className='text-5xl sm:text-6xl font-extrabold leading-tight mb-6 bg-gradient-to-b from-white to-gray-400 bg-clip-text text-transparent'>
                        Visualiza y analiza tu red en
                        <br />
                        <span className='bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent'>
                            tiempo real
                        </span>
                    </h1>
                    <p className='text-lg text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed'>
                        Plataforma 3D interactiva para el análisis de cobertura, gestión de nodos y
                        visualización de redes de telecomunicaciones en la región de Chachapoyas,
                        Perú.
                    </p>
                    <div className='flex flex-col sm:flex-row items-center justify-center gap-4'>
                        <Link
                            href='/analyzer'
                            className='w-full sm:w-auto px-8 py-3.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-gray-950 font-bold text-base transition-all shadow-lg shadow-emerald-500/25 hover:shadow-emerald-400/40'
                        >
                            Ir al Analizador →
                        </Link>
                        <Link
                            href='/login'
                            className='w-full sm:w-auto px-8 py-3.5 rounded-xl border border-gray-700 hover:border-gray-500 text-gray-300 hover:text-white font-semibold text-base transition-colors'
                        >
                            Iniciar sesión
                        </Link>
                    </div>
                </div>
            </section>

            {/* Features */}
            <section className='px-8 py-20 max-w-6xl mx-auto'>
                <h2 className='text-center text-3xl font-bold mb-3 text-white'>
                    Características principales
                </h2>
                <p className='text-center text-gray-500 mb-14 text-sm'>
                    Todo lo que necesitas para analizar y gestionar tu infraestructura de red.
                </p>
                <div className='grid sm:grid-cols-2 lg:grid-cols-3 gap-6'>
                    {[
                        {
                            icon: (
                                <svg
                                    className='w-6 h-6'
                                    fill='none'
                                    stroke='currentColor'
                                    strokeWidth={1.8}
                                    viewBox='0 0 24 24'
                                >
                                    <path
                                        strokeLinecap='round'
                                        strokeLinejoin='round'
                                        d='M12 21a9.004 9.004 0 0 0 8.716-6.747M12 21a9.004 9.004 0 0 1-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 0 1 7.843 4.582M12 3a8.997 8.997 0 0 0-7.843 4.582m15.686 0A11.953 11.953 0 0 1 12 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0 1 21 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0 1 12 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 0 1 3 12c0-1.605.42-3.113 1.157-4.418'
                                    />
                                </svg>
                            ),
                            title: 'Mapa 3D Interactivo',
                            desc: 'Visualiza la topografía y los nodos de red en un entorno tridimensional con rotación, inclinación y zoom.',
                            color: 'emerald'
                        },
                        {
                            icon: (
                                <svg
                                    className='w-6 h-6'
                                    fill='none'
                                    stroke='currentColor'
                                    strokeWidth={1.8}
                                    viewBox='0 0 24 24'
                                >
                                    <path
                                        strokeLinecap='round'
                                        strokeLinejoin='round'
                                        d='M7.5 14.25v2.25m3-4.5v4.5m3-6.75v6.75m3-9v9M6 20.25h12A2.25 2.25 0 0 0 20.25 18V6A2.25 2.25 0 0 0 18 3.75H6A2.25 2.25 0 0 0 3.75 6v12A2.25 2.25 0 0 0 6 20.25Z'
                                    />
                                </svg>
                            ),
                            title: 'Análisis de Cobertura',
                            desc: 'Calcula y visualiza zonas de cobertura radial con superposición de polígonos para cada nodo de la red.',
                            color: 'cyan'
                        },
                        {
                            icon: (
                                <svg
                                    className='w-6 h-6'
                                    fill='none'
                                    stroke='currentColor'
                                    strokeWidth={1.8}
                                    viewBox='0 0 24 24'
                                >
                                    <path
                                        strokeLinecap='round'
                                        strokeLinejoin='round'
                                        d='M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244'
                                    />
                                </svg>
                            ),
                            title: 'Gestión de Redes',
                            desc: 'Define y visualiza las relaciones entre nodos, construye árboles de red y analiza la conectividad.',
                            color: 'violet'
                        },
                        {
                            icon: (
                                <svg
                                    className='w-6 h-6'
                                    fill='none'
                                    stroke='currentColor'
                                    strokeWidth={1.8}
                                    viewBox='0 0 24 24'
                                >
                                    <path
                                        strokeLinecap='round'
                                        strokeLinejoin='round'
                                        d='M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z'
                                    />
                                    <path
                                        strokeLinecap='round'
                                        strokeLinejoin='round'
                                        d='M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z'
                                    />
                                </svg>
                            ),
                            title: 'Puntos de Red',
                            desc: 'Agrega, filtra y gestiona los puntos de la red con información detallada: tipo, altitud y conectividad.',
                            color: 'amber'
                        },
                        {
                            icon: (
                                <svg
                                    className='w-6 h-6'
                                    fill='none'
                                    stroke='currentColor'
                                    strokeWidth={1.8}
                                    viewBox='0 0 24 24'
                                >
                                    <path
                                        strokeLinecap='round'
                                        strokeLinejoin='round'
                                        d='M2.25 7.125C2.25 6.504 2.754 6 3.375 6h6c.621 0 1.125.504 1.125 1.125v3.75c0 .621-.504 1.125-1.125 1.125h-6a1.125 1.125 0 0 1-1.125-1.125v-3.75ZM14.25 8.625c0-.621.504-1.125 1.125-1.125h5.25c.621 0 1.125.504 1.125 1.125v8.25c0 .621-.504 1.125-1.125 1.125h-5.25a1.125 1.125 0 0 1-1.125-1.125v-8.25ZM3.75 16.125c0-.621.504-1.125 1.125-1.125h5.25c.621 0 1.125.504 1.125 1.125v2.25c0 .621-.504 1.125-1.125 1.125h-5.25a1.125 1.125 0 0 1-1.125-1.125v-2.25Z'
                                    />
                                </svg>
                            ),
                            title: 'Paneles Informativos',
                            desc: 'Accede a paneles detallados con información de coberturas, árboles de red y estadísticas guardadas.',
                            color: 'rose'
                        },
                        {
                            icon: (
                                <svg
                                    className='w-6 h-6'
                                    fill='none'
                                    stroke='currentColor'
                                    strokeWidth={1.8}
                                    viewBox='0 0 24 24'
                                >
                                    <path
                                        strokeLinecap='round'
                                        strokeLinejoin='round'
                                        d='M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456Z'
                                    />
                                </svg>
                            ),
                            title: 'Árbol de Red',
                            desc: 'Genera automáticamente el árbol de expansión de la red y visualiza las rutas óptimas entre nodos.',
                            color: 'sky'
                        }
                    ].map(({ icon, title, desc, color }) => (
                        <div
                            key={title}
                            className='group p-6 rounded-2xl bg-gray-900 border border-gray-800 hover:border-gray-700 transition-all hover:-translate-y-0.5'
                        >
                            <div
                                className={`w-11 h-11 rounded-xl mb-5 flex items-center justify-center bg-${color}-500/10 text-${color}-400`}
                            >
                                {icon}
                            </div>
                            <h3 className='font-semibold text-white mb-2'>{title}</h3>
                            <p className='text-sm text-gray-500 leading-relaxed'>{desc}</p>
                        </div>
                    ))}
                </div>
            </section>

            {/* CTA */}
            <section className='px-8 py-20 text-center'>
                <div className='max-w-2xl mx-auto bg-gradient-to-br from-gray-900 to-gray-900/60 border border-gray-800 rounded-3xl p-12'>
                    <h2 className='text-3xl font-bold mb-4 text-white'>¿Listo para comenzar?</h2>
                    <p className='text-gray-400 mb-8'>
                        Inicia sesión para acceder al analizador completo con todas las
                        funcionalidades.
                    </p>
                    <Link
                        href='/login'
                        className='inline-block px-10 py-3.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-gray-950 font-bold text-base transition-all shadow-lg shadow-emerald-500/25 hover:shadow-emerald-400/40'
                    >
                        Iniciar sesión →
                    </Link>
                </div>
            </section>

            {/* Footer */}
            <footer className='border-t border-gray-800 px-8 py-8 text-center text-xs text-gray-600'>
                RedAnalyzer · Región Chachapoyas, Perú · {new Date().getFullYear()}
            </footer>
        </main>
    )
}
