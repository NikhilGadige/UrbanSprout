/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        forest: {
          950: '#0A0F0A', // Near-black background with green tint
          900: '#111711', // Dark forest base
          800: '#1A2E1A', // Deep glass card base
          700: '#2D4A2D', // Muted green border
          600: '#4B7A4B', // Muted text/placeholder
        },
        accent: {
          green: '#4ADE80', // Vibrant lime green
          mint: '#86EFAC',  // Soft hover mint
          amber: '#FCD34D', // Amber warning/modal
          red: '#F87171',   // Soft danger red
        }
      },
      fontFamily: {
        display: ['Syne', 'sans-serif'], // For Headings, Brand, Hero
        body: ['DM Sans', 'sans-serif'],   // For Body Copy, Buttons, Inputs
      },
      boxShadow: {
        'glow-green': '0 0 20px rgba(74, 222, 128, 0.15)',
        'glow-green-bright': '0 0 30px rgba(74, 222, 128, 0.3)',
      },
      backgroundImage: {
        'grid-pattern': "radial-gradient(rgba(74, 222, 128, 0.05) 1px, transparent 1px)",
      }
    },
  },
  plugins: [],
}
