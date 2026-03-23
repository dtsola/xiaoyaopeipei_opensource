/**
 * 小遥配配 B端 - 路由配置
 */

import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'

// 布局组件
const Layout = () => import('@/components/Layout.vue')

// 页面组件
const Login = () => import('@/views/Login.vue')
const Dashboard = () => import('@/views/Dashboard.vue')
const SKUList = () => import('@/views/SKU/List.vue')
const SKUForm = () => import('@/views/SKU/Form.vue')
const LeadList = () => import('@/views/Lead/List.vue')
const LeadDetail = () => import('@/views/Lead/Detail.vue')
const Share = () => import('@/views/Share.vue')
const Profile = () => import('@/views/Profile.vue')

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { title: '登录 - 小遥配配', requiresAuth: false }
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { title: '首页 - 小遥配配', icon: 'dashboard' }
      },
      {
        path: 'sku',
        name: 'SKUList',
        component: SKUList,
        meta: { title: 'SKU管理 - 小遥配配', icon: 'shopping' }
      },
      {
        path: 'sku/add',
        name: 'SKUAdd',
        component: SKUForm,
        meta: { title: '添加配置 - 小遥配配' }
      },
      {
        path: 'sku/edit/:id',
        name: 'SKUEdit',
        component: SKUForm,
        meta: { title: '编辑配置 - 小遥配配' }
      },
      {
        path: 'leads',
        name: 'LeadList',
        component: LeadList,
        meta: { title: '客户线索 - 小遥配配', icon: 'team' }
      },
      {
        path: 'leads/:id',
        name: 'LeadDetail',
        component: LeadDetail,
        meta: { title: '线索详情 - 小遥配配' }
      },
      {
        path: 'share',
        name: 'Share',
        component: Share,
        meta: { title: '分享管理 - 小遥配配', icon: 'share-alt' }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: Profile,
        meta: { title: '个人中心 - 小遥配配', icon: 'user' }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/dashboard'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title as string
  }

  // 检查是否需要登录
  if (to.meta.requiresAuth !== false && !userStore.isLoggedIn) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.name === 'Login' && userStore.isLoggedIn) {
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router
