import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx}",
    "./src/components/**/*.{js,ts,jsx,tsx}",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      keyframes: {
        truckMove: {
          "0%": { transform: "translateX(calc(100% + 120px))" },
          "100%": { transform: "translateX(-120px)" }
        },
        wheelRotate: {
          from: { transform: "rotate(0deg)" },
          to: { transform: "rotate(-360deg)" }
        },
        roadMove: {
          "0%": { transform: "translateX(-400px)" },
          "100%": { transform: "translateX(0)" }
        },
        lampGlow: {
          "0%, 100%": { opacity: "0.5", filter: "drop-shadow(0 0 3px rgba(251,191,36,0.4))" },
          "50%": { opacity: "1", filter: "drop-shadow(0 0 10px rgba(251,191,36,0.9))" }
        }
      },
      animation: {
        truckMove: "truckMove 3.5s cubic-bezier(0.4, 0, 0.2, 1) infinite",
        wheelRotate: "wheelRotate 0.25s linear infinite",
        roadMove: "roadMove 0.5s linear infinite",
        lampGlow: "lampGlow 1.2s ease-in-out infinite"
      }
    }
  },
  plugins: []
};

export default config;

