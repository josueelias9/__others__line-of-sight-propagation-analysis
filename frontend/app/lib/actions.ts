'use server'

import { signIn, signOut } from '@/auth'
import { AuthError } from 'next-auth'
import { z } from 'zod'
import { postToBackend, deleteFromBackend } from '@/app/lib/backend'
import type { PuntoData, CoberturaViewModel, ArbolResult } from '@/app/lib/types'

// ─── Auth ──────────────────────────────────────────────────────────────────────

export type State = {
    errors?: {
        email?: string[]
        password?: string[]
    }
    message?: string | null
}

export async function authenticate(prevState: string | undefined, formData: FormData) {
    try {
        await signIn('credentials', formData)
    } catch (error) {
        if (error instanceof AuthError) {
            switch (error.type) {
                case 'CredentialsSignin':
                    return 'Credenciales inválidas.'
                default:
                    return 'Algo salió mal.'
            }
        }
        throw error
    }
}

export async function signOutAction() {
    await signOut({ redirectTo: '/login' })
}

// ─── Cobertura ─────────────────────────────────────────────────────────────────

export type CoberturaState = {
    result: CoberturaViewModel | null
    error: string | null
}

const CoberturaSchema = z.object({
    ubigeo: z.coerce.number().int(),
    numero_de_ldv: z.coerce.number().int().gt(0),
    muestras: z.coerce.number().int().gt(0),
    distancia_km: z.coerce.number().gt(0),
    altura_torre_fantasma: z.coerce.number().gt(0)
})

export async function calcularCobertura(
    prevState: CoberturaState,
    formData: FormData
): Promise<CoberturaState> {
    const validated = CoberturaSchema.safeParse({
        ubigeo: formData.get('ubigeo'),
        numero_de_ldv: formData.get('numero_de_ldv'),
        muestras: formData.get('muestras'),
        distancia_km: formData.get('distancia_km'),
        altura_torre_fantasma: formData.get('altura_torre_fantasma')
    })
    if (!validated.success) {
        return { result: null, error: 'Campos inválidos.' }
    }
    try {
        const result = await postToBackend<CoberturaViewModel>('/api/cobertura', validated.data)
        return { result, error: null }
    } catch {
        return { result: null, error: 'Error al calcular cobertura.' }
    }
}

// ─── Árbol de conexión ─────────────────────────────────────────────────────────

export type ArbolState = {
    result: ArbolResult | null
    error: string | null
}

const ArbolSchema = z.object({
    tipo_conectados: z.string().min(1),
    tipo_no_conectados: z.string().min(1),
    distancia_maxima: z.coerce.number().gt(0),
    muestras: z.coerce.number().int().gt(0),
    nombre_red: z.string().optional()
})

export async function calcularArbol(
    prevState: ArbolState,
    formData: FormData
): Promise<ArbolState> {
    const validated = ArbolSchema.safeParse({
        tipo_conectados: formData.get('tipo_conectados'),
        tipo_no_conectados: formData.get('tipo_no_conectados'),
        distancia_maxima: formData.get('distancia_maxima'),
        muestras: formData.get('muestras'),
        nombre_red: formData.get('nombre_red')
    })
    if (!validated.success) {
        return { result: null, error: 'Campos inválidos.' }
    }
    try {
        const result = await postToBackend<ArbolResult>('/api/redes', validated.data)
        return { result, error: null }
    } catch {
        return { result: null, error: 'Error al calcular árbol de conexión.' }
    }
}

// ─── Puntos ────────────────────────────────────────────────────────────────────

export type PuntoState = {
    result: PuntoData | null
    error: string | null
}

const PuntoSchema = z.object({
    nombre: z.string().min(1),
    longitud: z.coerce.number(),
    latitud: z.coerce.number(),
    altura_antena: z.coerce.number().gt(0),
    tipo: z.string().min(1),
    green_asociado: z.string()
})

export async function agregarPunto(prevState: PuntoState, formData: FormData): Promise<PuntoState> {
    const validated = PuntoSchema.safeParse({
        nombre: formData.get('nombre'),
        longitud: formData.get('longitud'),
        latitud: formData.get('latitud'),
        altura_antena: formData.get('altura_antena'),
        tipo: formData.get('tipo'),
        green_asociado: formData.get('green_asociado')
    })
    if (!validated.success) {
        return { result: null, error: 'Campos inválidos.' }
    }
    try {
        const result = await postToBackend<PuntoData>('/api/puntos', validated.data)
        return { result, error: null }
    } catch {
        return { result: null, error: 'Error al agregar punto.' }
    }
}

// ─── Delete ────────────────────────────────────────────────────────────────────

export async function eliminarRed(id: number): Promise<void> {
    await deleteFromBackend(`/api/redes/${id}`)
}

export async function eliminarCobertura(id: number): Promise<void> {
    await deleteFromBackend(`/api/cobertura/${id}`)
}
