<template>
  <div class="sku-list-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <div>
        <h1 class="page-title font-display">SKU配置管理</h1>
        <p class="page-subtitle">管理您的电脑配置方案</p>
      </div>
      <a-button type="primary" size="large" @click="router.push('/sku/add')">
        <template #icon><PlusOutlined /></template>
        添加配置
      </a-button>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-bar card">
      <div class="filter-section">
        <div class="filter-tabs">
          <div
            v-for="tab in deviceTabs"
            :key="tab.key"
            class="filter-tab"
            :class="{ active: activeTab === tab.key }"
            @click="activeTab = tab.key"
          >
            {{ tab.label }}
            <span v-if="tab.count !== undefined" class="tab-count">{{ tab.count }}</span>
          </div>
        </div>

        <div class="filter-controls">
          <a-input-search
            v-model:value="searchKeyword"
            placeholder="搜索配置名称、品牌..."
            style="width: 280px"
            allow-clear
            @search="handleSearch"
          >
            <template #prefix>
              <SearchOutlined />
            </template>
          </a-input-search>

          <a-dropdown>
            <a-button>
              <template #icon><FilterOutlined /></template>
              筛选
              <DownOutlined />
            </a-button>
            <template #overlay>
              <a-menu>
                <a-menu-item @click="filterStatus = ''">
                  全部状态
                </a-menu-item>
                <a-menu-item @click="filterStatus = 'active'">
                  在售
                </a-menu-item>
                <a-menu-item @click="filterStatus = 'inactive'">
                  缺货
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </div>
      </div>
    </div>

    <!-- SKU列表 -->
    <div v-if="filteredSKUs.length > 0" class="sku-grid">
      <div
        v-for="sku in paginatedSKUs"
        :key="sku.id"
        class="sku-card card"
        :class="{ out_of_stock: sku.stock === 0 }"
      >
        <!-- 图片区域 -->
        <div class="sku-image-area">
          <img :src="sku.images[0] || defaultImage" :alt="sku.name" class="sku-image" />
          <div class="sku-badges">
            <a-tag v-if="sku.stock === 0" color="red">缺货</a-tag>
            <a-tag v-else color="green">在售</a-tag>
            <a-tag :color="getDeviceColor(sku.device_type)">{{ sku.device_type }}</a-tag>
          </div>
        </div>

        <!-- 内容区域 -->
        <div class="sku-content">
          <h3 class="sku-name">{{ sku.name }}</h3>

          <!-- 配置参数 -->
          <div class="sku-specs">
            <div class="spec-item" v-if="sku.cpu">
              <span class="spec-label">CPU</span>
              <span class="spec-value">{{ sku.cpu }}</span>
            </div>
            <div class="spec-item" v-if="sku.gpu">
              <span class="spec-label">GPU</span>
              <span class="spec-value">{{ sku.gpu }}</span>
            </div>
            <div class="spec-item">
              <span class="spec-label">内存</span>
              <span class="spec-value">{{ sku.ram }}</span>
            </div>
            <div class="spec-item">
              <span class="spec-label">存储</span>
              <span class="spec-value">{{ sku.storage }}</span>
            </div>
          </div>

          <!-- 标签 -->
          <div class="sku-tags">
            <a-tag v-for="tag in sku.tags" :key="tag" color="blue">{{ tag }}</a-tag>
          </div>

          <!-- 底部信息 -->
          <div class="sku-footer">
            <div class="sku-stats">
              <span class="stat-item">
                <EyeOutlined />
                {{ sku.view_count }}
              </span>
              <span class="stat-item">
                <ShoppingCartOutlined />
                {{ sku.select_count }}
              </span>
              <span class="stat-item" :class="{ low_stock: sku.stock <= 2 && sku.stock > 0 }">
                <InboxOutlined />
                库存: {{ sku.stock }}
              </span>
            </div>

            <div class="sku-price">
              <span class="price-symbol">¥</span>
              <span class="price-value">{{ sku.price.toLocaleString() }}</span>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="sku-actions">
          <a-button type="link" size="small" @click="router.push(`/sku/edit/${sku.id}`)">
            <EditOutlined />
            编辑
          </a-button>
          <a-button type="link" size="small" @click="handleCopy(sku)">
            <CopyOutlined />
            复制
          </a-button>
          <a-popconfirm
            title="确定要删除这个配置吗？"
            ok-text="确定"
            cancel-text="取消"
            @confirm="handleDelete(sku.id)"
          >
            <a-button type="link" size="small" danger>
              <DeleteOutlined />
              删除
            </a-button>
          </a-popconfirm>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <a-empty
      v-else
      description="暂无配置数据"
      :image="Empty.PRESENTED_IMAGE_SIMPLE"
      class="empty-state"
    >
      <a-button type="primary" @click="router.push('/sku/add')">
        添加第一个配置
      </a-button>
    </a-empty>

    <!-- 分页 -->
    <div v-if="filteredSKUs.length > pageSize" class="pagination-wrapper">
      <a-pagination
        v-model:current="currentPage"
        v-model:page-size="pageSize"
        :total="filteredSKUs.length"
        show-size-changer
        show-quick-jumper
        :show-total="(total) => `共 ${total} 个配置`"
        @change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { message, Modal } from 'ant-design-vue'
import { Empty } from 'ant-design-vue'
import {
  PlusOutlined,
  SearchOutlined,
  FilterOutlined,
  DownOutlined,
  EditOutlined,
  CopyOutlined,
  DeleteOutlined,
  EyeOutlined,
  ShoppingCartOutlined,
  InboxOutlined
} from '@ant-design/icons-vue'
import { mockSKUs } from '@/utils/mockData'
import type { SKU } from '@/types'

