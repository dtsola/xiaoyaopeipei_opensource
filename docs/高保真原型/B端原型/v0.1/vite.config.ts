import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
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
})
