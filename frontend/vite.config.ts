import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The proxy forwards /api/* to the FastAPI backend, so the browser
// only ever talks to one origin during development.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
