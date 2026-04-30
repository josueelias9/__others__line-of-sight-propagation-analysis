"use client";

import { useState } from "react";
import type { PuntoData, ArbolResult } from "./types";
import { BACKEND_URL } from "./config";

interface ArbolPanelProps {
  puntos: PuntoData[];
  onResult: (data: ArbolResult) => void;
  onSaved?: () => void;
}

export function ArbolPanel({ puntos, onResult, onSaved }: ArbolPanelProps) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const tipos = Array.from(new Set(puntos.map((p) => p.tipo))).sort();

  const [tipoConectados, setTipoConectados] = useState("");
  const [tipoNoConectados, setTipoNoConectados] = useState("");
  const [distancia, setDistancia] = useState("20");
  const [muestras, setMuestras] = useState("100");
  const [nombreRed, setNombreRed] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${BACKEND_URL}/api/arbol`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tipo_conectados: tipoConectados,
          tipo_no_conectados: tipoNoConectados,
          distancia_maxima: parseFloat(distancia),
          muestras: parseInt(muestras),
          nombre_red: nombreRed,
        }),
      });

      if (!res.ok) {
        const detail = await res.text();
        throw new Error(`HTTP ${res.status}: ${detail}`);
      }

      const data: ArbolResult = await res.json();
      onResult(data);
      if (nombreRed) onSaved?.();
      setOpen(false);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  }

  const canSubmit = tipoConectados && tipoNoConectados && tipoConectados !== tipoNoConectados;

  return (
    <div className="w-72 rounded-2xl overflow-hidden shadow-2xl">
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full bg-gray-900/90 backdrop-blur-xl border border-white/10 px-5 py-4 text-left"
      >
        <span className="text-white font-bold text-base tracking-tight">
          Árbol de Conexión LOS
        </span>
        <p className="text-gray-400 text-xs mt-0.5">
          {open ? "▲ Cerrar" : "▼ Seleccionar tipos y calcular"}
        </p>
      </button>

      {open && (
        <>
          <div className="h-px bg-white/10" />
          <form
            onSubmit={handleSubmit}
            className="bg-gray-900/85 backdrop-blur-xl border-x border-b border-white/10 rounded-b-2xl px-5 py-4 space-y-3"
          >
            <div>
              <label className="text-gray-400 text-xs block mb-0.5">
                Tipo BASE / Conectados
              </label>
              <select
                value={tipoConectados}
                onChange={(e) => setTipoConectados(e.target.value)}
                required
                className="w-full bg-gray-800/60 border border-white/10 rounded-lg px-3 py-1.5 text-white text-sm focus:outline-none focus:ring-1 focus:ring-cyan-400/60"
              >
                <option value="" disabled>Seleccionar tipo…</option>
                {tipos.map((t) => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-gray-400 text-xs block mb-0.5">
                Tipo a CONECTAR
              </label>
              <select
                value={tipoNoConectados}
                onChange={(e) => setTipoNoConectados(e.target.value)}
                required
                className="w-full bg-gray-800/60 border border-white/10 rounded-lg px-3 py-1.5 text-white text-sm focus:outline-none focus:ring-1 focus:ring-cyan-400/60"
              >
                <option value="" disabled>Seleccionar tipo…</option>
                {tipos.map((t) => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
              {tipoConectados && tipoNoConectados && tipoConectados === tipoNoConectados && (
                <p className="text-amber-400 text-xs mt-1">Los tipos deben ser distintos.</p>
              )}
            </div>

            <div>
              <label className="text-gray-400 text-xs block mb-0.5">Distancia máxima (km)</label>
              <input
                type="number"
                step="any"
                min="0.1"
                value={distancia}
                onChange={(e) => setDistancia(e.target.value)}
                required
                className="w-full bg-gray-800/60 border border-white/10 rounded-lg px-3 py-1.5 text-white text-sm focus:outline-none focus:ring-1 focus:ring-cyan-400/60"
              />
            </div>

            <div>
              <label className="text-gray-400 text-xs block mb-0.5">Muestras de elevación</label>
              <input
                type="number"
                min="10"
                value={muestras}
                onChange={(e) => setMuestras(e.target.value)}
                required
                className="w-full bg-gray-800/60 border border-white/10 rounded-lg px-3 py-1.5 text-white text-sm focus:outline-none focus:ring-1 focus:ring-cyan-400/60"
              />
            </div>

            <div>
              <label className="text-gray-400 text-xs block mb-0.5">Nombre de la red (opcional)</label>
              <input
                type="text"
                value={nombreRed}
                onChange={(e) => setNombreRed(e.target.value)}
                placeholder="Ej: Red norte…"
                className="w-full bg-gray-800/60 border border-white/10 rounded-lg px-3 py-1.5 text-white text-sm placeholder-gray-600 focus:outline-none focus:ring-1 focus:ring-cyan-400/60"
              />
            </div>

            {error && (
              <p className="text-red-400 text-xs bg-red-400/10 rounded-lg px-3 py-2">
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={loading || !canSubmit}
              className="w-full mt-1 bg-cyan-500 hover:bg-cyan-400 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold text-sm rounded-xl py-2 transition-colors"
            >
              {loading ? "Calculando…" : "Calcular árbol"}
            </button>
          </form>
        </>
      )}
    </div>
  );
}
