/**
 * 小遥配配 B端 - 应用状态管理
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  // 侧边栏折叠状态
  const sidebarCollapsed = ref(false)

  // 当前选中的菜单
  const currentMenu = ref('dashboard')

  // 全局loading
  const globalLoading = ref(false)

  // 切换侧边栏
  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  // 设置当前菜单
  function setCurrentMenu(menu: string) {
    currentMenu.value = menu
  }

  // 设置全局loading
  function setGlobalLoading(loading: boolean) {
    globalLoading.value = loading
  }

  return {
    sidebarCollapsed,
    currentMenu,
    globalLoading,
    toggleSidebar,
    setCurrentMenu,
    setGlobalLoading
  }
})
