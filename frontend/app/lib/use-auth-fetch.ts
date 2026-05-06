'use client'

import { useSession } from 'next-auth/react'
import { useCallback } from 'react'

export function useAuthFetch() {
    const { data: session } = useSession()

    return useCallback(
        (url: string, options: RequestInit = {}): Promise<Response> => {
            const headers = new Headers(options.headers)
            if (options.body !== undefined && !headers.has('Content-Type')) {
                headers.set('Content-Type', 'application/json')
            }
            if (session?.accessToken) {
                headers.set('Authorization', `Bearer ${session.accessToken}`)
            }
            return fetch(url, { ...options, headers })
        },
        [session?.accessToken]
    )
}
