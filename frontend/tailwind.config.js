/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "syn-bg":       "#0a0a14", /* Vazio Profundo */
        "syn-surface":  "#12121a",
        "syn-card":     "#18181b", /* Grafite */
        "syn-border":   "#27272a",
        "syn-accent":   "#7b61ff", /* Plasma */
        "syn-accent-light": "#9c8aff",
        "syn-text":     "#f0eff4", /* Fantasma */
        "syn-muted":    "#a1a1aa",
        "syn-danger":   "#ef4444",
        "syn-warn":     "#f59e0b",
        "syn-ok":       "#22c55e",
      },
      fontFamily: {
        sans: ["Sora", "system-ui", "sans-serif"],    /* Headings & Base */
        serif: ["Instrument Serif", "serif"],         /* Drama */
        mono: ["Fira Code", "monospace"],             /* Data */
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'hero-glow': 'radial-gradient(circle at 50% 0%, rgba(123, 97, 255, 0.15) 0%, transparent 60%)',
      },
      animation: {
        "pulse-slow":    "pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "float":         "float 6s ease-in-out infinite",
        "scan-line":     "scanLine 3s linear infinite",
        "shimmer":       "shimmer 2s linear infinite",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%":      { transform: "translateY(-12px)" },
        },
        scanLine: {
          "0%":   { transform: "translateY(-100%)", opacity: 0 },
          "50%":  { opacity: 1 },
          "100%": { transform: "translateY(100%)", opacity: 0 },
        },
        shimmer: {
          "0%":   { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
      backdropBlur: {
        xs: "2px",
      },
    },
  },
  plugins: [],
}
