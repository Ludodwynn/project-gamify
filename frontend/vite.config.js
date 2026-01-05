import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
//import tailwindcss from '@tailwindcss/vite';
import electron from 'vite-plugin-electron';

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    //tailwindcss(),
    electron({
      entry: 'electron/main.cjs', // Chemin vers ton fichier principal Electron
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
