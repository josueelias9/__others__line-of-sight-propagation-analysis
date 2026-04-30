'use client'

import React from 'react'

interface PanelFrameProps {
    title: string
    closedLabel: string
    open: boolean
    onToggle: () => void
    children: React.ReactNode
    contentClassName?: string
    as?: 'div' | 'form'
    onSubmit?: React.FormEventHandler<HTMLFormElement>
}

const BASE =
    'bg-gray-900/85 backdrop-blur-xl border-x border-b border-white/10 rounded-b-2xl px-5 py-4 space-y-3'

export function PanelFrame({
    title,
    closedLabel,
    open,
    onToggle,
    children,
    contentClassName,
    as = 'div',
    onSubmit
}: PanelFrameProps) {
    const cls = contentClassName ? `${BASE} ${contentClassName}` : BASE

    return (
        <div className='w-72 rounded-2xl overflow-hidden shadow-2xl'>
            <button
                onClick={onToggle}
                className='w-full bg-gray-900/90 backdrop-blur-xl border border-white/10 px-5 py-4 text-left'
            >
                <span className='text-white font-bold text-base tracking-tight'>{title}</span>
                <p className='text-gray-400 text-xs mt-0.5'>
                    {open ? '▲ Cerrar' : `▼ ${closedLabel}`}
                </p>
            </button>

            {open && (
                <>
                    <div className='h-px bg-white/10' />
                    {as === 'form' ? (
                        <form className={cls} onSubmit={onSubmit}>
                            {children}
                        </form>
                    ) : (
                        <div className={cls}>{children}</div>
                    )}
                </>
            )}
        </div>
    )
}
