import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ArrowRight } from 'lucide-react';
import NeuralNetworkBackground from './NeuralNetworkBackground';

export default function HeroSection() {
  const comp = useRef();

  useEffect(() => {
    let ctx = gsap.context(() => {
      gsap.from('.hero-element', {
        y: 60,
        opacity: 0,
        duration: 1.2,
        stagger: 0.1,
        ease: 'power3.out',
        delay: 0.2
      });
    }, comp);
    return () => ctx.revert();
  }, []);

  return (
    <section ref={comp} className="relative h-[100dvh] w-full overflow-hidden flex flex-col justify-end pb-24 md:pb-32 bg-[#05050A]">
      <NeuralNetworkBackground />
      
      <div className="absolute inset-0 z-10 hero-gradient" />
      
      {/* Content */}
      <div className="relative z-20 px-6 md:px-12 w-full max-w-[1400px] mx-auto text-left">
        
        <p className="hero-element font-data text-syn-accent text-sm md:text-base tracking-[0.2em] mb-4 uppercase">
          TECNOLOGIA A FAVOR DA RECUPERAÇÃO
        </p>
        
        <h1 className="hero-element text-5xl md:text-7xl lg:text-[5.5rem] font-heading font-extrabold text-syn-text mb-2 leading-none">
          Movimento acompanhado
        </h1>
        
        <h2 className="hero-element text-6xl md:text-[8rem] lg:text-[10rem] font-drama italic text-syn-accent-light leading-[0.8] mb-6">
          evolução visível.
        </h2>
        
        <p className="hero-element max-w-xl text-syn-muted md:text-lg mt-8 mb-10 leading-relaxed font-sans">
          A SynapsIA ajuda profissionais a planejar exercícios, acompanhar os movimentos e visualizar a evolução de cada paciente ao longo do tratamento.
        </p>

        <div className="hero-element flex flex-col sm:flex-row items-center gap-4">
          <button className="btn-magnetic w-full sm:w-auto text-base glow-accent">
            <span>Conhecer a SynapsIA</span>
            <ArrowRight size={18} />
            <span className="slider-bg"></span>
          </button>
        </div>
      </div>
    </section>
  );
}
