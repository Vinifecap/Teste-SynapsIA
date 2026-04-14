import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { ArrowRight, Fingerprint, ActivitySquare, Workflow } from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

export function PhilosophySection() {
  const sectionRef = useRef();

  useEffect(() => {
    let ctx = gsap.context(() => {
      gsap.from('.philo-line', {
        scrollTrigger: {
          trigger: sectionRef.current,
          start: 'top 60%',
        },
        y: 30,
        opacity: 0,
        duration: 1,
        stagger: 0.2,
        ease: 'power3.out'
      });
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={sectionRef} className="relative py-32 px-6 md:px-12 w-full max-w-[1400px] mx-auto overflow-hidden">
      <div 
        className="absolute inset-0 z-0 bg-cover bg-center opacity-10 mix-blend-screen pointer-events-none"
        style={{ backgroundImage: "url('https://images.unsplash.com/photo-1543881267-27bfe62174c0?q=80&w=2070&auto=format&fit=crop')" }} 
      />
      <div className="relative z-10 max-w-4xl">
        <p className="philo-line font-heading text-syn-muted text-lg md:text-2xl mb-6">
          A maioria dos sistemas foca em arquivar imagens.
        </p>
        <p className="philo-line font-drama italic text-5xl md:text-7xl lg:text-[6rem] text-syn-text leading-[0.9]">
          Nós focamos em <span className="text-syn-accent-light not-italic font-heading tracking-tight drop-shadow-[0_0_30px_rgba(123,97,255,0.4)]">movimento.</span>
        </p>
      </div>
    </section>
  );
}

export function ProtocolSection() {
  const containerRef = useRef();

  useEffect(() => {
    let ctx = gsap.context(() => {
      const cards = gsap.utils.toArray('.sticky-card');
      
      cards.forEach((card, i) => {
        if (i < cards.length - 1) {
          ScrollTrigger.create({
            trigger: card,
            start: "top 20%",
            endTrigger: '.protocol-wrapper',
            end: "bottom bottom",
            pin: true,
            pinSpacing: false,
          });

          gsap.to(card, {
            scale: 0.9,
            opacity: 0.5,
            filter: "blur(10px)",
            scrollTrigger: {
              trigger: cards[i + 1],
              start: "top 60%",
              end: "top 20%",
              scrub: true,
            }
          });
        }
      });
    }, containerRef);
    return () => ctx.revert();
  }, []);

  const steps = [
    { num: '01', title: 'Extração de Biometria', desc: 'Processamento de fMRI com identificação paralela de anomalias.', Icon: Fingerprint },
    { num: '02', title: 'Integração de IA', desc: 'Mapeamento neural com algoritmos de deep learning para classificar padrões BOLD.', Icon: ActivitySquare },
    { num: '03', title: 'Plataforma de Reabilitação', desc: 'Pré-relatórios gerados para validar o diagnóstico e acelerar o retorno à vida.', Icon: Workflow },
  ];

  return (
    <section id="protocol" className="py-24 px-6 md:px-12 w-full max-w-[1400px] mx-auto protocol-wrapper" ref={containerRef}>
      <h2 className="font-heading font-extrabold text-4xl md:text-6xl mb-16 text-center">Protocolo Central</h2>
      
      <div className="relative flex flex-col gap-24 h-full pb-32">
        {steps.map((step, i) => (
          <div key={i} className="sticky-card vapor-card h-[60vh] md:h-[70vh] flex flex-col md:flex-row shadow-2xl relative w-full overflow-hidden">
            {/* Visual Part */}
            <div className="w-full md:w-1/2 bg-syn-bg h-full flex items-center justify-center border-b md:border-b-0 md:border-r border-syn-border/50 relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-syn-accent/10 to-transparent"></div>
              <step.Icon size={120} className="text-syn-accent/20 animate-pulse-slow" />
              {/* Optional: Add a CSS scanline effect here */}
              {i === 1 && <div className="absolute inset-0 w-full h-1 bg-syn-accent/30 animate-scan-line shadow-[0_0_20px_rgba(123,97,255,0.8)]"></div>}
            </div>
            
            {/* Text Part */}
            <div className="w-full md:w-1/2 p-8 md:p-16 flex flex-col justify-center bg-syn-surface/80 backdrop-blur-md">
              <span className="font-data text-syn-accent text-xl mb-4">//{step.num}</span>
              <h3 className="font-heading font-bold text-3xl md:text-5xl text-syn-text mb-6">{step.title}</h3>
              <p className="text-syn-muted text-lg md:text-xl leading-relaxed">{step.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export function CtaFooterSection() {
  return (
    <footer className="w-full mt-32">
      {/* CTA Get Started - Adapting from Membership pricing rules */}
      <div className="w-full max-w-[800px] mx-auto px-6 mb-32 text-center">
        <div className="vapor-card glow-accent p-12 md:p-16 flex flex-col items-center">
          <h2 className="font-heading font-extrabold text-4xl md:text-6xl text-syn-text mb-6">Pronto para iniciar?</h2>
          <p className="text-syn-muted text-lg mb-10 max-w-lg">Solicite uma demonstração do instrumento MVP e veja em tempo real nossa IA conectando cérebro e movimento.</p>
          <button className="btn-magnetic w-full md:w-auto text-lg px-8 py-4 glow-accent bg-syn-accent/10">
            <span>Solicitar Demo Agora</span>
            <ArrowRight size={20} />
            <span className="slider-bg"></span>
          </button>
        </div>
      </div>

      {/* Footer Details */}
      <div className="bg-syn-bg border-t border-syn-border rounded-t-[4rem] px-8 py-16 text-center md:text-left flex flex-col md:flex-row justify-between items-center gap-8">
        <div className="flex flex-col items-center md:items-start gap-2">
          <div className="font-heading font-bold text-2xl text-syn-text tracking-tight shadow-sm">SynapsIA</div>
          <p className="text-syn-muted text-sm">Do diagnóstico à reabilitação.</p>
        </div>
        
        <div className="flex items-center gap-3 bg-syn-surface border border-syn-border px-4 py-2 rounded-full cursor-default">
          <span className="relative flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-syn-ok opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-syn-ok"></span>
          </span>
          <span className="font-data text-xs tracking-wider text-syn-muted">SISTEMA OPERACIONAL</span>
        </div>
      </div>
    </footer>
  );
}
