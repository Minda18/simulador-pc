import { defineConfig, loadEnv } from 'vite'

// Configuración de Vite para el simulador de PC.
// El proxy deja preparada la futura integración con las rutas /api de Django.
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')

  return {
    server: {
      host: '0.0.0.0',
      port: 5173,
      proxy: {
        '/api': {
          target: env.VITE_API_URL || 'http://localhost:8000',
          changeOrigin: true,
        },
      },
    },
  }
})
