/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',      // global template directory
    './**/templates/**/*.html',   // all app-level templates (flat structure)
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
