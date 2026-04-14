/**
 * AnomalyGauge — visual indicator for the anomaly score (0..1)
 * Displays Low / Moderado / Alto with color-coded arc gauge
 */
import { useEffect, useRef } from 'react'

const LEVELS = {
  Baixo:    { color: '#22c55e', label: 'Baixo',    cls: 'badge-low' },
  Moderado: { color: '#f59e0b', label: 'Moderado', cls: 'badge-medium' },
  Alto:     { color: '#ef4444', label: 'Alto',      cls: 'badge-high' },
}

export default function AnomalyGauge({ score = 0, level = 'Baixo' }) {
  const canvasRef = useRef(null)
  const info      = LEVELS[level] || LEVELS['Baixo']

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx  = canvas.getContext('2d')
    const cx   = canvas.width  / 2
    const cy   = canvas.height * 0.78
    const R    = cx - 18

    const START = Math.PI        // left (180°)
    const END   = 2 * Math.PI    // right (360°)
    const filled = START + (END - START) * Math.min(score, 1)

    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // Background arc
    ctx.beginPath()
    ctx.arc(cx, cy, R, START, END)
    ctx.strokeStyle = '#1e293b'
    ctx.lineWidth   = 14
    ctx.lineCap     = 'round'
    ctx.stroke()

    // Colored fill arc (Neon effect)
    ctx.beginPath()
    ctx.arc(cx, cy, R, START, filled)
    ctx.strokeStyle = info.color
    ctx.lineWidth   = 14
    ctx.lineCap     = 'round'
    
    // Core glow
    ctx.shadowColor = info.color
    ctx.shadowBlur  = 25
    ctx.stroke()
    
    // Intense inner core (draw again without shadow, thinner)
    ctx.beginPath()
    ctx.arc(cx, cy, R, START, filled)
    ctx.strokeStyle = '#ffffff'
    ctx.lineWidth   = 4
    ctx.lineCap     = 'round'
    ctx.shadowBlur  = 0
    // We only draw this if it's very premium
    ctx.globalAlpha = 0.4
    ctx.stroke()
    ctx.globalAlpha = 1.0

    // Score text in center
    ctx.fillStyle   = '#ffffff'
    ctx.font        = `bold 28px Inter,sans-serif`
    ctx.textAlign   = 'center'
    ctx.shadowColor = 'rgba(255,255,255,0.2)'
    ctx.shadowBlur  = 10
    ctx.fillText(`${(score * 100).toFixed(1)}%`, cx, cy - 8)
    ctx.shadowBlur  = 0

    ctx.fillStyle   = info.color
    ctx.font        = `600 14px Inter,sans-serif`
    ctx.letterSpacing = '1px'
    ctx.fillText(info.label.toUpperCase(), cx, cy + 18)
  }, [score, level])

  return (
    <div className="flex flex-col items-center gap-3">
      <canvas ref={canvasRef} width={180} height={110} aria-label={`Score de anomalia: ${level}`} />
      <span className={`px-4 py-1.5 rounded-full text-sm font-semibold ${info.cls}`}>
        Risco {info.label}
      </span>
    </div>
  )
}
