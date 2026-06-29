// File location: frontend/vite.config.js
//
// Vite 6.x config. Two plugins only: the official React plugin and the
// official Tailwind v4 Vite plugin (no PostCSS config, no
// tailwind.config.js needed -- Tailwind v4 reads its configuration from
// CSS directly, see src/index.css).
//
// The /api proxy means the frontend dev server forwards any request
// starting with /api straight to the Django backend on port 8000, so
// the frontend code can call fetch("/api/v1/...") without hardcoding a
// host, and without hitting CORS in development.
 
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
 
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
});
 
