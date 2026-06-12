/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c084fc',
          400: '#a855f7',
          500: '#8b5cf6', // main brand purple
          600: '#7c3aed',
          700: '#6d28d9',
        },
        accent: {
          cyan: '#06b6d4',
          yellow: '#f59e0b',
          pink: '#ec4899',
          green: '#10b981',
          coral: '#f43f5e',
        }
      },
      fontFamily: {
        comic: ['"Comic Sans MS"', 'cursive', 'sans-serif'],
        sans: ['Inter', 'Roboto', 'sans-serif'],
      },
      borderRadius: {
        'kids': '1.5rem',
      }
    },
  },
  plugins: [],
}
