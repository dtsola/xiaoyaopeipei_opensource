<template>
  <div class="sku-form-container">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <a-button @click="router.back()" class="back-btn">
          <LeftOutlined />
        </a-button>
        <div>
          <h1 class="page-title font-display">{{ isEdit ? '编辑配置' : '添加配置' }}</h1>
          <p class="page-subtitle">{{ isEdit ? '修改电脑配置信息' : '创建新的电脑配置方案' }}</p>
        </div>
      </div>
      <div class="header-actions">
        <a-button @click="handleCancel">取消</a-button>
        <a-button type="primary" :loading="isSubmitting" @click="handleSubmit">
          <template #icon><SaveOutlined /></template>
          保存配置
        </a-button>
      </div>
    </div>

    <!-- 表单内容 -->
    <a-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      layout="vertical"
      class="sku-form"
    >
      <!-- 设备类型选择 -->
      <div class="form-section card">
        <h2 class="section-title font-display">设备类型</h2>
        <a-form-item name="device_type">
          <a-radio-group v-model:value="formData.device_type" size="large" button-style="solid">
            <a-radio-button value="desktop">
              <DesktopOutlined />
              台式机
            </a-radio-button>
            <a-radio-button value="laptop">
              <LaptopOutlined />
              笔记本
            </a-radio-button>
            <a-radio-button value="aio">
              <OneToOneOutlined />
              一体机
            </a-radio-button>
          </a-radio-group>
        </a-form-item>
      </div>

      <!-- 基本信息 -->
      <div class="form-section card">
        <h2 class="section-title font-display">基本信息</h2>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="配置名称" name="name">
              <a-input
                v-model:value="formData.name"
                size="large"
                placeholder="如：联想拯救者Y7000P"
                allow-clear
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="品牌" name="brand">
              <a-auto-complete
                v-model:value="formData.brand"
                :options="brandOptions"
                size="large"
                placeholder="选择或输入品牌"
                allow-clear
                :filter-option="filterOption"
              />
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16" v-if="formData.device_type !== 'desktop'">
          <a-col :span="12">
            <a-form-item label="型号" name="model">
              <a-input
                v-model:value="formData.model"
                size="large"
                placeholder="如：Y7000P 2023款"
                allow-clear
              />
            </a-form-item>
          </a-col>
        </a-row>
      </div>

      <!-- 硬件配置 -->
      <div class="form-section card">
        <h2 class="section-title font-display">硬件配置</h2>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="处理器（CPU）" name="cpu">
              <a-input
                v-model:value="formData.cpu"
                size="large"
                placeholder="如：i7-12700H"
                allow-clear
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="显卡（GPU）" name="gpu">
              <a-input
                v-model:value="formData.gpu"
                size="large"
                placeholder="如：RTX 4060 8G"
                allow-clear
              />
            </a-form-item>
          </a-col>
        </a-row>

        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="内存（RAM）" name="ram">
              <a-input
                v-model:value="formData.ram"
                size="large"
                placeholder="如：16GB DDR5"
                allow-clear
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item label="存储（Storage）" name="storage">
              <a-input
                v-model:value="formData.storage"
                size="large"
                placeholder="如：512GB SSD"
                allow-clear
              />
            </a-form-item>
          </a-col>
        </a-row>

        <!-- 台式机专属字段 -->
        <template v-if="formData.device_type === 'desktop'">
          <a-divider orientation="left">台式机专属配置</a-divider>
          <a-row :gutter="16">
            <a-col :span="8">
              <a-form-item label="主板" name="motherboard">
                <a-input
                  v-model:value="formData.motherboard"
                  size="large"
                  placeholder="如：B660M"
                  allow-clear
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item label="电源" name="power_supply">
                <a-input
                  v-model:value="formData.power_supply"
                  size="large"
                  placeholder="如：650W 80Plus金牌"
                  allow-clear
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item label="机箱" name="case">
                <a-input
                  v-model:value="formData.case"
                  size="large"
                  placeholder="如：ATX中塔机箱"
                  allow-clear
                />
              </a-form-item>
            </a-col>
          </a-row>
        </template>

        <!-- 笔记本专属字段 -->
        <template v-if="formData.device_type === 'laptop'">
          <a-divider orientation="left">笔记本专属配置</a-divider>
          <a-row :gutter="16">
            <a-col :span="8">
              <a-form-item label="屏幕" name="screen">
                <a-input
                  v-model:value="formData.screen"
                  size="large"
                  placeholder="如：15.6英寸 2.5K 165Hz"
                  allow-clear
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item label="重量" name="weight">
                <a-input
                  v-model:value="formData.weight"
                  size="large"
                  placeholder="如：2.4kg"
                  allow-clear
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item label="续航" name="battery">
                <a-input
                  v-model:value="formData.battery"
                  size="large"
                  placeholder="如：5-6小时"
                  allow-clear
                />
              </a-form-item>
            </a-col>
          </a-row>
        </template>

        <!-- 一体机专属字段 -->
        <template v-if="formData.device_type === 'aio'">
          <a-divider orientation="left">一体机专属配置</a-divider>
          <a-form-item label="屏幕尺寸" name="screen">
            <a-input
              v-model:value="formData.screen"
              size="large"
              placeholder="如：27英寸 4K 触控"
              allow-clear
            />
          </a-form-item>
        </template>
      </div>

      <!-- 价格与库存 -->
      <div class="form-section card">
        <h2 class="section-title font-display">价格与库存</h2>
        <a-row :gutter="16">
          <a-col :span="8">
            <a-form-item label="价格（元）" name="price">
              <a-input-number
                v-model:value="formData.price"
                size="large"
                :min="0"
                :precision="0"
                placeholder="请输入价格"
                style="width: 100%"
              >
                <template #prefix>¥</template>
              </a-input-number>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="库存（台）" name="stock">
              <a-input-number
                v-model:value="formData.stock"
                size="large"
                :min="0"
                :precision="0"
                placeholder="请输入库存数量"
                style="width: 100%"
              />
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item label="库存状态" name="status">
              <a-select v-model:value="formData.status" size="large" placeholder="选择状态">
                <a-select-option value="active">在售</a-select-option>
                <a-select-option value="inactive">缺货</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
      </div>

      <!-- 标签设置 -->
      <div class="form-section card">
        <h2 class="section-title font-display">标签设置</h2>
        <a-form-item label="用途标签" name="usage_tags">
          <a-checkbox-group v-model:value="formData.usage_tags">
            <a-checkbox value="gaming">游戏（gaming）</a-checkbox>
            <a-checkbox value="office">办公（office）</a-checkbox>
            <a-checkbox value="design">设计（design）</a-checkbox>
          </a-checkbox-group>
        </a-form-item>

        <a-form-item label="特性标签" name="feature_tags">
          <a-checkbox-group v-model:value="formData.feature_tags">
            <a-checkbox value="budget">性价比（budget）</a-checkbox>
            <a-checkbox value="brand">品牌（brand）</a-checkbox>
            <a-checkbox value="portable">便携（portable）</a-checkbox>
            <a-checkbox value="high-refresh">高刷屏（high-refresh）</a-checkbox>
            <a-checkbox value="thin-light">轻薄（thin-light）</a-checkbox>
            <a-checkbox value="high_performance">高性能（high-performance）</a-checkbox>
          </a-checkbox-group>
        </a-form-item>
      </div>

      <!-- 配置图片 -->
      <div class="form-section card">
        <h2 class="section-title font-display">配置图片</h2>
        <a-upload
          v-model:file-list="imageList"
          list-type="picture-card"
          :max-count="5"
          :before-upload="beforeUpload"
          @preview="handlePreview"
        >
          <div v-if="imageList.length < 5">
            <PlusOutlined />
            <div style="margin-top: 8px">上传图片</div>
          </div>
        </a-upload>
        <div class="upload-tip">
          支持jpg/png格式，单张图片不超过2MB，最多上传5张
        </div>
      </div>
    </a-form>

    <!-- 图片预览 -->
    <a-modal v-model:open="previewVisible" :footer="null" @cancel="previewVisible = false">
      <img alt="preview" style="width: 100%" :src="previewImage" />
    </a-modal>

    <!-- 取消确认 -->
    <a-modal
      v-model:open="cancelVisible"
      title="确认取消"
      content="您有未保存的修改，确定要放弃吗？"
      centered
      @ok="router.back()"
    >
      <template #footer>
        <a-button @click="cancelVisible = false">继续编辑</a-button>
        <a-button type="primary" danger @click="router.back()">放弃修改</a-button>
      </template>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { message } from 'ant-design-vue'
