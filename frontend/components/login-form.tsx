'use client'

import { useFormState as useActionState, useFormStatus } from 'react-dom'
import { authenticate } from '@/app/lib/actions'

export default function LoginForm() {
    const [errorMessage, formAction, isPending] = useActionState(
        authenticate,
        undefined,
    )

    return (
        <form action={formAction} className='space-y-4'>
            <div>
                <label
                    htmlFor='email'
                    className='block text-xs font-medium text-gray-400 mb-1'
                >
                    Correo electrónico
                </label>
                <input
                    id='email'
                    type='email'
                    name='email'
                    placeholder='usuario@ejemplo.com'
                    required
                    className='w-full rounded-xl bg-gray-800 border border-white/10 text-white placeholder-gray-600 text-sm px-4 py-2.5 outline-none focus:ring-2 focus:ring-blue-500 transition'
                />
            </div>
            <div>
                <label
                    htmlFor='password'
                    className='block text-xs font-medium text-gray-400 mb-1'
                >
                    Contraseña
                </label>
                <input
                    id='password'
                    type='password'
                    name='password'
                    placeholder='••••••••'
                    required
                    minLength={6}
                    className='w-full rounded-xl bg-gray-800 border border-white/10 text-white placeholder-gray-600 text-sm px-4 py-2.5 outline-none focus:ring-2 focus:ring-blue-500 transition'
                />
            </div>
            <button
                type='submit'
                aria-disabled={isPending}
                className='w-full bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-semibold text-sm rounded-xl py-2.5 transition-colors'
            >
                {isPending ? 'Ingresando…' : 'Ingresar'}
            </button>
            {errorMessage && (
                <p className='text-red-400 text-xs text-center' aria-live='polite'>
                    {errorMessage}
                </p>
            )}
        </form>
    )
}

