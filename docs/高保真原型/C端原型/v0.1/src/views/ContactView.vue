<template>
  <div class="contact-view">
    <!-- 头部 -->
    <AppHeader title="留下联系方式" />

    <!-- 内容区域 -->
    <div class="content-container">
      <!-- 选中的方案摘要 -->
      <div v-if="selectedSku" class="selected-summary">
        <div class="summary-title">您选择的方案</div>
        <div class="summary-content">
          <img :src="selectedSku.images[0]" :alt="selectedSku.name" class="summary-image" />
          <div class="summary-info">
            <div class="summary-name">{{ selectedSku.name }}</div>
            <div class="summary-price">¥{{ selectedSku.price.toLocaleString() }}</div>
          </div>
        </div>
      </div>

      <!-- 表单区域 -->
      <div class="form-container">
        <a-form
          ref="formRef"
          :model="formData"
          :rules="formRules"
          layout="vertical"
          @finish="handleSubmit"
        >
          <!-- 手机号 -->
          <a-form-item label="📱 手机号" name="phone" required>
            <a-input
              v-model:value="formData.phone"
              placeholder="请输入手机号"
              size="large"
              :maxlength="11"
              @input="handlePhoneInput"
            >
              <template #prefix>
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M4 2H12C13.1046 2 14 2.89543 14 4V12C14 13.1046 13.1046 14 12 14H4C2.89543 14 2 13.1046 2 12V4C2 2.89543 2.89543 2 4 2Z" stroke="currentColor" stroke-width="1.5"/>
                  <path d="M2 5H14" stroke="currentColor" stroke-width="1.5"/>
                </svg>
              </template>
            </a-input>
          </a-form-item>

          <!-- 微信号 -->
          <a-form-item label="💬 微信号（选填）" name="wechat">
            <a-input
              v-model:value="formData.wechat"
              placeholder="请输入微信号"
              size="large"
            >
              <template #prefix>
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M8 2C4.68629 2 2 4.23858 2 6C2 7.31016 2.91659 8.43558 4.32678 9.12098L3.5 12L6.31189 10.2785C6.84104 10.4234 7.40502 10.5 8 10.5C11.3137 10.5 14 8.26142 14 6C14 3.73858 11.3137 1.5 8 1.5V2Z" stroke="currentColor" stroke-width="1.5"/>
                </svg>
              </template>
            </a-input>
          </a-form-item>

          <!-- 备注 -->
          <a-form-item label="📝 备注（选填）" name="remark">
            <a-textarea
              v-model:value="formData.remark"
              placeholder="有什么想对老板说的吗？"
              :rows="4"
              :maxlength="200"
              show-count
            />
          </a-form-item>

          <!-- 隐私协议 -->
          <a-form-item name="agreedToPrivacy">
            <a-checkbox v-model:checked="formData.agreedToPrivacy" class="privacy-checkbox">
              我已阅读并同意
              <a href="#" class="privacy-link">《隐私协议》</a>
            </a-checkbox>
          </a-form-item>

          <!-- 提交按钮 -->
          <a-form-item>
            <a-button
              type="primary"
              html-type="submit"
              size="large"
              :loading="submitting"
              block
              class="submit-button"
            >
              提交
            </a-button>
          </a-form-item>
        </a-form>
      </div>

      <!-- 温馨提示 -->
      <div class="tips-card">
        <div class="tips-icon">💡</div>
        <div class="tips-content">
          <div class="tips-title">温馨提示</div>
          <div class="tips-text">老板会在1小时内联系您，请保持手机畅通</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import type { FormInstance } from 'ant-design-vue'
import { AppHeader } from '@/components'
import { mockApi } from '@/api'
import type { Sku, ContactForm, FormErrors } from '@/types'

const router = useRouter()

// 选中的SKU
const selectedSku = ref<Sku | null>(null)

// 表单引用
const formRef = ref<FormInstance>()

// 表单数据
const formData = reactive<ContactForm>({
  phone: '',
  wechat: '',
  remark: '',
  agreedToPrivacy: false,
})

// 提交状态
const submitting = ref(false)

