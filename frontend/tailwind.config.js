/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'mondelez': {
          'purple': '#5F259F',
          'deep-purple': '#3E1F62',
          'blue': '#0066B2',
          'light-purple': '#8B5FBF',
          'accent-purple': '#9D7BB8',
          'dark-blue': '#003B71',
        },
      },
    },
  },
  plugins: [],
}

