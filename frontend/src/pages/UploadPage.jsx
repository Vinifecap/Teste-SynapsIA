import { useState, useCallback, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import NeuralBackground from '../components/NeuralBackground'
import ProgressBar from '../components/ProgressBar'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const API = `${API_BASE_URL}/api`
const ALLOWED = ['.nii', '.nii.gz']

/**
 * UploadPage — drag-and-drop NIfTI file upload with real-time processing progress
 */
export default function UploadPage() {
  const navigate   = useNavigate()
  const inputRef   = useRef(null)

  const [file,       setFile]       = useState(null)
  const [dragging,   setDragging]   = useState(false)
  const [uploading,  setUploading]  = useState(false)
  const [progress,   setProgress]   = useState(0)
  const [message,    setMessage]    = useState('')
  const [error,      setError]      = useState('')
  const [examId,     setExamId]     = useState(null)

  // ── File validation ──────────────────────────────────────────────────────
  const isValidFile = (f) =>
    f && (f.name.endsWith('.nii.gz') || f.name.endsWith('.nii'))

  const formatSize = (bytes) => {
    if (bytes < 1024)       return `${bytes} B`
    if (bytes < 1024 ** 2)  return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / 1024 ** 2).toFixed(2)} MB`
  }

  const handleFileSelect = (f) => {
    setError('')
    if (!isValidFile(f)) {
      setError('Formato inválido. Envie apenas arquivos .nii ou .nii.gz')
      return
    }
    setFile(f)
  }

  // ── Drag & Drop ──────────────────────────────────────────────────────────
  const onDragOver  = useCallback(e => { e.preventDefault(); setDragging(true)  }, [])
  const onDragLeave = useCallback(e => { e.preventDefault(); setDragging(false) }, [])
  const onDrop      = useCallback(e => {
    e.preventDefault()
    setDragging(false)
    handleFileSelect(e.dataTransfer.files[0])
  }, [])

  // ── Upload & Poll ────────────────────────────────────────────────────────
  const uploadExam = async () => {
    if (!file) return
    setUploading(true)
    setProgress(10)
    setMessage('Carregando exame...')
    setError('')

    try {
      const form = new FormData()
      form.append('file', file)

      const { data } = await axios.post(`${API}/upload`, form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setExamId(data.exam_id)
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao enviar o arquivo. Verifique o servidor.')
      setUploading(false)
    }
  }

  // Poll status once we have an exam_id
  useEffect(() => {
    if (!examId) return

    const poll = setInterval(async () => {
      try {
        const { data } = await axios.get(`${API}/status/${examId}`)
        setProgress(data.progress)
        setMessage(data.message)

        if (data.status === 'completed') {
          clearInterval(poll)
          setTimeout(() => navigate(`/report/${examId}`), 600)
        }
        if (data.status === 'error') {
          clearInterval(poll)
          setError(`Erro no processamento: ${data.message}`)
          setUploading(false)
        }
      } catch {
        clearInterval(poll)
        setError('Erro ao consultar o status do processamento.')
        setUploading(false)
      }
    }, 800)

    return () => clearInterval(poll)
  }, [examId, navigate])

  // ── UI ───────────────────────────────────────────────────────────────────
  return (
    <main className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden px-4 py-16">
      <NeuralBackground />

      {/* Back link */}
      <a href="/" className="absolute top-6 left-6 z-10 flex items-center gap-2
                              text-syn-muted hover:text-syn-blue transition-colors text-sm">
        ← Início
      </a>

      <div className="relative z-10 w-full max-w-xl space-y-6">

        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-extrabold text-white mb-2 tracking-tight">Análise <span className="text-syn-blue">Neuro-uncional</span></h1>
          <p className="text-syn-muted text-base font-medium">
            Upload seguro de ressonância magnética (fMRI) para detecção de desvios via IA
          </p>
        </div>

        {/* Drop zone */}
        {!uploading && (
          <div
            id="drop-zone"
            className={`relative overflow-hidden rounded-2xl p-12 flex flex-col items-center justify-center gap-6
                        transition-all duration-500 cursor-pointer select-none border border-syn-border
                        bg-syn-surface/40 backdrop-blur-xl shadow-2xl
                        ${dragging   ? 'border-syn-purple/70 glow-purple scale-[1.02]' : ''}
                        ${file       ? 'border-syn-ok/50'    : ''}
                        ${!file && !dragging ? 'hover:border-syn-blue/50 hover:bg-syn-surface/60 hover:shadow-syn-blue/10' : ''}`}
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onDrop={onDrop}
            onClick={() => !file && inputRef.current?.click()}
          >
            {/* Soft background glow */}
            <div className="absolute inset-0 pointer-events-none opacity-20"
                 style={{ background: 'radial-gradient(circle at 50% -20%, var(--blue), transparent 60%)' }} />

            <input
              ref={inputRef}
              type="file"
              accept=".nii,.nii.gz"
              className="hidden"
              onChange={e => handleFileSelect(e.target.files[0])}
            />

            {file ? (
              <>
                <div className="relative w-20 h-20 rounded-2xl bg-syn-ok/10 border border-syn-ok/40
                                flex items-center justify-center text-syn-ok font-bold uppercase text-sm shadow-[0_0_30px_rgba(34,197,94,0.15)]">
                  NIfTI
                </div>
                <div className="text-center">
                  <p className="font-bold text-white text-lg">{file.name}</p>
                  <p className="text-sm text-syn-ok font-medium mt-1">{formatSize(file.size)}</p>
                </div>
                <button
                  className="z-10 text-sm font-medium text-syn-muted hover:text-syn-danger transition-colors px-4 py-2 rounded border border-transparent hover:border-syn-danger/30 hover:bg-syn-danger/10 mt-2"
                  onClick={e => { e.stopPropagation(); setFile(null) }}
                >
                  Remover e enviar outro
                </button>
              </>
            ) : (
              <>
                <div className={`relative w-24 h-24 rounded-3xl border-2 border-dashed flex items-center
                                 justify-center transition-all duration-500
                                 ${dragging ? 'border-syn-purple bg-syn-purple/10 scale-110 shadow-lg glow-purple text-syn-purple' : 'border-syn-border text-syn-muted'}`}>
                  {dragging ? (
                    <div className="w-8 h-8 border-b-2 border-r-2 border-current transform rotate-45 -translate-y-2"></div>
                  ) : (
                    <div className="flex flex-col gap-1 items-center">
                      <div className="w-8 h-1 bg-current rounded px-4"></div>
                      <div className="w-6 h-1 bg-current rounded px-3"></div>
                      <div className="w-8 h-1 bg-current rounded px-4"></div>
                    </div>
                  )}
                </div>
                <div className="text-center">
                  <p className="font-bold text-white text-xl">
                    {dragging ? 'Solte para Iniciar' : 'Arraste seu NIfTI aqui'}
                  </p>
                  <p className="text-sm text-syn-muted mt-2 font-medium">
                    Ou clique para navegar. Suporte apenas para <span className="text-syn-blue">.nii</span> e <span className="text-syn-blue">.nii.gz</span>
                  </p>
                </div>
              </>
            )}
          </div>
        )}

        {/* Error message */}
        {error && (
          <div className="glass p-4 border-syn-danger/40 rounded-xl text-syn-danger text-sm font-semibold">
            Erro: {error}
          </div>
        )}

        {/* Progress (visible during processing) */}
        {uploading && (
          <div className="glass p-6 rounded-2xl space-y-4">
            <ProgressBar progress={progress} message={message} />
          </div>
        )}

        {/* Submit button */}
        {!uploading && file && (
          <button
            id="btn-analisar"
            className="btn-primary-premium w-full mt-4 py-4 text-lg"
            onClick={uploadExam}
            disabled={!file}
          >
            Processar Exame
          </button>
        )}

        {/* Info note */}
        {!uploading && (
          <div className="flex items-center justify-center gap-2 mt-4 text-syn-muted/60 text-sm">
            <span className="w-2 h-2 rounded-full bg-syn-purple animate-pulse"></span>
            <p>O processamento via inteligência artificial leva de 30 a 120 segundos</p>
          </div>
        )}
      </div>
    </main>
  )
}