import type { FormInstance, UploadProps } from 'ant-design-vue'
import {
  LeftOutlined,
  SaveOutlined,
  DesktopOutlined,
  LaptopOutlined,
  OneToOneOutlined,
  PlusOutlined
} from '@ant-design/icons-vue'
import { mockSKUs } from '@/utils/mockData'
import type { SKU, DeviceType } from '@/types'

const router = useRouter()
const route = useRoute()
const formRef = ref<FormInstance>()

// 是否为编辑模式
const isEdit = computed(() => !!route.params.id)

// 是否正在提交
const isSubmitting = ref(false)

// 取消确认
const cancelVisible = ref(false)

// 图片预览
const previewVisible = ref(false)
const previewImage = ref('')

// 图片列表
const imageList = ref<any[]>([])

// 品牌选项
const brandOptions = ref([
  { value: '联想', label: '联想' },
  { value: '华硕', label: '华硕' },
  { value: '惠普', label: '惠普' },
  { value: '戴尔', label: '戴尔' },
  { value: '苹果', label: '苹果' },
  { value: '宏碁', label: '宏碁' },
  { value: '微星', label: '微星' }
])

// 表单数据
const formData = reactive({
  device_type: 'laptop' as DeviceType,
  name: '',
  brand: undefined as string | undefined,
  model: undefined as string | undefined,
  cpu: '',
  gpu: undefined as string | undefined,
  ram: '',
  storage: '',
  motherboard: undefined as string | undefined,
  power_supply: undefined as string | undefined,
  case: undefined as string | undefined,
  screen: undefined as string | undefined,
  weight: undefined as string | undefined,
  battery: undefined as string | undefined,
  price: undefined as number | undefined,
  stock: 0,
  status: 'active' as 'active' | 'inactive',
  usage_tags: [] as string[],
  feature_tags: [] as string[]
})

