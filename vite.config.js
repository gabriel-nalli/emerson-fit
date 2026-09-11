import { defineConfig } from 'vite'

export default defineConfig({
  publicDir: 'public',
  server: { port: 5175, strictPort: true, open: false },
  build: { outDir: 'dist' },
})
