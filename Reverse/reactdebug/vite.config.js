import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    port: 5173,
    open: true,
  },
  build: {
    sourcemap: false,
    target: 'es2019',
    // minify so small and obfuscate
  },
});
