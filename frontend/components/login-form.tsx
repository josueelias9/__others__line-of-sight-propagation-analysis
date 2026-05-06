'use client'

import { useState } from 'react'
import { signIn } from 'next-auth/react'

function AtSymbolIcon({ className }: { className?: string }) {
    return (
        <svg className={className} fill='none' viewBox='0 0 24 24' strokeWidth={1.5} stroke='currentColor'>
            <path strokeLinecap='round' strokeLinejoin='round' d='M16.5 12a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0Zm0 0c0 1.657 1.007 3 2.25 3S21 13.657 21 12a9 9 0 1 0-2.636 6.364M16.5 12V8.25' />
        </svg>
    )
}

function KeyIcon({ className }: { className?: string }) {
    return (
        <svg className={className} fill='none' viewBox='0 0 24 24' strokeWidth={1.5} stroke='currentColor'>
            <path strokeLinecap='round' strokeLinejoin='round' d='M15.75 5.25a3 3 0 0 1 3 3m3 0a6 6 0 0 1-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 0 1 21.75 8.25Z' />
        </svg>
    )
}

function ExclamationCircleIcon({ className }: { className?: string }) {
    return (
        <svg className={className} fill='none' viewBox='0 0 24 24' strokeWidth={1.5} stroke='currentColor'>
            <path strokeLinecap='round' strokeLinejoin='round' d='M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z' />
        </svg>
    )
}

function ArrowRightIcon({ className }: { className?: string }) {
    return (
        <svg className={className} viewBox='0 0 20 20' fill='currentColor'>
            <path fillRule='evenodd' d='M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z' clipRule='evenodd' />
        </svg>
    )
}

export default function LoginForm() {
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
            window.location.replace('/')
        }
    }

    return (
        <form onSubmit={handleSubmit} className='space-y-4'>
            <div className='space-y-1.5'>
                <label
                    htmlFor='email'
                    className='text-gray-400 text-xs font-semibold uppercase tracking-wide'
                >
                    Email
                </label>
                <div className='relative'>
                    <input
                        id='email'
                        type='email'
                        required
                        autoComplete='email'
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                        placeholder='admin@example.com'
                        className='peer w-full bg-white/5 border border-white/10 rounded-xl pl-10 pr-4 py-2.5 text-white text-sm placeholder-gray-600 focus:outline-none focus:border-cyan-500 transition-colors'
                    />
                    <AtSymbolIcon className='pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500 peer-focus:text-cyan-500 transition-colors' />
                </div>
            </div>

            <div className='space-y-1.5'>
                <label
                    htmlFor='password'
                    className='text-gray-400 text-xs font-semibold uppercase tracking-wide'
                >
                    Contraseña
                </label>
                <div className='relative'>
                    <input
                        id='password'
                        type='password'
                        required
                        autoComplete='current-password'
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        placeholder='••••••••'
                        className='peer w-full bg-white/5 border border-white/10 rounded-xl pl-10 pr-4 py-2.5 text-white text-sm placeholder-gray-600 focus:outline-none focus:border-cyan-500 transition-colors'
                    />
                    <KeyIcon className='pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500 peer-focus:text-cyan-500 transition-colors' />
                </div>
            </div>

            <div aria-live='polite' aria-atomic='true' className='min-h-[2rem]'>
                {error && (
                    <div className='flex items-center gap-2 text-red-400 text-sm bg-red-400/10 border border-red-400/20 rounded-xl px-4 py-2.5'>
                        <ExclamationCircleIcon className='h-4 w-4 shrink-0' />
                        <p>{error}</p>
                    </div>
                )}
            </div>

            <button
                type='submit'
                disabled={loading}
                aria-disabled={loading}
                className='w-full flex items-center justify-center gap-2 bg-cyan-500 hover:bg-cyan-400 disabled:opacity-50 disabled:cursor-not-allowed text-gray-950 font-bold text-sm rounded-xl py-2.5 transition-colors shadow-lg shadow-cyan-500/30'
            >
                {loading ? 'Ingresando…' : 'Ingresar'}
                {!loading && <ArrowRightIcon className='h-4 w-4' />}
            </button>
        </form>
    )
}
