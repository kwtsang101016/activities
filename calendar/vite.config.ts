import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ command }) => ({
  plugins: [react()],
  base: command === "build" ? "/activities/consult2027/calendar/" : "/",
  build: {
    outDir: "../consult2027/calendar",
    emptyOutDir: true,
  },
  server: {
    host: "127.0.0.1",
    port: 5179,
    strictPort: false,
  },
}));
