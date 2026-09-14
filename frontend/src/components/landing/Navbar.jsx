import { useEffect, useState } from 'react'
import { ArrowRight } from 'lucide-react'

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50)
    }

    window.addEventListener('scroll', handleScroll)

    return () => {
      window.removeEventListener('scroll', handleScroll)
    }
  }, [])

  return (
    <nav
      className={`fixed top-6 left-1/2 -translate-x-1/2 z-50 transition-all duration-500 rounded-full px-6 py-3 flex items-center justify-between min-w-[90vw] md:min-w-[70vw] lg:min-w-[1000px] ${
        scrolled
          ? 'bg-syn-surface/70 backdrop-blur-xl border border-syn-border shadow-2xl'
          : 'bg-transparent border-transparent'
      }`}
    >
      <div className="flex items-center gap-3 cursor-pointer">
        <div className="w-10 h-10 rounded-full overflow-hidden flex items-center justify-center bg-syn-surface border border-syn-border shrink-0">
          <img
            src="/logo.png"
            alt="Logo da SynapsIA"
            className="w-full h-full object-cover"
          />
        </div>

        <span className="font-heading font-bold text-xl text-syn-text tracking-tight">
          SynapsIA
        </span>
      </div>

      <div className="hidden md:flex gap-8 text-sm font-medium">
        <a
          href="#features"
          className="interactive-link text-syn-text"
        >
          Tecnologia
        </a>

        <a
          href="#protocol"
          className="interactive-link text-syn-text"
        >
          Protocolo
        </a>

        <span
          className="text-syn-muted cursor-not-allowed"
          title="O novo MVP será integrado em breve"
        >
          Portal MVP
        </span>
      </div>

      <button className="btn-magnetic text-sm px-5 py-2">
        <span>Solicitar Demo</span>
        <ArrowRight size={16} />
        <span className="slider-bg" />
      </button>
    </nav>
  )
}