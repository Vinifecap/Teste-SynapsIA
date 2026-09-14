import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import axios from 'axios'
import BrainViewer from '../components/BrainViewer'
import AnomalyGauge from '../components/AnomalyGauge'
import RegionCard from '../components/RegionCard'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const API = `${API_BASE_URL}/api`

/**
 * ReportPage — displays the full AI-generated neurological pre-report:
 * - Medical disclaimer (always at top)
 * - Brain map images (glass brain + slices + charts)
 * - Anomaly score gauge
 * - Affected brain regions list
 * - Structured findings & recommendations
 * - PDF export button
 */
export default function ReportPage() {
  const { id }     = useParams()
  const navigate   = useNavigate()

  const [report,   setReport]   = useState(null)
  const [loading,  setLoading]  = useState(true)
  const [error,    setError]    = useState('')
  const [exporting,setExporting]= useState(false)

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const { data } = await axios.get(`${API}/result/${id}`)
        setReport(data)
      } catch (err) {
        setError(err.response?.data?.detail || 'Erro ao carregar o relatório.')
      } finally {
        setLoading(false)
      }
    }
    fetchReport()
  }, [id])

  const exportPDF = async () => {
    setExporting(true)
    try {
      const res = await axios.get(`${API}/export-pdf/${id}`, { responseType: 'blob' })
      const url = URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }))
      const a   = document.createElement('a')
      a.href     = url
      a.download = `synapsia_relatorio_${id.slice(0, 8)}.pdf`
      document.body.appendChild(a)
      a.click()
      a.remove()
      URL.revokeObjectURL(url)
    } catch {
      alert('Erro ao exportar PDF. Tente novamente.')
    } finally {
      setExporting(false)
    }
  }

  // ── Loading state ────────────────────────────────────────────────────────
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="w-12 h-12 border-2 border-syn-blue border-t-transparent
                          rounded-full animate-spin mx-auto" />
          <p className="text-syn-muted">Carregando relatório...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="glass p-8 max-w-md text-center space-y-4 border-syn-danger/30">
          <p className="text-syn-danger font-semibold">{error}</p>
          <button className="btn-secondary" onClick={() => navigate('/upload')}>
            ← Tentar novamente
          </button>
        </div>
      </div>
    )
  }

  const score  = report?.anomaly_score ?? 0
  const level  = report?.anomaly_level ?? 'Baixo'
  const regions = report?.affected_regions ?? []
  const recs    = report?.recommendations   ?? []

  return (
    <main className="min-h-screen bg-syn-bg pb-20">
      {/* Top bar (Premium) */}
      <header
        className="sticky top-0 z-50 border-b border-syn-border/60 py-4 px-6
                   flex items-center justify-between shadow-lg"
        style={{ background: 'rgba(10,10,15,0.80)', backdropFilter: 'blur(20px)' }}
      >
        <div className="flex items-center gap-4">
          <button
            className="flex items-center gap-2 text-white font-bold hover:text-syn-blue transition-colors group"
            onClick={() => navigate('/')}
          >
            <span className="text-xl group-hover:-translate-x-1 transition-transform">←</span>
            Synaps<span className="text-syn-purple">IA</span>
          </button>
          <div className="h-6 w-px bg-syn-border/80"></div>
          <span className="text-syn-muted font-medium text-sm">Painel Analítico Neurométrico</span>
        </div>
        <button
          id="btn-export-pdf"
          className="btn-primary-premium py-2 px-6 text-sm shadow-[0_0_15px_rgba(168,85,247,0.3)]"
          onClick={exportPDF}
          disabled={exporting}
        >
          {exporting ? 'Processando...' : 'Baixar PDF Médico'}
        </button>
      </header>

      <div className="max-w-6xl mx-auto px-4 md:px-8 pt-8 space-y-8">

        {/* ── DISCLAIMER ──────────────────────────────────────────────── */}
        <div className="disclaimer">
          <strong>Atenção Médica:</strong> {report?.disclaimer}
        </div>

        {/* ── HEADER INFO ─────────────────────────────────────────────── */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'Data do Exame',         value: report?.exam_date ?? '—' },
            { label: 'Tempo de Processamento', value: `${report?.processing_time_seconds?.toFixed(1) ?? 0}s` },
            { label: 'Volumes Analisados',     value: report?.n_volumes ?? '—' },
            { label: 'Regiões Avaliadas',      value: report?.n_regions_analyzed ?? '—' },
          ].map(({ label, value }) => (
            <div key={label} className="glass p-4 text-center">
              <p className="text-xs text-syn-muted mb-1">{label}</p>
              <p className="text-xl font-bold gradient-text">{value}</p>
            </div>
          ))}
        </div>

        {/* Mode badge */}
        {report?.is_simulated && (
          <div className="glass p-3 border-syn-purple/30 text-center text-xs text-syn-purple font-semibold">
            Modo demonstração — dados simulados. Envie um arquivo fMRI real para análise completa.
          </div>
        )}

        {/* ── BRAIN MAPS ──────────────────────────────────────────────── */}
        <section>
          <SectionTitle title="Mapas Cerebrais" />
          <BrainViewer images={report?.images ?? {}} />
        </section>

        {/* ── ANOMALY SCORE ───────────────────────────────────────────── */}
        <section>
          <SectionTitle title="Score de Anomalia" />
          <div className="glass p-6 flex flex-col md:flex-row items-center gap-8">
            <AnomalyGauge score={score} level={level} />
            <div className="flex-1 space-y-3">
              <h3 className="text-lg font-bold text-syn-text">
                Interpretação do Score
              </h3>
              <p className="text-syn-muted text-sm leading-relaxed">
                O score de anomalia representa o grau de desvio dos padrões de conectividade
                funcional em relação à linha de base populacional. Um score{' '}
                <span className={
                  level === 'Alto' ? 'text-syn-danger' :
                  level === 'Moderado' ? 'text-syn-warn' : 'text-syn-ok'
                }>
                  {level.toLowerCase()}
                </span>{' '}
                indica{' '}
                {level === 'Alto'     ? 'alterações funcionais significativas que requerem avaliação clínica urgente.' :
                 level === 'Moderado' ? 'variações funcionais moderadas que merecem acompanhamento especializado.'     :
                                       'padrão de conectividade próximo ao esperado para a faixa etária.'}
              </p>
              <div className="flex gap-2 flex-wrap text-xs">
                <span className="badge-low    px-3 py-1 rounded-full">0.00–0.33 Baixo</span>
                <span className="badge-medium px-3 py-1 rounded-full">0.33–0.66 Moderado</span>
                <span className="badge-high   px-3 py-1 rounded-full">0.66–1.00 Alto</span>
              </div>
            </div>
          </div>
        </section>

        {/* ── AFFECTED REGIONS ────────────────────────────────────────── */}
        <section>
          <SectionTitle title={`Regiões Afetadas (${regions.length})`} />
          {regions.length === 0 ? (
            <div className="glass p-8 text-center text-syn-muted">
              Nenhuma região com desvio significativo identificada (limiar z = 2.0).
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {regions.map((r, i) => (
                <RegionCard key={i} region={r} index={i} />
              ))}
            </div>
          )}
        </section>

        {/* ── RECOMMENDATIONS ─────────────────────────────────────────── */}
        <section>
          <SectionTitle title="Recomendações Clínicas" />
          <div className="glass p-6 space-y-3">
            {recs.map((rec, i) => (
              <div key={i} className="flex gap-3 items-start text-sm">
                <span className="mt-0.5 w-6 h-6 flex-shrink-0 rounded-full bg-syn-blue/10
                                 text-syn-blue text-xs flex items-center justify-center font-bold border border-syn-blue/20">
                  {i + 1}
                </span>
                <p className="text-syn-muted leading-relaxed">{rec}</p>
              </div>
            ))}
          </div>
        </section>

        {/* ── EXPORT BUTTON (bottom) ───────────────────────────────────── */}
        <div className="flex justify-center pt-8">
          <button
            className="btn-primary-premium text-lg px-12 py-4 shadow-[0_0_30px_rgba(168,85,247,0.4)] hover:shadow-[0_0_50px_rgba(168,85,247,0.6)]"
            onClick={exportPDF}
            disabled={exporting}
          >
            {exporting ? 'Compilando PDF...' : 'Baixar Relatório Clínico Completo'}
          </button>
        </div>

        {/* Footer disclaimer */}
        <p className="text-center text-xs text-syn-muted/40 pb-4">
          SynapsIA — Este pré-relatório foi gerado por IA e não substitui a avaliação médica profissional.
          O médico é responsável pelo diagnóstico final.
        </p>

      </div>
    </main>
  )
}

function SectionTitle({ title }) {
  return (
    <div className="flex items-center gap-3 mb-4">
      <div className="w-1.5 h-6 bg-syn-purple rounded-full"></div>
      <h2 className="text-xl font-bold text-syn-text">{title}</h2>
      <div className="flex-1 h-px bg-syn-border" />
    </div>
  )
}
