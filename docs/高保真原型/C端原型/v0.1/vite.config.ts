import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
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
  server: {
    port: 3000,
    open: true,
  },
})
