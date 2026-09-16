/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dhaba: {
          bg: "#121214",
          surface: "#1a1a1e",
          card: "#222227",
          border: "#2e2e36",
          accent: "#f97316",
          accentHover: "#ea580c",
          accentGlow: "rgba(249, 115, 22, 0.15)",
          cream: "#fafaf9",
          muted: "#a1a1aa",
          success: "#10b981",
          warning: "#f59e0b",
          danger: "#ef4444",
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
