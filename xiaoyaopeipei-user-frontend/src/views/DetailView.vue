<template>
  <div class="detail-view">
    <!-- 头部 -->
    <AppHeader title="方案详情" />

    <!-- 内容区域 -->
    <div class="content-container" v-if="sku">
      <!-- 图片轮播 -->
      <div class="image-carousel">
        <div class="carousel-track">
          <img
            v-for="(image, index) in sku.images"
            :key="index"
            :src="image"
            :alt="`${sku.name} ${index + 1}`"
            class="carousel-image"
          />
        </div>
        <div class="carousel-indicators">
          <span
            v-for="(_, index) in sku.images"
            :key="index"
            class="indicator"
            :class="{ active: currentImageIndex === index }"
          ></span>
        </div>
      </div>

      <!-- 基本信息 -->
      <div class="product-basic">
        <div class="product-header">
          <h1 class="product-name">{{ sku.name }}</h1>
          <span class="product-type-badge">{{ deviceTypeLabel }}</span>
        </div>

        <div class="product-price">¥{{ sku.price.toLocaleString() }} <span class="price-suffix">到手价</span></div>

        <!-- AI推荐理由 -->
        <div class="ai-reason-card">
          <div class="ai-reason-header">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M8 0C3.58172 0 0 3.58172 0 8C0 12.4183 3.58172 16 8 16C12.4183 16 16 12.4183 16 8C16 3.58172 12.4183 0 8 0ZM8.8 12H7.2V10.4H8.8V12ZM8.8 8.8H7.2V4H8.8V8.8Z" fill="var(--color-primary)"/>
            </svg>
            <span>AI推荐理由</span>
          </div>
          <p class="ai-reason-text">{{ sku.aiReason }}</p>
        </div>
      </div>

      <!-- 详细配置 -->
      <div class="specs-section">
        <h2 class="section-title">📋 详细配置</h2>
        <div class="specs-table">
          <div class="spec-row" v-for="(value, key) in displaySpecs" :key="key">
            <span class="spec-label">{{ getSpecLabel(key) }}</span>
            <span class="spec-value">{{ value }}</span>
          </div>
        </div>
      </div>

      <!-- 标签 -->
      <div class="tags-section" v-if="tags.length > 0">
        <h2 class="section-title">🏷️ 标签</h2>
        <div class="tags-list">
          <span v-for="tag in tags" :key="tag" class="tag">{{ tag }}</span>
        </div>
      </div>

      <!-- 品牌信息 -->
      <div class="brand-section">
        <div class="brand-info">
          <span class="brand-label">品牌</span>
          <span class="brand-name">{{ sku.brand }}</span>
        </div>
        <div class="match-score">
          <span class="score-label">匹配度</span>
          <div class="score-bar">
            <div class="score-fill" :style="{ width: `${sku.matchScore}%` }"></div>
          </div>
          <span class="score-value">{{ sku.matchScore }}%</span>
        </div>
      </div>
    </div>

    <!-- 底部操作栏 -->
    <div class="bottom-action" v-if="sku">
      <button class="confirm-button" @click="handleConfirm">
        我要这个
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { AppHeader } from '@/components'
import type { Sku } from '@/types'
import { DEVICE_TYPE_LABELS } from '@/types'

const router = useRouter()
const route = useRoute()

// SKU信息
const sku = ref<Sku | null>(null)
const currentImageIndex = ref(0)

// 设备类型标签
const deviceTypeLabel = computed(() => {
  if (!sku.value) return ''
  return DEVICE_TYPE_LABELS[sku.value.deviceType] || sku.value.deviceType
})

// 显示的规格参数
const displaySpecs = computed(() => {
  if (!sku.value) return {}
  return sku.value.specs
})

// 获取规格标签
const getSpecLabel = (key: string): string => {
  const labels: Record<string, string> = {
    cpu: '处理器',
    gpu: '显卡',
    ram: '内存',
    storage: '存储',
    screen: '屏幕',
    weight: '重量',
    battery: '续航',
    motherboard: '主板',
    powerSupply: '电源',
    case: '机箱',
  }
  return labels[key] || key
}

// 标签列表
const tags = computed(() => {
  if (!sku.value) return []
  const tags: string[] = []

  // 根据设备类型添加标签
  if (sku.value.deviceType === 'laptop') tags.push('笔记本')
  else if (sku.value.deviceType === 'desktop') tags.push('台式机')
  else if (sku.value.deviceType === 'aio') tags.push('一体机')

  // 根据配置添加标签
  if (sku.value.specs.gpu?.toLowerCase().includes('rtx')) {
    tags.push('独显', '高性能')
  }
  if (sku.value.specs.screen?.toLowerCase().includes('165hz') ||
      sku.value.specs.screen?.toLowerCase().includes('144hz')) {
    tags.push('高刷屏')
  }
  if (sku.value.specs.ram?.includes('16')) {
    tags.push('大内存')
  }
  if (sku.value.specs.cpu?.includes('i7') || sku.value.specs.cpu?.includes('R7')) {
    tags.push('高性能')
  }

  return [...new Set(tags)]
})

