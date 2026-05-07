'use server'

import { fetchFromBackend } from '@/app/lib/backend'
import type { PuntoData, RedData, MultipoligonoData } from '@/app/lib/types'

export async function fetchPuntos(tipo?: string): Promise<PuntoData[]> {
    const path = tipo ? `/api/puntos?tipo=${encodeURIComponent(tipo)}` : '/api/puntos'
    return fetchFromBackend<PuntoData[]>(path)
}

export async function fetchRedes(): Promise<RedData[]> {
    return fetchFromBackend<RedData[]>('/api/redes')
}

export async function fetchSavedCoberturas(): Promise<MultipoligonoData[]> {
    return fetchFromBackend<MultipoligonoData[]>('/api/cobertura')
}
