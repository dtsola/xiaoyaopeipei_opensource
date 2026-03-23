/**
 * Vite配置文件 - 支持多环境配置
 */

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig(({ mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd())

  return {
    // 基础路径：通过环境变量 VITE_BASE_PATH 控制，默认为 /
    base: env.VITE_BASE_PATH || '/',

    plugins: [vue()],

    // 路径别名
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src')
      }
    },

    // 开发服务器配置
    server: {
      port: 5173,
      host: '0.0.0.0',
      open: true,
      // API代理配置（仅开发环境）
      proxy: {
        '/api': {
          target: env.VITE_API_BASE_URL || 'http://localhost:8001/api/mer',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        }
      }
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
            'chart-vendor': ['echarts', 'vue-echarts']
          }
        }
      }
    },

    // CSS配置
    css: {
      preprocessorOptions: {
        less: {
          javascriptEnabled: true,
          modifyVars: {
            // 主题色
            '@primary-color': '#2563eb',
            '@success-color': '#059669',
            '@warning-color': '#d97706',
            '@error-color': '#dc2626',
            '@info-color': '#0891b2',

            // 背景色
            '@body-background': '#fafbfc',
            '@component-background': '#ffffff',

            // 文字色
            '@heading-color': '#1a1d23',
            '@text-color': '#5a6370',
            '@text-color-secondary': '#8a94a5',
            '@disabled-color': '#d9d9d9',

            // 边框色
            '@border-color-base': '#e8eaed',
            '@border-color-split': '#f0f2f5',

            // 圆角
            '@border-radius-base': '10px',
            '@border-radius-lg': '16px',

            // 阴影
            '@shadow-1-up': '0 -4px 12px rgba(0, 0, 0, 0.06)',
            '@shadow-1-down': '0 4px 12px rgba(0, 0, 0, 0.06)',
            '@shadow-2': '0 8px 24px rgba(0, 0, 0, 0.12)',
          }
        }
      }
    }
  }
})
