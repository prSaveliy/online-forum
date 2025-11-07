/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Django templates (theme and app-level)
    '../templates/**/*.html',
    '../../templates/**/*.html',
    '../../../**/templates/**/*.html',

    // JS inside your static_src folder
    './src/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        // Example custom palette (optional)
        primary: {
          DEFAULT: '#1d4ed8', // blue-700
          light: '#3b82f6',   // blue-500
          dark: '#1e40af',    // blue-800
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms')
  ],
}