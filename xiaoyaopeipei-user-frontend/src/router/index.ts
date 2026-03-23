/**
 * 路由配置
 * 小遥配配 - C端原型
 */

import type { RouteRecordRaw } from 'vue-router'

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Chat',
    component: () => import('@/views/ChatView.vue'),
    meta: {
      title: '小遥配配',
      keepAlive: true,
    },
  },
  {
    path: '/recommend',
    name: 'Recommend',
    component: () => import('@/views/RecommendView.vue'),
    meta: {
      title: '为您推荐',
      showBack: true,
    },
  },
  {
    path: '/detail/:id',
    name: 'Detail',
    component: () => import('@/views/DetailView.vue'),
    meta: {
      title: '方案详情',
      showBack: true,
    },
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('@/views/ContactView.vue'),
    meta: {
      title: '留下联系方式',
      showBack: true,
    },
  },
  {
    path: '/success',
    name: 'Success',
    component: () => import('@/views/SuccessView.vue'),
    meta: {
      title: '提交成功',
    },
  },
  {
    path: '/compare',
    name: 'Compare',
    component: () => import('@/views/CompareView.vue'),
    meta: {
      title: '方案对比',
      showBack: true,
    },
  },
  {
    path: '/terms',
    name: 'Terms',
    component: () => import('@/views/TermsView.vue'),
    meta: {
      title: '用户协议',
      showBack: true,
    },
  },
  {
    path: '/privacy',
    name: 'Privacy',
    component: () => import('@/views/PrivacyView.vue'),
    meta: {
      title: '隐私政策',
      showBack: true,
    },
  },
]
