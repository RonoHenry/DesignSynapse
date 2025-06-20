module.exports = {
    // Scan all JS/JSX/TS/TSX files in src for Tailwind classes
    content: [
      "./src/**/*.{js,jsx,ts,tsx}",
      "./public/index.html"
    ],
    theme: { extend: {} },
    plugins: [],
  };