const router = useRouter()

// 默认图片
const defaultImage = 'https://via.placeholder.com/300x200/e8eaed/8a94a5?text=No+Image'

// 筛选状态
const activeTab = ref<SKU['device_type'] | 'all'>('all')
const filterStatus = ref<'active' | 'inactive' | ''>('')
const searchKeyword = ref('')

// 分页
const currentPage = ref(1)
const pageSize = ref(9)

// 设备类型Tab
const deviceTabs = computed(() => [
  { key: 'all', label: '全部', count: mockSKUs.length },
  { key: 'desktop', label: '台式机', count: mockSKUs.filter(s => s.device_type === 'desktop').length },
  { key: 'laptop', label: '笔记本', count: mockSKUs.filter(s => s.device_type === 'laptop').length },
  { key: 'aio', label: '一体机', count: mockSKUs.filter(s => s.device_type === 'aio').length }
])

// 筛选后的SKU列表
const filteredSKUs = computed(() => {
  let result = [...mockSKUs]

  // 设备类型筛选
  if (activeTab.value !== 'all') {
    result = result.filter(sku => sku.device_type === activeTab.value)
  }

  // 状态筛选
  if (filterStatus.value) {
    result = result.filter(sku => sku.status === filterStatus.value)
  }

  // 搜索筛选
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(sku =>
      sku.name.toLowerCase().includes(keyword) ||
      sku.brand?.toLowerCase().includes(keyword) ||
      sku.model?.toLowerCase().includes(keyword)
    )
  }

  return result
})

// 分页后的SKU列表
const paginatedSKUs = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredSKUs.value.slice(start, end)
})

// 获取设备类型颜色
function getDeviceColor(type: string) {
  const colors: Record<string, string> = {
    '笔记本': 'blue',
    '台式机': 'green',
    '一体机': 'orange'
  }
  return colors[type] || 'default'
}

// 搜索处理
function handleSearch() {
  currentPage.value = 1
}

// 分页处理
function handlePageChange(page: number) {
  currentPage.value = page
  // 滚动到顶部
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 复制配置
function handleCopy(sku: SKU) {
  message.success('已创建配置副本，正在跳转到编辑页面...')
  // 这里可以跳转到编辑页面并预填充数据
  setTimeout(() => {
    router.push(`/sku/add`)
  }, 500)
}

// 删除配置
function handleDelete(id: string) {
  message.success('配置已删除')
  // 这里调用API删除数据
}
</script>

<style scoped>
.sku-list-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ========== 页面头部 ========== */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin-top: 4px;
}

/* ========== 筛选栏 ========== */
.filter-bar {
  padding: 20px;
}

.filter-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.filter-tabs {
  display: flex;
  gap: 8px;
}

.filter-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: var(--radius-full);
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  background: var(--bg-hover);
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.filter-tab:hover {
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.filter-tab.active {
  background: var(--primary-color);
  color: #ffffff;
  border-color: var(--primary-color);
}

.tab-count {
  font-size: 12px;
  padding: 2px 6px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
}

.filter-controls {
  display: flex;
  gap: 12px;
}

/* ========== SKU网格 ========== */
.sku-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.sku-card {
  padding: 0;
  overflow: hidden;
  transition: all var(--transition-base);
  position: relative;
}

.sku-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl);
}

.sku-card.out_of_stock {
  opacity: 0.7;
}

.sku-card.out_of_stock::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.02);
  pointer-events: none;
}

/* 图片区域 */
.sku-image-area {
  position: relative;
  width: 100%;
  height: 180px;
  overflow: hidden;
}

.sku-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-slow);
}

.sku-card:hover .sku-image {
  transform: scale(1.05);
}

.sku-badges {
  position: absolute;
  top: 12px;
  left: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

/* 内容区域 */
.sku-content {
  padding: 16px;
}

.sku-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sku-specs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 12px;
}

.spec-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.spec-label {
  font-size: 11px;
  color: var(--text-tertiary);
  text-transform: uppercase;
}

.spec-value {
  font-size: 13px;
  color: var(--text-primary);
  font-weight: 500;
}

.sku-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 12px;
}

.sku-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 12px;
  border-top: 1px solid var(--border-color-light);
}

.sku-stats {
  display: flex;
  gap: 12px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-tertiary);
}

.stat-item.low_stock {
  color: var(--warning-color);
}

.sku-price {
  display: flex;
  align-items: baseline;
}

.price-symbol {
  font-size: 14px;
  color: var(--danger-color);
  font-weight: 600;
}

.price-value {
  font-size: 20px;
  color: var(--danger-color);
  font-weight: 700;
}

/* 操作按钮 */
.sku-actions {
  display: flex;
  padding: 12px 16px;
  background: var(--bg-hover);
  border-top: 1px solid var(--border-color-light);
  gap: 8px;
}

.sku-actions :deep(.ant-btn-link) {
  padding: 0;
  font-size: 13px;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 20px;
}

/* 空状态 */
.empty-state {
  padding: 60px 20px;
}

/* 响应式 */
@media (max-width: 1400px) {
  .sku-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1024px) {
  .sku-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .filter-section {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-tabs {
    overflow-x: auto;
    padding-bottom: 4px;
  }
}

@media (max-width: 768px) {
  .sku-grid {
    grid-template-columns: 1fr;
  }

  .page-header {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }

  .filter-controls {
    flex-direction: column;
  }

  .filter-controls :deep(.ant-input-search) {
    width: 100% !important;
  }
}
</style>
