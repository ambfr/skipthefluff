/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        red: {
          500: '#E8294C',
          600: '#C9203E',
        },
        pink: {
          50: '#FFF0F3',
          100: '#FFD6DE',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        playfair: ['"Playfair Display"', 'serif'],
      },
    }
  },
  plugins: []
}
