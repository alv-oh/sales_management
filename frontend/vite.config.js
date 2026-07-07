import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  // React plugin plus a fixed port so API CORS settings stay predictable.
  plugins: [react()],
  server: {
    port: 5173,
  },
});
