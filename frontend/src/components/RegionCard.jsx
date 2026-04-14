/**
 * RegionCard — displays a single affected brain region with z-score and deviation badge
 */

const DEVIATION_STYLE = {
  alta:     { cls: 'badge-high',   label: 'Desvio Alto'    },
  moderada: { cls: 'badge-medium', label: 'Desvio Moderado' },
}

export default function RegionCard({ region, index }) {
  const dev   = DEVIATION_STYLE[region.deviation] || DEVIATION_STYLE['moderada']
  const zAbs  = Math.abs(region.z_score || 0)
  // Bar width: z-score normalized to ~4 max
  const barW  = Math.min((zAbs / 4) * 100, 100)

  return (
    <div className="relative overflow-hidden glass rounded-xl p-5 space-y-3 transition-all duration-300 border border-white/5 bg-syn-surface/40 hover:bg-syn-surface/60 hover:shadow-[0_0_20px_rgba(168,85,247,0.15)] hover:border-syn-purple/50 hover:-translate-y-1">
      {/* Subtle top glare */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white/10 to-transparent"></div>
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-2 min-w-0">
          <span className="flex-shrink-0 w-6 h-6 rounded-full bg-syn-border flex items-center
                           justify-center text-xs text-syn-muted font-mono">
            {index + 1}
          </span>
          <p className="font-semibold text-syn-text text-sm truncate">{region.name}</p>
        </div>
        <span className={`text-xs px-3 py-1 rounded-full flex-shrink-0 font-bold border border-current ${dev.cls}`}>
          {dev.label}
        </span>
      </div>

      {/* Z-score bar */}
      <div className="space-y-1">
        <div className="flex justify-between text-xs text-syn-muted">
          <span>Z-score</span>
          <span className="font-mono text-syn-blue">{region.z_score?.toFixed(3)}</span>
        </div>
        <div className="h-1.5 bg-syn-border rounded-full overflow-hidden">
          <div
            className="h-full rounded-full transition-all duration-700"
            style={{
              width: `${barW}%`,
              background: zAbs > 2.8
                ? 'linear-gradient(90deg,#f59e0b,#ef4444)'
                : 'linear-gradient(90deg,#4f8ef7,#a855f7)',
            }}
          />
        </div>
      </div>

      <div className="flex gap-3 text-xs text-syn-muted">
        {region.laterality && (
          <span className="flex items-center gap-1">
            <div className="w-1.5 h-1.5 rounded-full bg-syn-purple"></div>
            {region.laterality.charAt(0).toUpperCase() + region.laterality.slice(1)}
          </span>
        )}
      </div>
    </div>
  )
}
