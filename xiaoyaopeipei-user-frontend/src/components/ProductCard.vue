<template>
  <div class="product-card" @click="$emit('click', sku)">
    <!-- 图片区域 -->
    <div class="product-image">
      <img :src="sku.images[0]" :alt="sku.name" loading="lazy" />
      <div class="product-type-badge">{{ sku.deviceType === 'laptop' ? '笔记本' : sku.deviceType === 'desktop' ? '台式机' : '一体机' }}</div>
    </div>

    <!-- 信息区域 -->
    <div class="product-info">
      <!-- 名称和价格 -->
      <div class="product-header">
        <h3 class="product-name">{{ sku.name }}</h3>
        <div class="product-price">¥{{ sku.price.toLocaleString() }}</div>
      </div>

      <!-- 核心配置 -->
      <div class="product-specs">
        <div class="spec-item">
          <span class="spec-label">处理器</span>
          <span class="spec-value">{{ sku.specs.cpu }}</span>
        </div>
        <div v-if="sku.specs.gpu" class="spec-item">
          <span class="spec-label">显卡</span>
          <span class="spec-value">{{ sku.specs.gpu }}</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">内存</span>
          <span class="spec-value">{{ sku.specs.ram }}</span>
        </div>
        <div class="spec-item">
          <span class="spec-label">存储</span>
          <span class="spec-value">{{ sku.specs.storage }}</span>
        </div>
        <div v-if="sku.specs.screen" class="spec-item">
          <span class="spec-label">屏幕</span>
          <span class="spec-value">{{ sku.specs.screen }}</span>
        </div>
      </div>

      <!-- AI推荐理由 -->
      <div class="ai-reason">
        <div class="ai-reason-header">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M7 0C3.13401 0 0 3.13401 0 7C0 10.866 3.13401 14 7 14C10.866 14 14 10.866 14 7C14 3.13401 10.866 0 7 0ZM7.7 10.5H6.3V9.1H7.7V10.5ZM7.7 7.7H6.3V3.5H7.7V7.7Z" fill="var(--color-primary)"/>
          </svg>
          <span>AI推荐理由</span>
        </div>
        <p class="ai-reason-text">{{ sku.aiReason }}</p>
      </div>

      <!-- 操作按钮 -->
      <button class="select-button" @click.stop="$emit('select', sku)">
        选择这个
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Sku } from '@/types'

interface Props {
  sku: Sku
}

defineProps<Props>()
defineEmits<{
  click: [sku: Sku]
  select: [sku: Sku]
}>()
</script>

<style lang="less" scoped>
.product-card {
  background: var(--color-bg-elevated);
  backdrop-filter: blur(10px);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-glass);
  border: 1px solid var(--color-border-glass);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;

  &:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-card-glow);
    background: rgba(255, 255, 255, 0.95);
  }
}

.product-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: var(--color-bg-secondary);

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  }

  &:hover img {
    transform: scale(1.05);
  }
}

.product-type-badge {
  position: absolute;
  top: var(--spacing-md);
  left: var(--spacing-md);
  padding: var(--spacing-xs) var(--spacing-md);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  color: var(--color-text-secondary);
  font-size: var(--font-size-xs);
  font-weight: 500;
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-sm);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.product-info {
  padding: var(--spacing-lg);
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.product-name {
  flex: 1;
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
  line-height: 1.4;
}

.product-price {
  font-size: 28px;
  font-weight: 700;
  font-family: var(--font-family-number);
  flex-shrink: 0;
  background: var(--gradient-price);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 2px 4px rgba(255, 107, 53, 0.2));
}

.product-specs {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--gradient-primary-subtle);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-primary);
}

.spec-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: var(--font-size-sm);
}

.spec-label {
  color: var(--color-text-secondary);
  font-weight: 500;
}

.spec-value {
  color: var(--color-text-primary);
  text-align: right;
  max-width: 60%;
}

// AI推荐理由 - 增强版
.ai-reason {
  position: relative;
  padding: var(--spacing-md);
  background: var(--gradient-reason);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-primary);
  overflow: hidden;
  margin-bottom: var(--spacing-lg);

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: var(--gradient-primary);
  }

  &::after {
    content: '✨';
    position: absolute;
    top: 8px;
    right: 12px;
    font-size: 18px;
    opacity: 0.15;
  }
}

.ai-reason-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-sm);
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-primary);
  position: relative;
  z-index: 1;
}

.ai-reason-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  line-height: 1.6;
  margin: 0;
  position: relative;
  z-index: 1;
}

// 选择按钮 - 光效扫过动画
.select-button {
  width: 100%;
  padding: 14px 24px;
  background: var(--gradient-primary);
  color: var(--color-text-inverse);
  font-size: 16px;
  font-weight: 600;
  border-radius: var(--radius-md);
  border: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(
      45deg,
      transparent 30%,
      rgba(255, 255, 255, 0.3) 50%,
      transparent 70%
    );
    transform: translateX(-100%) rotate(45deg);
    transition: transform 0.6s;
  }

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-primary-hover);

    &::before {
      transform: translateX(100%) rotate(45deg);
    }
  }

  &:active {
    transform: scale(0.98);
  }
}

@media (max-width: 768px) {
  .product-image {
    height: 160px;
  }

  .product-price {
    font-size: 24px;
  }

  .select-button {
    padding: 12px 20px;
    font-size: 15px;
  }
}
</style>
