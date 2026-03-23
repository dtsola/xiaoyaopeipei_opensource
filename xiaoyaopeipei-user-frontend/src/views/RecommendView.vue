<template>
  <div class="recommend-view">
    <!-- 头部 -->
    <AppHeader title="为您推荐" />

    <!-- 内容区域 -->
    <div class="content-container">
      <!-- 需求摘要卡片 -->
      <div class="needs-summary">
        <div class="summary-header">
          <span class="summary-title">您的需求</span>
        </div>
        <div class="summary-tags">
          <div class="summary-tag">
            <DollarOutlined class="tag-icon" />
            <span class="tag-label">预算</span>
            <span class="tag-value">{{ userNeeds?.budget || '5000-8000元' }}</span>
          </div>
          <div class="summary-tag">
            <LaptopOutlined class="tag-icon" />
            <span class="tag-value">{{ deviceTypeLabel }}</span>
          </div>
          <div class="summary-tag" v-if="userNeeds?.usage">
            <ControlOutlined class="tag-icon" />
            <span class="tag-value">{{ usageLabel }}</span>
          </div>
        </div>
      </div>

      <!-- 推荐标题 -->
      <div class="recommend-title">
        为您精选{{ recommendations.length }}个方案 🎉
      </div>

      <!-- 推荐方案列表 -->
      <div class="recommend-list">
        <ProductCard
          v-for="sku in recommendations"
          :key="sku.skuId"
          :sku="sku"
          @click="handleViewDetail"
          @select="handleSelect"
        />
      </div>

      <!-- 空状态 -->
      <div v-if="recommendations.length === 0" class="empty-state">
        <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
          <circle cx="32" cy="32" r="28" stroke="var(--color-border-medium)" stroke-width="2"/>
          <path d="M32 20V32L40 40" stroke="var(--color-text-tertiary)" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <p class="empty-text">暂无推荐方案</p>
        <button class="retry-button" @click="handleRetry">重新选择</button>
      </div>
    </div>

    <!-- 底部操作栏 -->
    <div class="bottom-actions" v-if="recommendations.length > 0">
      <button class="action-button secondary" @click="handleRetry">
        不满意？重新选择
      </button>
      <button class="action-button primary" @click="handleCompare">
        对比方案
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { AppHeader, ProductCard } from '@/components'
import { DollarOutlined, LaptopOutlined, ControlOutlined } from '@ant-design/icons-vue'
import type { Sku, UserNeeds } from '@/types'
import { DEVICE_TYPE_LABELS } from '@/types'
import { sessionManager } from '@/utils/request'

const router = useRouter()

// 推荐方案
const recommendations = ref<Sku[]>([])
// 用户需求
const userNeeds = ref<Partial<UserNeeds> | null>(null)

// 设备类型标签
const deviceTypeLabel = computed(() => {
  if (!userNeeds.value?.deviceType) return '笔记本'
  return DEVICE_TYPE_LABELS[userNeeds.value.deviceType as keyof typeof DEVICE_TYPE_LABELS] || userNeeds.value.deviceType
})

// 用途标签
const usageLabel = computed(() => {
  const usageMap: Record<string, string> = {
    'office': '办公',
    'game': '游戏',
    'design': '设计',
    'study': '学习',
    'programming': '编程',
  }
  return usageMap[userNeeds.value?.usage || ''] || userNeeds.value?.usage || '日常使用'
})

// 查看详情
const handleViewDetail = (sku: Sku) => {
  sessionStorage.setItem('selectedSku', JSON.stringify(sku))
  router.push(`/detail/${sku.skuId}`)
}

// 选择方案
const handleSelect = (sku: Sku) => {
  sessionStorage.setItem('selectedSku', JSON.stringify(sku))
  router.push('/contact')
}

// 重新选择
const handleRetry = () => {
  sessionStorage.removeItem('recommendations')
  sessionStorage.removeItem('userNeeds')
  // 保留shop参数
  const shopId = sessionManager.getShopId()
  router.push(shopId ? `/?shop=${shopId}` : '/')
}

// 对比方案
const handleCompare = () => {
  sessionStorage.setItem('compareSkus', JSON.stringify(recommendations.value))
  router.push('/compare')
}

// 初始化
onMounted(() => {
  // 从 sessionStorage 获取数据
  const stored = sessionStorage.getItem('recommendations')
  const storedNeeds = sessionStorage.getItem('userNeeds')

  if (stored) {
    recommendations.value = JSON.parse(stored)
  }

  if (storedNeeds) {
    userNeeds.value = JSON.parse(storedNeeds)
  }
})
</script>

<style lang="less" scoped>
.recommend-view {
  min-height: 100vh;
  background: var(--color-bg-secondary);
  padding-bottom: 80px;
}

.content-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 76px var(--spacing-lg) var(--spacing-lg);
}

// 需求摘要卡片 - 方案二：卡片标签样式
.needs-summary {
  background: var(--color-bg-elevated);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border-light);
  animation: fadeInUp 0.4s ease-out;
}

.summary-header {
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--color-border-light);
}

.summary-title {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--color-text-primary);
}

.summary-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.summary-tag {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  font-weight: 500;
  transition: all var(--transition-fast);

  &:hover {
    background: var(--gradient-primary-subtle);
    color: var(--color-primary);

    .tag-icon {
      color: var(--color-primary);
    }
  }
}

.tag-icon {
  font-size: 14px;
  color: var(--color-text-secondary);
  transition: color var(--transition-fast);
  flex-shrink: 0;
}

.tag-label {
  color: var(--color-text-secondary);
  margin-right: var(--spacing-xs);
}

.tag-value {
  color: var(--color-text-primary);
}

// 推荐标题
.recommend-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-lg);
  text-align: center;
  animation: fadeIn 0.4s ease-out;
}

// 推荐列表
.recommend-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.recommend-list > :deep(.product-card) {
  animation: fadeInUp 0.4s ease-out backwards;

  &:nth-child(1) { animation-delay: 0.1s; }
  &:nth-child(2) { animation-delay: 0.2s; }
  &:nth-child(3) { animation-delay: 0.3s; }
}

// 空状态
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-2xl) var(--spacing-lg);
  text-align: center;
  animation: fadeIn 0.4s ease-out;
}

.empty-text {
  margin-top: var(--spacing-lg);
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
}

.retry-button {
  margin-top: var(--spacing-lg);
  padding: var(--spacing-md) var(--spacing-xl);
  background: var(--color-primary);
  color: white;
  font-size: var(--font-size-base);
  font-weight: 600;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);

  &:hover {
    background: var(--color-primary-hover);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
}

// 底部操作栏
.bottom-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md) var(--spacing-lg);
  background: var(--color-bg-primary);
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.04);
  z-index: var(--z-sticky);
  max-width: 600px;
  margin: 0 auto;
}

.action-button {
  flex: 1;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-base);
  font-weight: 600;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);

  &.secondary {
    background: var(--color-bg-secondary);
    color: var(--color-text-primary);

    &:hover {
      background: var(--color-bg-tertiary);
    }
  }

  &.primary {
    background: var(--color-primary);
    color: white;

    &:hover {
      background: var(--color-primary-hover);
    }
  }

  &:active {
    transform: scale(0.98);
  }
}

@media (max-width: 768px) {
  .content-container {
    padding: 70px var(--spacing-md) var(--spacing-md);
  }

  .bottom-actions {
    padding: var(--spacing-sm) var(--spacing-md);
  }
}
</style>
