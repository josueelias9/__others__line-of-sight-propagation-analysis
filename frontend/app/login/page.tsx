'use client'

import LoginForm from '@/components/login-form'

export default function LoginPage() {
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
                    <LoginForm />
                </div>
            </div>
        </div>
    )
}
