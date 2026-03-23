<template>
  <div class="layout-container">
    <!-- 侧边栏 -->
    <aside class="layout-sidebar" :class="{ collapsed: appStore.sidebarCollapsed }">
      <!-- Logo区域 -->
      <div class="sidebar-header">
        <transition name="logo-fade">
          <div v-show="!appStore.sidebarCollapsed" class="sidebar-logo">
            <div class="logo-icon">
              <svg width="32" height="32" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="4" y="8" width="40" height="32" rx="4" fill="currentColor"/>
                <rect x="8" y="12" width="28" height="20" rx="2" fill="currentColor" fill-opacity="0.3"/>
                <path d="M36 16L44 24V36H36V16Z" fill="currentColor" fill-opacity="0.5"/>
              </svg>
            </div>
            <span class="logo-text">小遥配配</span>
          </div>
        </transition>
        <div v-show="appStore.sidebarCollapsed" class="sidebar-logo-collapsed">
          <svg width="32" height="32" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="4" y="8" width="40" height="32" rx="4" fill="currentColor"/>
            <rect x="8" y="12" width="28" height="20" rx="2" fill="currentColor" fill-opacity="0.3"/>
            <path d="M36 16L44 24V36H36V16Z" fill="currentColor" fill-opacity="0.5"/>
          </svg>
        </div>
      </div>

      <!-- 导航菜单 -->
      <nav class="sidebar-nav">
        <router-link
          v-for="item in menuItems"
          :key="item.key"
          :to="{ name: item.name }"
          class="nav-item"
          :class="{ active: $route.name === item.key }"
        >
          <component :is="item.icon" class="nav-icon" />
          <transition name="text-fade">
            <span v-show="!appStore.sidebarCollapsed" class="nav-text">{{ item.label }}</span>
          </transition>
          <div v-if="item.badge && !appStore.sidebarCollapsed" class="nav-badge">{{ item.badge }}</div>
        </router-link>
      </nav>

      <!-- 侧边栏底部 -->
      <div class="sidebar-footer">
        <div class="footer-user" @click="router.push('/profile')">
          <div class="user-avatar">
            {{ userStore.userName?.charAt(0)?.toUpperCase() || 'U' }}
          </div>
          <transition name="text-fade">
            <div v-show="!appStore.sidebarCollapsed" class="user-info">
              <div class="user-name text-ellipsis">{{ userStore.shopName }}</div>
              <div class="user-role">商家后台</div>
            </div>
          </transition>
        </div>
      </div>
    </aside>

    <!-- 主体内容区 -->
    <div class="layout-main">
      <!-- 顶部导航栏 -->
      <header class="layout-header">
        <!-- 左侧：折叠按钮 -->
        <div class="header-left">
          <button class="collapse-btn" @click="appStore.toggleSidebar">
            <MenuUnfoldOutlined v-if="appStore.sidebarCollapsed" />
            <MenuFoldOutlined v-else />
          </button>
          <a-breadcrumb class="header-breadcrumb">
            <a-breadcrumb-item v-for="item in breadcrumbItems" :key="item.path">
              {{ item.name }}
            </a-breadcrumb-item>
          </a-breadcrumb>
        </div>

        <!-- 右侧：操作区 -->
        <div class="header-right">
          <!-- 刷新按钮 -->
          <button class="header-action" @click="handleRefresh" title="刷新">
            <ReloadOutlined :spin="isRefreshing" />
          </button>

          <!-- 通知 -->
          <a-dropdown placement="bottomRight">
            <button class="header-action">
              <a-badge :count="appStore.notificationCount" :offset="[-4, 4]">
                <BellOutlined />
              </a-badge>
            </button>
            <template #overlay>
              <a-menu class="notification-menu">
                <a-menu-item v-for="n in notifications" :key="n.id">
                  <div class="notification-item">
                    <div class="notification-content">{{ n.content }}</div>
                    <div class="notification-time">{{ n.time }}</div>
                  </div>
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item @click="appStore.clearNotifications">
                  <a>清空通知</a>
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>

          <!-- 用户菜单 -->
          <a-dropdown placement="bottomRight">
            <button class="header-action user-action">
              <div class="user-avatar-small">
                {{ userStore.userName?.charAt(0)?.toUpperCase() || 'U' }}
              </div>
              <span class="user-name-dropdown">{{ userStore.userName }}</span>
              <DownOutlined />
            </button>
            <template #overlay>
              <a-menu>
                <a-menu-item @click="router.push('/profile')">
                  <UserOutlined />
                  <span>个人中心</span>
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item @click="handleLogout">
                  <LogoutOutlined />
                  <span>退出登录</span>
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </div>
      </header>

      <!-- 内容区域 -->
      <main class="layout-content">
        <router-view v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>

    <!-- 退出确认弹窗 -->
    <a-modal
      v-model:open="logoutVisible"
      title="确认退出"
      content="确定要退出登录吗？"
      centered
      @ok="handleConfirmLogout"
    >
      <template #footer>
        <a-button @click="logoutVisible = false">取消</a-button>
        <a-button type="primary" danger @click="handleConfirmLogout">确定退出</a-button>
      </template>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Modal } from 'ant-design-vue'
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  DashboardOutlined,
  ShoppingOutlined,
  TeamOutlined,
  ShareAltOutlined,
  UserOutlined,
  LogoutOutlined,
  BellOutlined,
  ReloadOutlined,
  DownOutlined
} from '@ant-design/icons-vue'
import { useAppStore } from '@/stores/app'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const appStore = useAppStore()
const userStore = useUserStore()

