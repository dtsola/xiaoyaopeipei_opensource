/**
 * 店铺管理 Composable
 * 处理URL参数中的shop_id和店铺信息
 */
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { sessionManager } from '@/utils/request'
import { getShopInfo, type ShopInfo } from '@/api'

const shopInfo = ref<ShopInfo | null>(null)
const isLoading = ref(false)
const error = ref<string | null>(null)

export function useShop() {
  const route = useRoute()

  /**
   * 从URL参数获取shop_id
   */
  const getShopIdFromUrl = (): string | null => {
    // 优先从URL参数获取
    const shopParam = route.query.shop as string
    if (shopParam) {
      return shopParam
    }
    return null
  }

  /**
   * 初始化店铺信息
   */
  const initShop = async () => {
    // 先尝试从sessionStorage获取
    let shopId = sessionManager.getShopId()

    // 如果没有，从URL参数获取
    if (!shopId) {
      shopId = getShopIdFromUrl()
    }

    if (!shopId) {
      error.value = '缺少店铺参数，请检查链接是否正确'
      return false
    }

    // 保存shop_id到session
    sessionManager.setShopId(shopId)

    // 如果已有店铺信息，直接返回
    if (shopInfo.value && shopInfo.value.id === shopId) {
      return true
    }

    // 加载店铺信息
    try {
      isLoading.value = true
      error.value = null
      const response = await getShopInfo(shopId)
      shopInfo.value = response
      return true
    } catch (err: any) {
      error.value = err.message || '加载店铺信息失败'
      console.error('加载店铺信息失败:', err)
      return false
    } finally {
      isLoading.value = false
    }
  }

  /**
   * 清除店铺信息
   */
  const clearShop = () => {
    shopInfo.value = null
    error.value = null
  }

  // 计算属性
  const hasShopInfo = computed(() => !!shopInfo.value)
  const shopName = computed(() => shopInfo.value?.shopName || '')
  const shopPhone = computed(() => shopInfo.value?.phone || '')
  const shopAddress = computed(() => shopInfo.value?.address || '')
  const shopBusinessHours = computed(() => shopInfo.value?.businessHours || '')

  return {
    // 状态
    shopInfo,
    isLoading,
    error,
    // 计算属性
    hasShopInfo,
    shopName,
    shopPhone,
    shopAddress,
    shopBusinessHours,
    // 方法
    getShopIdFromUrl,
    initShop,
    clearShop,
  }
}
