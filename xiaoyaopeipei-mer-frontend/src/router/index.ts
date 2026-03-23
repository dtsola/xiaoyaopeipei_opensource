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
const MembershipExpired = () => import('@/views/MembershipExpired.vue')
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
    path: '/membership-expired',
    name: 'MembershipExpired',
    component: MembershipExpired,
    meta: { title: '会员已过期 - 小遥配配', requiresAuth: true }
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
  // 通过环境变量 VITE_BASE_PATH 控制基础路径，默认为 /
  history: createWebHistory(import.meta.env.VITE_BASE_PATH || '/'),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()

  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title as string
  }

  // 如果是会员过期页面，直接放行
  if (to.name === 'MembershipExpired') {
    next()
    return
  }

  // 检查是否需要登录
  if (to.meta.requiresAuth !== false && !userStore.isLoggedIn) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.name === 'Login' && userStore.isLoggedIn) {
    // 如果已登录，检查会员状态
    if (userStore.user?.is_membership_expired) {
      next({ name: 'MembershipExpired' })
    } else {
      next({ name: 'Dashboard' })
    }
  } else if (userStore.isLoggedIn && userStore.user?.is_membership_expired) {
    // 如果会员已过期，跳转到会员过期页面（但profile页面允许访问，用于查看到期时间和续期）
    if (to.name === 'Profile') {
      next()
    } else {
      next({ name: 'MembershipExpired' })
    }
  } else {
    next()
  }
})

export default router