// 表单验证规则
const formRules = {
  device_type: [{ required: true, message: '请选择设备类型' }],
  name: [
    { required: true, message: '请输入配置名称' },
    { min: 2, max: 100, message: '配置名称长度为2-100个字符' }
  ],
  brand: [{ required: true, message: '请选择或输入品牌' }],
  cpu: [{ required: true, message: '请输入处理器信息' }],
  ram: [{ required: true, message: '请输入内存信息' }],
  storage: [{ required: true, message: '请输入存储信息' }],
  price: [
    { required: true, message: '请输入价格' },
    { type: 'number', min: 0, message: '价格不能为负数' }
  ],
  stock: [
    { required: true, message: '请输入库存数量' },
    { type: 'number', min: 0, message: '库存不能为负数' }
  ],
  status: [{ required: true, message: '请选择库存状态' }]
}

// 品牌搜索过滤
function filterOption(input: string, option: any) {
  return option.value.toLowerCase().includes(input.toLowerCase())
}

// 图片上传前验证
const beforeUpload: UploadProps['beforeUpload'] = (file) => {
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png'
  if (!isJpgOrPng) {
    message.error('只能上传 JPG/PNG 格式的图片')
    return false
  }
  const isLt2M = file.size / 1024 / 1024 < 2
  if (!isLt2M) {
    message.error('图片大小不能超过 2MB')
    return false
  }
  return false // 阻止自动上传
}

// 图片预览
const handlePreview: UploadProps['onPreview'] = (file) => {
  previewImage.value = file.url || file.thumbUrl
  previewVisible.value = true
}

// 处理取消
function handleCancel() {
  cancelVisible.value = true
}

// 提交表单
async function handleSubmit() {
  try {
    await formRef.value?.validate()
    isSubmitting.value = true

    // 合并标签
    const tags = [...formData.usage_tags, ...formData.feature_tags]

    // 合并图片URL
    const images = imageList.value
      .filter(file => file.url || file.response?.url)
      .map(file => file.url || file.response?.url)

    const submitData = {
      ...formData,
      tags,
      images
    }

    console.log('提交数据:', submitData)

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))

    message.success(isEdit.value ? '配置修改成功！' : '配置添加成功！')
    router.push('/sku')
  } catch (error) {
    console.error('表单验证失败:', error)
  } finally {
    isSubmitting.value = false
  }
}

