<template>
  <div id="app" class="app-container">
    <!-- 路由视图 -->
    <router-view v-slot="{ Component, route }">
      <transition :name="route.meta.transition || 'fade'" mode="out-in">
        <component :is="Component" :key="route.path" />
      </transition>
    </router-view>

    <!-- 全局加载指示器 -->
    <teleport to="body">
      <div v-if="globalLoading" class="global-loading">
        <div class="loading-spinner"></div>
      </div>
    </teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, provide } from 'vue'

// 全局加载状态
const globalLoading = ref(false)

// 提供给全局使用
provide('globalLoading', {
  show: () => { globalLoading.value = true },
  hide: () => { globalLoading.value = false },
})
</script>

<style lang="less" scoped>
.app-container {
  min-height: 100vh;
  background: #F7F7F8;
  // 页面背景微纹理 - 径向渐变
  background-image:
    radial-gradient(circle at 20% 30%, rgba(255,107,53,0.03) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(59,130,246,0.02) 0%, transparent 50%);
  background-attachment: fixed;
}

// 页面过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition-slow), transform var(--transition-slow);
}

.fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

// 全局加载指示器 - 增强版
.global-loading {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.9);
  z-index: 9999;
  backdrop-filter: blur(8px);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-primary-light);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  box-shadow: var(--shadow-primary-glow);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
