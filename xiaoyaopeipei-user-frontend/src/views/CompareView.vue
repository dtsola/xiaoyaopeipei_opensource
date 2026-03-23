<template>
  <div class="compare-view">
    <!-- 头部 -->
    <AppHeader title="方案对比" />

    <!-- 内容区域 -->
    <div class="content-container">
      <div class="compare-table-wrapper" v-if="compareSkus.length > 0">
        <table class="compare-table">
          <!-- 表头 -->
          <thead>
            <tr>
              <th class="row-header">对比项目</th>
              <th v-for="sku in compareSkus" :key="sku.skuId" class="product-column">
                <div class="product-header-cell">
                  <img :src="sku.images[0]" :alt="sku.name" class="product-thumb" />
                  <div class="product-name">{{ sku.name }}</div>
                  <div class="product-price">¥{{ sku.price.toLocaleString() }}</div>
                </div>
              </th>
            </tr>
          </thead>

          <!-- 表体 -->
          <tbody>
            <tr v-for="(row, rowIndex) in compareRows" :key="rowIndex">
              <td class="row-header">{{ row.label }}</td>
              <td v-for="sku in compareSkus" :key="sku.skuId" class="compare-cell">
                {{ getCellValue(sku, row.key) }}
              </td>
            </tr>

            <!-- 操作行 -->
            <tr class="action-row">
              <td class="row-header"></td>
              <td v-for="sku in compareSkus" :key="sku.skuId">
                <button class="select-button" @click="handleSelect(sku)">
                  选择这个
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state">
        <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
          <rect x="10" y="20" width="25" height="45" rx="4" stroke="var(--color-border-medium)" stroke-width="2"/>
          <rect x="30" y="15" width="25" height="50" rx="4" stroke="var(--color-border-medium)" stroke-width="2"/>
          <rect x="50" y="25" width="20" height="35" rx="4" stroke="var(--color-border-medium)" stroke-width="2"/>
        </svg>
        <p class="empty-text">暂无对比方案</p>
        <button class="back-button" @click="handleBack">返回推荐</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { AppHeader } from '@/components'
import type { Sku } from '@/types'

const router = useRouter()

// 对比方案列表
const compareSkus = ref<Sku[]>([])

// 对比行配置
const compareRows = [
  { label: '价格', key: 'price' },
  { label: '品牌', key: 'brand' },
  { label: '处理器', key: 'cpu', specKey: true },
  { label: '显卡', key: 'gpu', specKey: true },
  { label: '内存', key: 'ram', specKey: true },
  { label: '存储', key: 'storage', specKey: true },
  { label: '屏幕', key: 'screen', specKey: true },
  { label: '重量', key: 'weight', specKey: true },
  { label: '续航', key: 'battery', specKey: true },
  { label: '匹配度', key: 'matchScore', isScore: true },
]

// 获取单元格值
const getCellValue = (sku: Sku, key: string): string => {
  const rowConfig = compareRows.find(r => r.key === key)

  if (rowConfig?.specKey) {
    return sku.specs[key as keyof typeof sku.specs] || '-'
  }

  if (rowConfig?.isScore) {
    return `${sku.matchScore}%`
  }

  if (key === 'price') {
    return `¥${sku.price.toLocaleString()}`
  }

  return String((sku as any)[key] || '-')
}

// 选择方案
const handleSelect = (sku: Sku) => {
  sessionStorage.setItem('selectedSku', JSON.stringify(sku))
  router.push('/contact')
}

// 返回推荐页
const handleBack = () => {
  router.back()
}

// 初始化
onMounted(() => {
  // 从 sessionStorage 获取对比数据
  const stored = sessionStorage.getItem('compareSkus')
  if (stored) {
    compareSkus.value = JSON.parse(stored)
  }
})
</script>

<style lang="less" scoped>
.compare-view {
  min-height: 100vh;
  background: var(--color-bg-secondary);
}

.content-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 76px var(--spacing-lg) var(--spacing-xl);
  animation: fadeIn 0.4s ease-out;
}

// 对比表格包装器
.compare-table-wrapper {
  background: var(--color-bg-primary);
  border-radius: var(--radius-lg);
  overflow-x: auto;
  box-shadow: var(--shadow-md);
  -webkit-overflow-scrolling: touch;

  &::-webkit-scrollbar {
    height: 4px;
  }

  &::-webkit-scrollbar-thumb {
    background: var(--color-border-medium);
    border-radius: var(--radius-full);
  }
}

// 对比表格
.compare-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 600px;
}

thead {
  background: linear-gradient(135deg, var(--color-primary-lighter) 0%, var(--color-primary-light) 100%);
}

th,
td {
  padding: var(--spacing-md);
  text-align: center;
  border-bottom: 1px solid var(--color-border-light);
}

.row-header {
  text-align: left;
  font-weight: 600;
  color: var(--color-text-secondary);
  background: var(--color-bg-secondary);
  position: sticky;
  left: 0;
  z-index: 10;
  min-width: 80px;
}

.product-column {
  min-width: 160px;
}

.product-header-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
}

.product-thumb {
  width: 80px;
  height: 60px;
  object-fit: cover;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}

.product-name {
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-primary);
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-price {
  font-size: var(--font-size-lg);
  font-weight: 700;
  color: var(--color-primary);
  font-family: var(--font-family-number);
}

.compare-cell {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  font-weight: 500;

  // 价格高亮
  &:nth-child(2):has-text('¥') {
    color: var(--color-primary);
    font-weight: 600;
  }
}

// 斑马纹
tbody tr:nth-child(even) {
  background: var(--color-bg-tertiary);
}

// 操作行
.action-row {
  background: var(--color-bg-secondary);

  td {
    border-bottom: none;
    padding: var(--spacing-lg) var(--spacing-md);
  }
}

.select-button {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-primary);
  color: white;
  font-size: var(--font-size-sm);
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

.back-button {
  margin-top: var(--spacing-lg);
  padding: var(--spacing-md) var(--spacing-xl);
  background: var(--color-primary);
  color: white;
  font-size: var(--font-size-base);
  font-weight: 600;
  border-radius: var(--radius-md);
  border: none;
  cursor: pointer;
  transition: all var(--transition-fast);

  &:hover {
    background: var(--color-primary-hover);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
}

// 差异高亮
.compare-cell {
  position: relative;

  // 最低价格高亮
  .price-lowest {
    color: var(--color-success);
    font-weight: 700;
  }

  // 最高匹配度高亮
  .score-highest {
    color: var(--color-primary);
    font-weight: 700;
  }
}

@media (max-width: 768px) {
  .content-container {
    padding: 70px var(--spacing-sm) var(--spacing-lg);
  }

  th,
  td {
    padding: var(--spacing-sm);
    font-size: var(--font-size-xs);
  }

  .row-header {
    min-width: 60px;
    font-size: var(--font-size-xs);
  }

  .product-column {
    min-width: 120px;
  }

  .product-thumb {
    width: 60px;
    height: 45px;
  }

  .product-name {
    font-size: var(--font-size-xs);
  }

  .product-price {
    font-size: var(--font-size-base);
  }
}
</style>
