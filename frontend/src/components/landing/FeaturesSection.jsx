import { useEffect, useRef, useState } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { MousePointer2, Activity, Zap, Eye } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

// --- Componente: Diagnostic Shuffler (Card 1) ---
function DiagnosticShuffler() {
  const [cards, setCards] = useState([
    { id: 1, title: 'Aquisição de Imagem', time: '00:15', active: true },
    { id: 2, title: 'Processamento BOLD', time: '01:30', active: false },
    { id: 3, title: 'Segmentação Neural', time: '02:45', active: false }
  ]);

  useEffect(() => {
    const interval = setInterval(() => {
      setCards(prev => {
        const newArr = [...prev];
        const last = newArr.pop();
        newArr.unshift(last);
        return newArr;
      });
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="vapor-card relative h-80 flex flex-col items-center justify-center p-8">
      <div className="absolute top-6 left-6 text-syn-muted font-heading font-semibold text-sm">/01 Shuffler</div>
      
      <div className="relative w-full max-w-[220px] h-32 mt-6">
        {cards.map((c, i) => {
          // i=0 is front, i=1 is middle, i=2 is back
          const isFront = i === 0;
          return (
            <div 
              key={c.id}
              className={`absolute top-0 left-0 w-full p-4 rounded-[1.5rem] border transition-all duration-700 ease-[cubic-bezier(0.34,1.56,0.64,1)] ${
                isFront 
                  ? 'bg-syn-surface border-syn-accent/50 z-30 opacity-100 scale-100 translate-y-0 shadow-lg shadow-syn-accent/10' 
                  : i === 1 
                    ? 'bg-syn-card border-syn-border z-20 opacity-70 scale-95 -translate-y-6'
                    : 'bg-syn-bg border-syn-border/50 z-10 opacity-40 scale-90 -translate-y-12'
              }`}
            >
              <div className="flex justify-between items-center mb-3">
                <Activity size={18} className={isFront ? 'text-syn-accent' : 'text-syn-muted'} />
                <span className="font-data text-xs text-syn-muted">{c.time}</span>
              </div>
              <p className={`font-heading text-sm ${isFront ? 'text-syn-text' : 'text-syn-muted'}`}>
                {c.title}
              </p>
            </div>
          );
        })}
      </div>

      <div className="mt-auto pt-6 text-center w-full">
        <h3 className="font-heading font-bold text-xl text-syn-text">Velocidade Extrema</h3>
        <p className="text-sm text-syn-muted mt-2">Análise de fMRI em minutos, não em dias.</p>
      </div>
    </div>
  );
}

// --- Componente: Telemetry Typewriter (Card 2) ---
function TelemetryTypewriter() {
  const codeString = `> INITIATING NEURAL SCAN...
> DETECTING BOLD SIGNALS
> 12 ANOMALIES IDENTIFIED
> APPLYING ML FILTERS
> PRECISION LEVEL: 99.8%`;
  
  const [text, setText] = useState('');
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (index < codeString.length) {
      const timeout = setTimeout(() => {
        setText(prev => prev + codeString[index]);
        setIndex(index + 1);
      }, 50);
      return () => clearTimeout(timeout);
    } else {
      const reset = setTimeout(() => {
        setText('');
        setIndex(0);
      }, 4000);
      return () => clearTimeout(reset);
    }
  }, [index, codeString]);

  return (
    <div className="vapor-card h-80 flex flex-col p-8 relative">
      <div className="flex justify-between items-center mb-6">
        <div className="text-syn-muted font-heading font-semibold text-sm">/02 Typewriter</div>
        <div className="flex items-center gap-2">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-syn-accent opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-syn-accent"></span>
          </span>
          <span className="font-data text-xs text-syn-accent tracking-widest">LIVE FEED</span>
        </div>
      </div>
      
      <div className="flex-1 bg-syn-bg/50 rounded-2xl p-4 font-data text-sm text-syn-accent-light flex flex-col justify-end overflow-hidden border border-syn-border/30">
        <pre className="whitespace-pre-wrap flex-1 flex flex-col justify-end">
          {text}
          <span className="inline-block w-2.5 h-4 bg-syn-accent animate-pulse align-middle ml-1"></span>
        </pre>
      </div>

      <div className="mt-6 text-center w-full">
        <h3 className="font-heading font-bold text-xl text-syn-text">Precisão baseada em IA</h3>
        <p className="text-sm text-syn-muted mt-2">Identifica alterações neurais milimétricas instantaneamente.</p>
      </div>
    </div>
  );
}

// --- Componente: Cursor Protocol Scheduler (Card 3) ---
function CursorProtocolScheduler() {
  const gridRef = useRef();
  
  useEffect(() => {
    let ctx = gsap.context(() => {
      const tl = gsap.timeline({ repeat: -1, repeatDelay: 1 });
      
      // Reset
      tl.set('.cursor-svg', { x: -20, y: 150, opacity: 0, scale: 1 });
      tl.set('.grid-cell-target', { backgroundColor: 'transparent', borderColor: 'var(--border)' });
      tl.set('.save-btn-target', { scale: 1, backgroundColor: 'var(--surface)' });
      
      // Move cursor into view
      tl.to('.cursor-svg', { opacity: 1, duration: 0.2 })
        .to('.cursor-svg', { 
          x: 45, y: 35, duration: 1.2, ease: "power2.inOut" 
        })
        // Click action
        .to('.cursor-svg', { scale: 0.9, duration: 0.1 })
        .to('.grid-cell-target', { backgroundColor: 'var(--accent)', borderColor: 'var(--accent)', duration: 0.1 }, "<")
        .to('.cursor-svg', { scale: 1, duration: 0.1 })
        // Move to save button
        .to('.cursor-svg', {
          x: 140, y: 100, duration: 1, ease: "power2.inOut", delay: 0.3
        })
        // Click save
        .to('.cursor-svg', { scale: 0.9, duration: 0.1 })
        .to('.save-btn-target', { backgroundColor: 'var(--accent)', color: '#fff', duration: 0.1 }, "<")
        .to('.cursor-svg', { scale: 1, duration: 0.1 })
        // Fade out
        .to('.cursor-svg', { opacity: 0, x: 180, duration: 0.5, delay: 0.5 });
        
    }, gridRef);
    return () => ctx.revert();
  }, []);

  return (
    <div className="vapor-card h-80 flex flex-col p-8 relative" ref={gridRef}>
      <div className="absolute top-6 left-6 text-syn-muted font-heading font-semibold text-sm">/03 Scheduler</div>
      
      <div className="relative mt-8 h-[120px] w-[200px] mx-auto">
        <div className="grid grid-cols-5 gap-2">
          {['S','T','Q','Q','S'].map((d, i) => (
             <div key={i} className="text-center font-data text-xs text-syn-muted mb-1">{d}</div>
          ))}
          {Array.from({length: 10}).map((_, i) => (
            <div key={i} className={`h-6 rounded-md border border-syn-border transition-colors ${i === 7 ? 'grid-cell-target' : 'bg-syn-surface/50'}`}></div>
          ))}
        </div>
        
        <div className="absolute -bottom-2 right-0 save-btn-target border border-syn-border px-3 py-1 text-xs rounded-full font-heading text-syn-text transition-colors">
          Validar
        </div>

        {/* Cursor SVG */}
        <div className="cursor-svg absolute top-0 left-0 text-syn-text drop-shadow-[0_4px_8px_rgba(0,0,0,0.5)] z-40 pointer-events-none">
          <MousePointer2 fill="currentColor" size={24} />
        </div>
      </div>

      <div className="mt-auto pt-6 text-center w-full">
        <h3 className="font-heading font-bold text-xl text-syn-text">Validação Imediata</h3>
        <p className="text-sm text-syn-muted mt-2">Pré-relatório visual pronto para validação médica.</p>
      </div>
    </div>
  );
}

export default function FeaturesSection() {
  const containerRef = useRef();

  useEffect(() => {
    let ctx = gsap.context(() => {
      gsap.from('.feature-card', {
        scrollTrigger: {
          trigger: containerRef.current,
          start: "top 75%",
        },
        y: 50,
        opacity: 0,
        duration: 1,
        stagger: 0.15,
        ease: 'power3.out'
      });
    }, containerRef);
    return () => ctx.revert();
  }, []);

  return (
    <section id="features" ref={containerRef} className="py-24 px-6 md:px-12 w-full max-w-[1400px] mx-auto">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="feature-card"><DiagnosticShuffler /></div>
        <div className="feature-card"><TelemetryTypewriter /></div>
        <div className="feature-card"><CursorProtocolScheduler /></div>
      </div>
    </section>
  );
}
