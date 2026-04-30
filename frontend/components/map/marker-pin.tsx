"use client";

export function MarkerPin({ tipo, highlighted = false }: { tipo: string; highlighted?: boolean }) {
  const color = tipo === "transporte" ? "#FBBF24" : "#22D3EE"; // amber / cyan
  const shadow = tipo === "transporte" ? "rgba(251,191,36,0.6)" : "rgba(34,211,238,0.6)";
  return (
    <div className="relative flex items-center justify-center">
      {highlighted && (
        <div
          className="absolute w-10 h-10 rounded-full opacity-60 ring-2"
          style={{ backgroundColor: "rgba(167,139,250,0.3)", borderColor: "#A78BFA", boxShadow: "0 0 12px 4px rgba(167,139,250,0.5)" }}
        />
      )}
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
