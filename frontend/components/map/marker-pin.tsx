"use client";

export function MarkerPin({ tipo }: { tipo: string }) {
  const color = tipo === "transporte" ? "#FBBF24" : "#22D3EE"; // amber / cyan
  const shadow = tipo === "transporte" ? "rgba(251,191,36,0.6)" : "rgba(34,211,238,0.6)";
  return (
    <div className="relative flex items-center justify-center">
      <div
        className="absolute w-7 h-7 rounded-full animate-ping opacity-40"
        style={{ background: color }}
      />
      <div
        className="relative w-4 h-4 rounded-full ring-2 ring-white"
        style={{ background: color, boxShadow: `0 0 8px 2px ${shadow}` }}
      />
    </div>
  );
}
