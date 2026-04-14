/**
 * ProgressBar — animated 3-phase upload/processing progress bar
 * Shows phase label, percentage, and an animated fill with glow effect
 */

const PHASES = [
  { id: 1, label: 'Carregando exame...',         min: 0,  max: 33  },
  { id: 2, label: 'Analisando redes neurais...', min: 33, max: 66  },
  { id: 3, label: 'Gerando pré-relatório...',    min: 66, max: 100 },
]

export default function ProgressBar({ progress = 0, message = '' }) {
  const currentPhase = PHASES.find(p => progress <= p.max) || PHASES[2]

  return (
    <div className="w-full space-y-4">
      {/* Phase steps */}
      <div className="flex items-center gap-3">
        {PHASES.map((phase, idx) => {
          const done    = progress > phase.max
          const active  = currentPhase.id === phase.id
          return (
            <div key={phase.id} className="flex items-center gap-2 flex-1">
              <div className={`
                w-7 h-7 rounded-full flex items-center justify-center
                text-xs font-bold transition-all duration-500 shrink-0
                ${done   ? 'bg-syn-blue text-white shadow-[0_0_12px_rgba(79,142,247,0.6)]' : ''}
                ${active ? 'bg-gradient-to-br from-syn-blue to-syn-purple text-white animate-pulse-slow' : ''}
                ${!done && !active ? 'bg-syn-border text-syn-muted' : ''}
              `}>
                {done ? '✓' : phase.id}
              </div>
              <span className={`text-xs font-medium truncate transition-colors duration-300
                ${active ? 'text-syn-text' : done ? 'text-syn-blue' : 'text-syn-muted'}`}>
                {phase.label}
              </span>
              {idx < PHASES.length - 1 && (
                <div className={`h-px flex-1 transition-all duration-700
                  ${done ? 'bg-syn-blue' : 'bg-syn-border'}`} />
              )}
            </div>
          )
        })}
      </div>

      {/* Track */}
      <div className="progress-track">
        <div className="progress-fill" style={{ width: `${progress}%` }} />
      </div>

      {/* Status text + percentage */}
      <div className="flex justify-between items-center">
        <p className="text-syn-muted text-sm animate-pulse">
          {message || currentPhase.label}
        </p>
        <span className="text-syn-blue font-mono text-sm font-semibold">
          {Math.round(progress)}%
        </span>
      </div>
    </div>
  )
}
