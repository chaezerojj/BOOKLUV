import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        secure: false,
        ws: true,
        // If backend sets cookies with a different domain (e.g. ngrok),
        // rewrite cookie domain to localhost so the browser accepts them during dev.
        cookieDomainRewrite: "localhost",
      },
    },
  },
});
