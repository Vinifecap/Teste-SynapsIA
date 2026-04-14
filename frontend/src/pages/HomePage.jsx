import Navbar from '../components/landing/Navbar'
import HeroSection from '../components/landing/HeroSection'
import FeaturesSection from '../components/landing/FeaturesSection'
import { PhilosophySection, ProtocolSection, CtaFooterSection } from '../components/landing/SupplementalSections'

export default function HomePage() {
  return (
    <div className="bg-syn-bg min-h-screen text-syn-text selection:bg-syn-accent/30 selection:text-syn-accent-light">
      <Navbar />
      <main>
        <HeroSection />
        <FeaturesSection />
        <PhilosophySection />
        <ProtocolSection />
      </main>
      <CtaFooterSection />
    </div>
  )
}
