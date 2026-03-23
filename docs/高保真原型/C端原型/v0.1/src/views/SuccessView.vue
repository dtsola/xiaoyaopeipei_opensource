<template>
  <div class="success-view">
    <!-- 成功动画区域 -->
    <div class="success-animation">
      <div class="success-icon-wrapper">
        <svg class="success-icon" viewBox="0 0 64 64" fill="none">
          <circle cx="32" cy="32" r="28" fill="var(--color-primary)" fill-opacity="0.1"/>
          <circle cx="32" cy="32" r="28" stroke="var(--color-primary)" stroke-width="2"/>
          <path class="check-path" d="M20 32L28 40L44 24" stroke="var(--color-primary)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
    </div>

    <!-- 标题 -->
    <h1 class="success-title">提交成功！</h1>

    <!-- 内容区域 -->
    <div class="content-container">
      <!-- 店铺信息卡片 -->
      <div class="shop-info-card">
        <div class="shop-info-title">老板会尽快联系您～</div>

        <div class="shop-info-list">
          <a :href="`tel:${shopInfo.phone}`" class="shop-info-item">
            <div class="info-icon">📞</div>
            <div class="info-content">
              <div class="info-label">店铺电话</div>
              <div class="info-value">{{ shopInfo.phone }}</div>
            </div>
            <svg class="info-arrow" width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M6 3L11 8L6 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </a>

          <div class="shop-info-item" @click="copyWechat">
            <div class="info-icon">💬</div>
            <div class="info-content">
              <div class="info-label">店铺微信</div>
              <div class="info-value">{{ shopInfo.wechat || 'xiaoyao_shop' }}</div>
            </div>
            <svg class="info-arrow" width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M6 3L11 8L6 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>

          <div class="shop-info-item">
            <div class="info-icon">🏪</div>
            <div class="info-content">
              <div class="info-label">店铺地址</div>
              <div class="info-value">{{ shopInfo.address }}</div>
            </div>
          </div>

          <div class="shop-info-item">
            <div class="info-icon">🕐</div>
            <div class="info-content">
              <div class="info-label">营业时间</div>
              <div class="info-value">{{ shopInfo.businessHours }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 您的信息卡片 -->
      <div class="your-info-card" v-if="submitData">
        <div class="info-card-title">您的信息</div>

        <div class="your-info-list">
          <div class="your-info-item">
            <span class="your-info-label">手机号</span>
            <span class="your-info-value">{{ maskPhone(submitData.formData?.phone || '') }}</span>
          </div>
          <div class="your-info-item" v-if="submitData.formData?.wechat">
            <span class="your-info-label">微信号</span>
            <span class="your-info-value">{{ submitData.formData.wechat }}</span>
          </div>
          <div class="your-info-item">
            <span class="your-info-label">选择方案</span>
            <span class="your-info-value">{{ submitData.selectedSku?.name }}</span>
          </div>
          <div class="your-info-item">
            <span class="your-info-label">价格</span>
            <span class="your-info-value your-info-price">¥{{ submitData.selectedSku?.price?.toLocaleString() }}</span>
          </div>
        </div>
      </div>

      <!-- 返回首页按钮 -->
      <button class="back-home-button" @click="handleBackHome">
        返回首页
      </button>

      <!-- 底部提示 -->
      <p class="bottom-tips">
        💡 您也可以直接拨打电话或添加微信咨询
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'

const router = useRouter()

// 店铺信息
const shopInfo = ref({
  phone: '138-1234-5678',
  wechat: 'xiaoyao_shop',
  address: '北京市朝阳区科技路88号数码广场3层',
  businessHours: '9:00 - 21:00',
})

// 提交的数据
const submitData = ref<any>(null)

// 手机号脱敏
const maskPhone = (phone: string): string => {
  if (!phone || phone.length !== 11) return phone
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

// 复制微信号
const copyWechat = () => {
  const wechat = shopInfo.value.wechat
  navigator.clipboard.writeText(wechat).then(() => {
    message.success('微信号已复制')
  }).catch(() => {
    // 降级方案
    const textarea = document.createElement('textarea')
    textarea.value = wechat
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand('copy')
    document.body.removeChild(textarea)
    message.success('微信号已复制')
  })
}

// 返回首页
const handleBackHome = () => {
  // 清除 sessionStorage
  sessionStorage.clear()
  router.push('/')
}

// 初始化
onMounted(() => {
  // 从 sessionStorage 获取提交结果
  const stored = sessionStorage.getItem('submitResult')
  if (stored) {
    submitData.value = JSON.parse(stored)
    if (submitData.value?.shopInfo) {
      shopInfo.value = { ...shopInfo.value, ...submitData.value.shopInfo }
    }
  }
})
</script>

<style lang="less" scoped>
.success-view {
  min-height: 100vh;
  background: var(--color-bg-secondary);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--spacing-2xl) var(--spacing-lg);
}

// 成功动画
.success-animation {
  margin-top: var(--spacing-2xl);
  margin-bottom: var(--spacing-lg);
}

.success-icon-wrapper {
  position: relative;
  width: 80px;
  height: 80px;
}

.success-icon {
  width: 100%;
  height: 100%;
  animation: scaleIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.check-path {
  stroke-dasharray: 50;
  stroke-dashoffset: 50;
  animation: drawCheck 0.4s ease-out 0.3s forwards;
}

@keyframes drawCheck {
  to {
    stroke-dashoffset: 0;
  }
}

@keyframes scaleIn {
  from {
    transform: scale(0);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

// 标题
.success-title {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xl) 0;
  animation: fadeInUp 0.5s ease-out 0.2s backwards;
}

// 内容容器
.content-container {
  width: 100%;
  max-width: 500px;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

// 店铺信息卡片
.shop-info-card {
  background: var(--color-bg-primary);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-md);
  animation: fadeInUp 0.5s ease-out 0.3s backwards;
}

.shop-info-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  text-align: center;
  margin-bottom: var(--spacing-lg);
}

.shop-info-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.shop-info-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
  cursor: pointer;

  &:hover {
    background: var(--color-bg-tertiary);
    transform: translateX(4px);
  }

  &.clickable {
    cursor: pointer;
  }
}

.info-icon {
  font-size: var(--font-size-xl);
  flex-shrink: 0;
}

.info-content {
  flex: 1;
  min-width: 0;
}

.info-label {
  font-size: var(--font-size-xs);
  color: var(--color-text-tertiary);
  margin-bottom: 2px;
}

.info-value {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.info-arrow {
  flex-shrink: 0;
  color: var(--color-text-tertiary);
}

// 您的信息卡片
.your-info-card {
  background: var(--color-bg-primary);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-sm);
  animation: fadeInUp 0.5s ease-out 0.4s backwards;
}

.info-card-title {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--color-border-light);
}

.your-info-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.your-info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.your-info-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.your-info-value {
  font-size: var(--font-size-base);
  color: var(--color-text-primary);
  font-weight: 500;

  &.your-info-price {
    color: var(--color-primary);
    font-weight: 700;
    font-family: var(--font-family-number);
  }
}

// 返回首页按钮
.back-home-button {
  width: 100%;
  height: 52px;
  background: var(--color-primary);
  color: white;
  font-size: var(--font-size-lg);
  font-weight: 600;
  border-radius: var(--radius-md);
  border: none;
  cursor: pointer;
  transition: all var(--transition-fast);
  animation: fadeInUp 0.5s ease-out 0.5s backwards;

  &:hover {
    background: var(--color-primary-hover);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }

  &:active {
    transform: scale(0.98);
  }
}

// 底部提示
.bottom-tips {
  text-align: center;
  font-size: var(--font-size-sm);
  color: var(--color-text-tertiary);
  margin: 0;
  animation: fadeIn 0.5s ease-out 0.6s backwards;
}

@media (max-width: 768px) {
  .success-view {
    padding: var(--spacing-xl) var(--spacing-md);
  }

  .success-title {
    font-size: var(--font-size-2xl);
  }
}
</style>
