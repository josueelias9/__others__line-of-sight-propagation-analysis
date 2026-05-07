import { auth } from '@/auth'

const BASE =
    process.env.BACKEND_API_URL ?? process.env.NEXT_PUBLIC_BACKEND_URL ?? 'http://localhost:8000'

// Includes the user's Google id_token as Bearer on every request
async function backendFetch(path: string, init?: RequestInit) {
    const session = await auth()
    return fetch(`${BASE}${path}`, {
        ...init,
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${session?.accessToken ?? ''}`,
            ...(init?.headers ?? {})
        }
    })
}

// ─── Read helpers (use from Server Components) ────────────────────────────────

export async function fetchFromBackend<T>(path: string): Promise<T> {
    const res = await backendFetch(path)
    if (!res.ok) throw new Error(`Backend error: ${res.status} ${path}`)
    return res.json() as Promise<T>
}

// ─── Mutation helpers (use from Server Actions) ───────────────────────────────

export async function postToBackend<T>(path: string, body: unknown): Promise<T> {
    const res = await backendFetch(path, {
        method: 'POST',
        body: JSON.stringify(body)
    })
    if (!res.ok) throw new Error(`Backend error: ${res.status} ${path}`)
    return res.json() as Promise<T>
}

export async function putToBackend<T>(path: string, body: unknown): Promise<T> {
    const res = await backendFetch(path, {
        method: 'PUT',
        body: JSON.stringify(body)
    })
    if (!res.ok) throw new Error(`Backend error: ${res.status} ${path}`)
    return res.json() as Promise<T>
}

export async function deleteFromBackend(path: string): Promise<void> {
    const res = await backendFetch(path, { method: 'DELETE' })
    if (!res.ok) throw new Error(`Backend error: ${res.status} ${path}`)
}
