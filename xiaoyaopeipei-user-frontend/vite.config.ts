/**
 * Vite配置文件 - 支持多环境配置（C端）
 */

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig(({ mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd())

  return {
    plugins: [vue()],

    // 路径别名
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src'),
      },
    },

    // 开发服务器配置
    server: {
      port: 5174,
      host: '0.0.0.0',
      open: true,
      // API代理配置（仅开发环境）
      proxy: {
        '/api': {
          target: env.VITE_API_BASE_URL || 'http://localhost:8001/api/user',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },

    // 构建配置
    build: {
      target: 'es2015',
      outDir: 'dist',
      assetsDir: 'assets',
      sourcemap: mode === 'development',
      minify: 'esbuild',
      chunkSizeWarningLimit: 1000,
      rollupOptions: {
        output: {
          // 分包策略
          manualChunks: {
            'vue-vendor': ['vue', 'vue-router', 'pinia'],
            'antd-vendor': ['ant-design-vue', '@ant-design/icons-vue'],
          },
        },
      },
    },

    // CSS配置
    css: {
      preprocessorOptions: {
        less: {
          javascriptEnabled: true,
          modifyVars: {
            // 科技白风格主题变量
            '@primary-color': '#FF6B35',
            '@primary-color-hover': '#FF8C5A',
            '@text-color': '#1A1A1A',
            '@text-color-secondary': '#6B7280',
            '@text-color-tertiary': '#9CA3AF',
            '@border-radius-base': '12px',
            '@border-radius-sm': '8px',
            '@border-radius-lg': '16px',
            '@box-shadow-base': '0 2px 8px rgba(0, 0, 0, 0.06)',
            '@box-shadow-lg': '0 8px 24px rgba(0, 0, 0, 0.12)',
          },
        },
      },
    },
  }
})