// 确认选择
const handleConfirm = () => {
  if (sku.value) {
    sessionStorage.setItem('selectedSku', JSON.stringify(sku.value))
    router.push('/contact')
  }
}

// 初始化
onMounted(() => {
  // 从路由参数或 sessionStorage 获取 SKU
  const stored = sessionStorage.getItem('selectedSku')
  if (stored) {
    sku.value = JSON.parse(stored)
  } else {
    // 如果没有，返回推荐页面
    router.push('/recommend')
  }
})
</script>

<style lang="less" scoped>
.detail-view {
  min-height: 100vh;
  background: var(--color-bg-secondary);
  padding-bottom: 80px;
}

.content-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 76px var(--spacing-lg) var(--spacing-lg);
  animation: fadeIn 0.4s ease-out;
}

// 图片轮播
.image-carousel {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 10;
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: var(--color-bg-tertiary);
  margin-bottom: var(--spacing-lg);
  box-shadow: var(--shadow-md);
}

.carousel-track {
  display: flex;
  width: 100%;
  height: 100%;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;

  &::-webkit-scrollbar {
    display: none;
  }
}

.carousel-image {
  flex-shrink: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  scroll-snap-align: start;
}

.carousel-indicators {
  position: absolute;
  bottom: var(--spacing-md);
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: var(--spacing-xs);
}

.indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  transition: all var(--transition-fast);

  &.active {
    width: 20px;
    border-radius: var(--radius-full);
    background: white;
  }
}

// 基本信息
.product-basic {
  margin-bottom: var(--spacing-xl);
}

.product-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.product-name {
  flex: 1;
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0;
}

.product-type-badge {
  padding: var(--spacing-xs) var(--spacing-md);
  background: var(--color-primary-light);
  color: var(--color-primary);
  font-size: var(--font-size-xs);
  font-weight: 600;
  border-radius: var(--radius-sm);
}

.product-price {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--color-primary);
  font-family: var(--font-family-number);
  margin-bottom: var(--spacing-lg);

  .price-suffix {
    font-size: var(--font-size-sm);
    font-weight: 500;
    color: var(--color-text-secondary);
    margin-left: var(--spacing-xs);
  }
}

// AI推荐理由
.ai-reason-card {
  padding: var(--spacing-lg);
  background: linear-gradient(135deg, var(--color-primary-lighter) 0%, var(--color-primary-light) 100%);
  border-radius: var(--radius-md);
  border-left: 3px solid var(--color-primary);
  box-shadow: var(--shadow-sm);
}

.ai-reason-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-sm);
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-primary);
}

.ai-reason-text {
  font-size: var(--font-size-base);
  color: var(--color-text-primary);
  line-height: 1.6;
  margin: 0;
}

// 详细配置
.specs-section {
  margin-bottom: var(--spacing-xl);
}

.section-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}

.specs-table {
  background: var(--color-bg-primary);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.spec-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  border-bottom: 1px solid var(--color-border-light);

  &:last-child {
    border-bottom: none;
  }

  &:nth-child(odd) {
    background: var(--color-bg-secondary);
  }
}

.spec-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-weight: 500;
}

.spec-value {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  text-align: right;
  max-width: 55%;
}

// 标签
.tags-section {
  margin-bottom: var(--spacing-xl);
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.tag {
  padding: var(--spacing-xs) var(--spacing-md);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-weight: 500;
  transition: all var(--transition-fast);

  &:hover {
    border-color: var(--color-primary);
    color: var(--color-primary);
  }
}

// 品牌信息
.brand-section {
  background: var(--color-bg-primary);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--spacing-lg);
}

.brand-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.brand-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.brand-name {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
}

.match-score {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.score-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.score-bar {
  width: 80px;
  height: 8px;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.score-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-primary-hover) 100%);
  border-radius: var(--radius-full);
  transition: width 1s ease-out;
}

.score-value {
  font-size: var(--font-size-lg);
  font-weight: 700;
  color: var(--color-primary);
  font-family: var(--font-family-number);
}

// 底部操作栏
.bottom-action {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: var(--spacing-md) var(--spacing-lg);
  background: var(--color-bg-primary);
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.04);
  z-index: var(--z-sticky);
}

.confirm-button {
  width: 100%;
  max-width: 600px;
  height: 52px;
  margin: 0 auto;
  display: block;
  background: var(--color-primary);
  color: white;
  font-size: var(--font-size-lg);
  font-weight: 600;
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);

  &:hover {
    background: var(--color-primary-hover);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }

  &:active {
    transform: scale(0.98);
  }
}

@media (max-width: 768px) {
  .content-container {
    padding: 70px var(--spacing-md) var(--spacing-md);
  }

  .product-price {
    font-size: var(--font-size-2xl);
  }

  .brand-section {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