// 刷新状态
const isRefreshing = ref(false)

// 退出确认
const logoutVisible = ref(false)

// 菜单项
const menuItems = [
  { key: 'Dashboard', name: 'Dashboard', label: '首页', icon: DashboardOutlined },
  { key: 'SKUList', name: 'SKUList', label: 'SKU管理', icon: ShoppingOutlined },
  { key: 'LeadList', name: 'LeadList', label: '客户线索', icon: TeamOutlined },
  { key: 'Share', name: 'Share', label: '分享管理', icon: ShareAltOutlined },
  { key: 'Profile', name: 'Profile', label: '个人中心', icon: UserOutlined }
]

// 通知数据
const notifications = ref([
  { id: 1, content: '您有3条新线索待跟进', time: '10分钟前' },
  { id: 2, content: '客户A选择了联想拯救者Y7000P', time: '25分钟前' },
  { id: 3, content: '您的分享海报已生成', time: '1小时前' }
])

// 面包屑
const breadcrumbMap: Record<string, string> = {
  Dashboard: '首页',
  SKUList: 'SKU管理',
  SKUAdd: '添加配置',
  SKUEdit: '编辑配置',
  LeadList: '客户线索',
  LeadDetail: '线索详情',
  Share: '分享管理',
  Profile: '个人中心'
}

const breadcrumbItems = computed(() => {
  const items = [{ path: '/dashboard', name: '首页' }]
  const currentName = route.name as string
  if (currentName && currentName !== 'Dashboard' && breadcrumbMap[currentName]) {
    items.push({ path: route.path, name: breadcrumbMap[currentName] })
  }
  return items
})

// 刷新页面
function handleRefresh() {
  isRefreshing.value = true
  setTimeout(() => {
    window.location.reload()
  }, 300)
}

// 退出登录
function handleLogout() {
  logoutVisible.value = true
}

function handleConfirmLogout() {
  userStore.logout()
  logoutVisible.value = false
  router.push('/login')
}
</script>

<style scoped>
.layout-container {
  display: flex;
  min-height: 100vh;
}

/* ========== 侧边栏 ========== */
.layout-sidebar {
  width: var(--sidebar-width);
  background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  z-index: 100;
  transition: width var(--transition-base);
}

.layout-sidebar.collapsed {
  width: 80px;
}

.sidebar-header {
  height: var(--header-height);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(37, 99, 235, 0.2);
  border-radius: var(--radius-md);
  color: #60a5fa;
  flex-shrink: 0;
}

.logo-text {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 600;
  color: #ffffff;
  white-space: nowrap;
}

.sidebar-logo-collapsed {
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar-logo-collapsed .logo-icon {
  width: 36px;
  height: 36px;
}

/* 导航菜单 */
.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  margin-bottom: 4px;
  transition: all var(--transition-fast);
  position: relative;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.nav-item.active {
  background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.nav-icon {
  font-size: 18px;
  flex-shrink: 0;
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}

.nav-badge {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
}

/* 侧边栏底部 */
.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-user {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.footer-user:hover {
  background: rgba(255, 255, 255, 0.1);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 16px;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: #ffffff;
}

.user-role {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
}

/* ========== 主体内容区 ========== */
.layout-main {
  flex: 1;
  margin-left: var(--sidebar-width);
  display: flex;
  flex-direction: column;
  transition: margin-left var(--transition-base);
}

.layout-sidebar.collapsed + .layout-main {
  margin-left: 80px;
}

/* ========== 顶部导航栏 ========== */
.layout-header {
  height: var(--header-height);
  background: var(--bg-card);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 50;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.collapse-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  transition: all var(--transition-fast);
}

.collapse-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.header-breadcrumb :deep(.ant-breadcrumb-link) {
  color: var(--text-secondary);
}

.header-breadcrumb :deep(.ant-breadcrumb-separator) {
  color: var(--text-tertiary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-action {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  transition: all var(--transition-fast);
}

.header-action:hover {
  background: var(--bg-hover);
  color: var(--primary-color);
}

.user-action {
  width: auto;
  padding: 0 12px;
  gap: 8px;
}

.user-avatar-small {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--primary-color), var(--primary-hover));
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 12px;
}

.user-name-dropdown {
  font-size: 14px;
  color: var(--text-primary);
  max-width: 100px;
}

/* ========== 内容区域 ========== */
.layout-content {
  flex: 1;
  padding: var(--content-padding);
  min-height: calc(100vh - var(--header-height));
}

/* ========== 页面切换动画 ========== */
.page-enter-active,
.page-leave-active {
  transition: all var(--transition-base);
}

.page-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* ========== 过渡动画 ========== */
.logo-fade-enter-active,
.logo-fade-leave-active,
.text-fade-enter-active,
.text-fade-leave-active {
  transition: all var(--transition-base);
}

.logo-fade-enter-from,
.logo-fade-leave-to,
.text-fade-enter-from,
.text-fade-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}

/* ========== 通知菜单 ========== */
.notification-menu {
  width: 320px;
  max-height: 400px;
  overflow-y: auto;
}

.notification-item {
  padding: 4px 0;
}

.notification-content {
  font-size: 14px;
  color: var(--text-primary);
}

.notification-time {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-top: 4px;
}
</style>
