'use client'

export default function Error({
    error,
    unstable_retry
}: {
    error: Error & { digest?: string }
    unstable_retry: () => void
}) {
    return (
        <div className='min-h-screen bg-gray-950 flex items-center justify-center px-4'>
            <div className='w-full max-w-sm text-center'>
                <div className='bg-gray-900 border border-white/10 rounded-2xl shadow-2xl p-8 space-y-4'>
                    <h2 className='text-white font-bold text-xl tracking-tight'>
                        Esta tomando tiempo al backend en responder...
                    </h2>
                    <p className='text-gray-400 text-sm'>
                        {error.message || 'Ocurrió un error inesperado.'}
                    </p>
                    {error.digest && (
                        <p className='text-gray-600 text-xs font-mono'>ID: {error.digest}</p>
                    )}
                    <button
                        onClick={() => unstable_retry()}
                        className='w-full bg-white/10 hover:bg-white/15 text-white text-sm font-medium rounded-xl px-4 py-2.5 transition-colors'
                    >
                        Intentar de nuevo
                    </button>
                    <h1 className='text-white font-bold text-xl tracking-tight'>
                        Si continua, presiona F5.
                    </h1>
                </div>
            </div>
        </div>
    )
}
