/**
 * 店铺模块API
 * 对接后端C端店铺接口
 */

import { get } from '@/utils/request'
import type { ShopInfo } from '@/types'

/**
 * 获取店铺信息
 * GET /api/user/shop/{shop_id}
 */
export async function getShopInfo(shopId: string): Promise<ShopInfo> {
  const res = await get<any>(`/shop/${shopId}`)

  // res 是 AxiosResponse<ApiResponse>, res.data 是 ApiResponse, 真正数据在 res.data.data
  const data = res.data.data || {}

  // 数据格式转换：后端 snake_case → 前端 camelCase
  return {
    id: data.id || '',
    shopName: data.shop_name || '',
    phone: data.phone || '',
    address: data.address || '',
    businessHours: data.business_hours || '',
    qrcodeUrl: data.qrcode_url || '',
  }
}
