/**
 * 应用入口文件
 * 小遥配配 - C端原型
 */

import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'
import './styles/global.less'
import App from './App.vue'
import { routes } from './router'

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0, behavior: 'smooth' }
  },
})

// 创建应用实例
const app = createApp(App)

// 使用插件
app.use(router)
app.use(Antd)

// 挂载应用
app.mount('#app')