// 加载编辑数据
onMounted(() => {
  if (isEdit.value) {
    const skuId = route.params.id as string
    const sku = mockSKUs.find(s => s.id === skuId)
    if (sku) {
      // 填充表单数据
      Object.assign(formData, {
        device_type: sku.device_type,
        name: sku.name,
        brand: sku.brand,
        model: sku.model,
        cpu: sku.cpu,
        gpu: sku.gpu,
        ram: sku.ram,
        storage: sku.storage,
        motherboard: sku.motherboard,
        power_supply: sku.power_supply,
        case: sku.case,
        screen: sku.screen,
        weight: sku.weight,
        battery: sku.battery,
        price: sku.price,
        stock: sku.stock,
        status: sku.status
      })

      // 分离标签
      const usageTags = ['gaming', 'office', 'design']
      const featureTags = ['budget', 'brand', 'portable', 'high-refresh', 'thin-light', 'high-performance']
      formData.usage_tags = sku.tags.filter(t => usageTags.includes(t))
      formData.feature_tags = sku.tags.filter(t => featureTags.includes(t))

      // 填充图片列表
      imageList.value = sku.images.map((url, index) => ({
        uid: `${index}`,
        name: `image-${index}.jpg`,
        status: 'done',
        url
      }))
    }
  }
})
</script>

<style scoped>
.sku-form-container {
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

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
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

.header-actions {
  display: flex;
  gap: 12px;
}

/* ========== 表单区块 ========== */
.form-section {
  padding: 24px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-color-light);
}

/* ========== 单选按钮组 ========== */
:deep(.ant-radio-group) {
  display: flex;
  gap: 12px;
}

:deep(.ant-radio-button-wrapper) {
  height: 48px;
  padding: 0 24px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  transition: all var(--transition-base);
}

:deep(.ant-radio-button-wrapper:hover) {
  color: var(--primary-color);
  border-color: var(--primary-color);
}

:deep(.ant-radio-button-wrapper-checked) {
  background: var(--primary-color);
  border-color: var(--primary-color);
}

/* ========== 输入框样式 ========== */
:deep(.ant-input),
:deep(.ant-input-number),
:deep(.ant-select-selector) {
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
}

:deep(.ant-input:focus),
:deep(.ant-input-number:focus),
:deep(.ant-select-focused .ant-select-selector) {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
}

:deep(.ant-form-item-label > label) {
  font-weight: 500;
  color: var(--text-secondary);
}

/* ========== 复选框组 ========== */
:deep(.ant-checkbox-group) {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

:deep(.ant-checkbox-wrapper) {
  padding: 8px 16px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  transition: all var(--transition-fast);
}

:deep(.ant-checkbox-wrapper:hover) {
  border-color: var(--primary-color);
  background: var(--primary-lighter);
}

:deep(.ant-checkbox-wrapper-checked) {
  background: var(--primary-lighter);
  border-color: var(--primary-color);
}

/* ========== 上传组件 ========== */
:deep(.ant-upload-select-picture-card) {
  width: 120px;
  height: 120px;
  border-radius: var(--radius-md);
  border: 2px dashed var(--border-color);
  transition: all var(--transition-base);
}

:deep(.ant-upload-select-picture-card:hover) {
  border-color: var(--primary-color);
}

:deep(.ant-upload-list-picture-card-container) {
  width: 120px;
  height: 120px;
}

.upload-tip {
  font-size: 13px;
  color: var(--text-tertiary);
  margin-top: 8px;
}

/* ========== 分割线 ========== */
:deep(.ant-divider) {
  margin: 20px 0;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
}

:deep(.ant-divider-inner-text) {
  padding: 0 12px;
}

/* 响应式 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }

  .header-left {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  :deep(.ant-radio-group) {
    flex-direction: column;
  }

  :deep(.ant-radio-button-wrapper) {
    width: 100%;
  }
}
</style>
