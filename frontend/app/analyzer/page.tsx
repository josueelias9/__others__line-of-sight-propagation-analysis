import MapView from '@/components/map-view'
import { fetchPuntos, fetchRedes, fetchSavedCoberturas } from '@/app/lib/data'

export default async function AnalyzerPage() {
    const [puntos, redes, coberturas] = await Promise.all([
        fetchPuntos(),
        fetchRedes(),
        fetchSavedCoberturas()
    ])

    return (
        <main className='w-screen h-screen overflow-hidden'>
            <MapView initialPuntos={puntos} initialRedes={redes} initialCoberturas={coberturas} />
        </main>
    )
}
