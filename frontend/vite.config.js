import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
<<<<<<< HEAD
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8006',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
=======
  plugins: [vue({
    script: {
      defineModel: true,
      propsDestructure: true
    }
  })],
  server: {
    port: 5176,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://localhost:8007',
        changeOrigin: true
      }
    },
    fs: {
      strict: false
    }
  },
  preview: {
    port: 5176,
    host: '0.0.0.0'
  },
  optimizeDeps: {
    include: ['three', 'vue'],
    exclude: []
  },
  build: {
    commonjsOptions: {
      include: [/three/, /node_modules/]
    },
    rollupOptions: {
      output: {
        manualChunks: undefined
      }
    }
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  }
})

>>>>>>> 694dc7c (the_last_update)
