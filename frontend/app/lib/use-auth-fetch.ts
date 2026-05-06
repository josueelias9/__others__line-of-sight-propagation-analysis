'use client'

import { useCallback } from 'react'

export function useAuthFetch() {
    return useCallback(
        (url: string, options: RequestInit = {}): Promise<Response> => {
            const headers = new Headers(options.headers)
            if (options.body !== undefined && !headers.has('Content-Type')) {
                headers.set('Content-Type', 'application/json')
            }
            return fetch(url, { ...options, headers })
        },
        []
    )
}
