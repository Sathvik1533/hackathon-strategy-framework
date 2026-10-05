/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        chassis: {
          dark: '#070a0f',
          panel: '#0d131f',
          border: '#1c2738',
          accent: '#00f59b',
          telemetry: '#00b4d8',
          warning: '#f59e0b',
          danger: '#ef4444',
        },
      },
      fontFamily: {
        mono: ['var(--font-geist-mono)', 'JetBrains Mono', 'monospace'],
        sans: ['var(--font-geist-sans)', 'Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