// 表单验证规则
const formRules = {
  phone: [
    { required: true, message: '请输入手机号' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号' },
  ],
  agreedToPrivacy: [
    {
      validator: (_rule: unknown, value: boolean) => {
        if (!value) {
          return Promise.reject('请阅读并同意隐私协议')
        }
        return Promise.resolve()
      },
      trigger: 'change',
    },
  ],
}

// 手机号输入处理（添加空格格式化）
const handlePhoneInput = () => {
  // 移除所有非数字字符
  formData.phone = formData.phone.replace(/\D/g, '')
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
  } catch (error) {
    console.log('表单验证失败:', error)
    return
  }

  if (!selectedSku.value) {
    message.error('请先选择方案')
    return
  }

  submitting.value = true

  try {
    // 调用提交API
    const response = await mockApi.submitLead({
      sessionId: 'mock-session-id',
      shopId: '1234567890123456789',
      skuId: selectedSku.value.skuId,
      phone: formData.phone,
      wechat: formData.wechat || undefined,
      remark: formData.remark || undefined,
    })

    // 保存提交信息
    sessionStorage.setItem('submitResult', JSON.stringify({
      leadId: response.leadId,
      shopInfo: response.shopInfo,
      formData: formData,
      selectedSku: selectedSku.value,
    }))

    // 显示成功消息
    message.success('提交成功！')

    // 跳转到成功页面
    setTimeout(() => {
      router.push('/success')
    }, 500)
  } catch (error) {
    console.error('提交失败:', error)
    message.error('提交失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

// 初始化
onMounted(() => {
  // 从 sessionStorage 获取选中的SKU
  const stored = sessionStorage.getItem('selectedSku')
  if (stored) {
    selectedSku.value = JSON.parse(stored)
  } else {
    // 如果没有选中的SKU，返回推荐页面
    router.push('/recommend')
  }
})
</script>

<style lang="less" scoped>
.contact-view {
  min-height: 100vh;
  background: var(--color-bg-secondary);
}

.content-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 76px var(--spacing-lg) var(--spacing-xl);
  animation: fadeIn 0.4s ease-out;
}

// 选中方案摘要
.selected-summary {
  background: var(--color-bg-primary);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
}

.summary-title {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-weight: 500;
  margin-bottom: var(--spacing-md);
}

.summary-content {
  display: flex;
  gap: var(--spacing-md);
}

.summary-image {
  width: 80px;
  height: 60px;
  object-fit: cover;
  border-radius: var(--radius-md);
  flex-shrink: 0;
}

.summary-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.summary-name {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xs);
}

.summary-price {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--color-primary);
  font-family: var(--font-family-number);
}

// 表单区域
.form-container {
  background: var(--color-bg-primary);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  margin-bottom: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
}

:deep(.ant-form-item) {
  margin-bottom: var(--spacing-lg);
}

:deep(.ant-form-item-label > label) {
  font-weight: 600;
  color: var(--color-text-primary);
}

:deep(.ant-input),
:deep(.ant-input-textarea) {
  border-radius: var(--radius-md);
  border-color: var(--color-border-light);

  &:hover {
    border-color: var(--color-primary-light);
  }

  &:focus {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 2px var(--color-primary-lighter);
  }
}

:deep(.ant-input-prefix) {
  color: var(--color-text-tertiary);
  margin-right: var(--spacing-sm);
}

.privacy-checkbox {
  font-size: var(--font-size-sm);

  :deep(.ant-checkbox-checked .ant-checkbox-inner) {
    background-color: var(--color-primary);
    border-color: var(--color-primary);
  }
}

.privacy-link {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 500;

  &:hover {
    color: var(--color-primary-hover);
    text-decoration: underline;
  }
}

.submit-button {
  height: 52px;
  font-size: var(--font-size-lg);
  font-weight: 600;
  border-radius: var(--radius-md);
  background: var(--color-primary);
  border-color: var(--color-primary);
  margin-top: var(--spacing-md);

  &:hover:not(:disabled) {
    background: var(--color-primary-hover);
    border-color: var(--color-primary-hover);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }

  &:active:not(:disabled) {
    transform: scale(0.98);
  }
}

// 温馨提示
.tips-card {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-radius: var(--radius-lg);
  border-left: 3px solid #f59e0b;
}

.tips-icon {
  font-size: var(--font-size-2xl);
  flex-shrink: 0;
}

.tips-content {
  flex: 1;
}

.tips-title {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: #92400e;
  margin-bottom: var(--spacing-xs);
}

.tips-text {
  font-size: var(--font-size-sm);
  color: #b45309;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .content-container {
    padding: 70px var(--spacing-md) var(--spacing-lg);
  }

  .form-container {
    padding: var(--spacing-lg);
  }
}
</style>
