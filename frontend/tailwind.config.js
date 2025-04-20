/** @type {import('tailwindcss').Config} */
export default {
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  content: [],
  theme: {
    extend: {
      colors: {
        primary: '#259AE8',
        //secondary: '#F9A825',
        secondary: '#a7eaf1'
      }
    },
  },
  plugins: [],
}

