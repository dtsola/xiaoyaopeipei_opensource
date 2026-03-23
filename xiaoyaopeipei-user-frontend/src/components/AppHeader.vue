<template>
  <header class="app-header" :class="{ 'has-shadow': hasShadow }">
    <div class="header-content">
      <!-- 返回按钮 -->
      <button v-if="showBack" class="back-button" @click="handleBack">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12.5 15L8.5 10L12.5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>

      <!-- 标题 -->
      <h1 class="header-title">
        <span>{{ title }}</span>
      </h1>

      <!-- 右侧操作区 -->
      <div class="header-actions">
        <slot name="actions"></slot>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

interface Props {
  title?: string
  showBack?: boolean
  hasShadow?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: '小遥配配',
  showBack: false,
  hasShadow: false,
})

const router = useRouter()
const route = useRoute()

// 根据路由自动决定是否显示返回按钮
const showBackComputed = computed(() => {
  if (props.showBack) return true
  return route.path !== '/' && route.name !== 'Chat'
})

const handleBack = () => {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/')
  }
}
</script>

<style lang="less" scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: var(--z-sticky);
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
  transition: all var(--transition-base);

  &.has-shadow {
    box-shadow: var(--shadow-glass);
  }
}

.header-content {
  display: flex;
  align-items: center;
  height: 56px;
  padding: 0 var(--spacing-lg);
  max-width: 600px;
  margin: 0 auto;
}

.back-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  color: var(--color-text-primary);
  border-radius: var(--radius-full);
  transition: all var(--transition-fast);
  flex-shrink: 0;
  margin-right: var(--spacing-sm);

  &:hover {
    background: var(--gradient-primary-subtle);
    color: var(--color-primary);
  }

  &:active {
    transform: scale(0.95);
  }
}

.header-title {
  flex: 1;
  font-size: var(--font-size-lg);
  font-weight: 600;
  background: var(--gradient-price);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.header-logo {
  width: 48px;
  height: 48px;
  object-fit: contain;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex-shrink: 0;
  margin-left: auto;

  &:empty {
    display: none;
  }
}

// 调整布局以平衡返回按钮和标题
:deep(.back-button) ~ .header-title {
  padding-left: 36px;
}

:deep(.header-actions:not(:empty)) ~ .header-title {
  padding-right: 36px;
}
</style>
