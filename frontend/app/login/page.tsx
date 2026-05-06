'use client'

import { useState } from 'react'
import { signIn } from 'next-auth/react'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
    const router = useRouter()
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState<string | null>(null)
    const [loading, setLoading] = useState(false)

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault()
        setLoading(true)
        setError(null)

        const result = await signIn('credentials', {
            email,
            password,
            redirect: false,
        })

        setLoading(false)

        if (result?.error) {
            setError('Email o contraseña incorrectos')
        } else {
            router.push('/')
            router.refresh()
        }
    }

    return (
        <div className='min-h-screen bg-gray-950 flex items-center justify-center px-4'>
            <div className='w-full max-w-sm'>
                {/* Logo / title */}
                <div className='text-center mb-8'>
                    <h1 className='text-2xl font-bold text-white tracking-tight'>
                        Análisis LOS
                    </h1>
                    <p className='text-gray-500 text-sm mt-1'>
                        Line-of-Sight Propagation Analysis
                    </p>
                </div>

                {/* Card */}
                <div className='bg-gray-900 border border-white/10 rounded-2xl shadow-2xl p-8'>
                    <h2 className='text-white font-semibold text-lg mb-6'>Iniciar sesión</h2>

                    <form onSubmit={handleSubmit} className='space-y-4'>
                        <div className='space-y-1.5'>
                            <label className='text-gray-400 text-xs font-semibold uppercase tracking-wide'>
                                Email
                            </label>
                            <input
                                type='email'
                                required
                                autoComplete='email'
                                value={email}
                                onChange={e => setEmail(e.target.value)}
                                placeholder='admin@example.com'
                                className='w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-white text-sm placeholder-gray-600 focus:outline-none focus:border-cyan-500 transition-colors'
                            />
                        </div>

                        <div className='space-y-1.5'>
                            <label className='text-gray-400 text-xs font-semibold uppercase tracking-wide'>
                                Contraseña
                            </label>
                            <input
                                type='password'
                                required
                                autoComplete='current-password'
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                                placeholder='••••••••'
                                className='w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-white text-sm placeholder-gray-600 focus:outline-none focus:border-cyan-500 transition-colors'
                            />
                        </div>

                        {error && (
                            <p className='text-red-400 text-sm bg-red-400/10 border border-red-400/20 rounded-xl px-4 py-2.5'>
                                {error}
                            </p>
                        )}

                        <button
                            type='submit'
                            disabled={loading}
                            className='w-full mt-2 bg-cyan-500 hover:bg-cyan-400 disabled:opacity-50 disabled:cursor-not-allowed text-gray-950 font-bold text-sm rounded-xl py-2.5 transition-colors shadow-lg shadow-cyan-500/30'
                        >
                            {loading ? 'Ingresando…' : 'Ingresar'}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    )
}
