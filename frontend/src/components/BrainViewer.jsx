/**
 * BrainViewer — displays the generated brain map images in a responsive grid
 * Shows: glass brain, axial, coronal, sagittal, connectivity matrix, z-score chart
 */

const IMAGE_LABELS = {
  glass_brain:  { title: 'Glass Brain',              subtitle: 'Visão global das redes neurais' },
  axial:        { title: 'Corte Axial',              subtitle: 'Vista transversal' },
  coronal:      { title: 'Corte Coronal',            subtitle: 'Vista frontal' },
  sagittal:     { title: 'Corte Sagital',            subtitle: 'Vista lateral' },
  brain_map:    { title: 'Mapa de Ativação',         subtitle: 'Regiões com desvio elevado' },
  connectivity: { title: 'Conectividade Funcional',  subtitle: 'Correlações entre regiões' },
  zscore_chart: { title: 'Z-Scores por Região',      subtitle: 'Desvio relativo à linha de base' },
}

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export default function BrainViewer({ images = {} }) {
  const entries = Object.entries(images).filter(([, url]) => url)

  if (!entries.length) {
    return (
      <div className="glass p-8 text-center text-syn-muted">
        <p>Nenhuma imagem disponível</p>
      </div>
    )
  }

  // Show glass brain or brain_map full-width first
  const primaryKey  = entries.find(([k]) => k === 'glass_brain' || k === 'brain_map')
  const secondaries = entries.filter(([k]) => k !== primaryKey?.[0])

  return (
    <div className="space-y-4">
      {primaryKey && (
        <BrainImage
          imgKey={primaryKey[0]}
          url={primaryKey[1]}
          fullWidth
        />
      )}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {secondaries.map(([key, url]) => (
          <BrainImage key={key} imgKey={key} url={url} />
        ))}
      </div>
    </div>
  )
}

function BrainImage({ imgKey, url, fullWidth = false }) {
  const meta = IMAGE_LABELS[imgKey] || { title: imgKey, subtitle: '' }
  const fullUrl = url.startsWith('http') ? url : `${BASE_URL}${url}`

  return (
    <div className={`glass rounded-2xl overflow-hidden group border border-white/5 shadow-lg transition-all duration-500 hover:shadow-[0_8px_30px_rgba(79,142,247,0.15)] hover:border-syn-blue/30 ${fullWidth ? 'col-span-full' : ''}`}>
      <div className="p-4 border-b border-white/5 bg-black/20 flex items-center gap-3 backdrop-blur-md">
        <div className="w-2.5 h-2.5 rounded-full bg-syn-blue animate-pulse shadow-[0_0_8px_rgba(79,142,247,0.8)]" />
        <div>
          <p className="text-sm font-semibold text-syn-text">{meta.title}</p>
          <p className="text-xs text-syn-muted">{meta.subtitle}</p>
        </div>
      </div>
      <div className="relative overflow-hidden bg-syn-bg">
        <img
          src={fullUrl}
          alt={meta.title}
          className="w-full object-contain transition-transform duration-500 group-hover:scale-105"
          style={{ maxHeight: fullWidth ? '320px' : '220px' }}
          onError={e => { e.target.style.display = 'none' }}
        />
        <div className="absolute inset-0 pointer-events-none
                        bg-gradient-to-t from-syn-surface/30 to-transparent" />
      </div>
    </div>
  )
}
