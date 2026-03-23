/**
 * 线索模块API
 * 对接后端C端线索接口
 */

import { post } from '@/utils/request'
import type { SubmitLeadRequest, SubmitLeadResponse } from '@/types'

/**
 * 提交客户线索
 * POST /api/user/lead/submit
 */
export async function submitLead(req: SubmitLeadRequest): Promise<SubmitLeadResponse> {
  const res = await post<any>('/lead/submit', {
    session_id: req.sessionId,
    shop_id: req.shopId,
    sku_id: req.skuId,
    phone: req.phone,
    wechat: req.wechat,
    remark: req.remark,
  })

  // res 是 AxiosResponse<ApiResponse>, res.data 是 ApiResponse, 真正数据在 res.data.data
  const data = res.data.data || {}

  // 数据格式转换：后端 snake_case → 前端 camelCase
  const shopInfo = data.shop_info || {}
  return {
    leadId: data.lead_id || '',
    shopInfo: {
      id: shopInfo.id || '',
      shopName: shopInfo.shop_name || '',
      phone: shopInfo.phone || '',
      address: shopInfo.address || '',
      businessHours: shopInfo.business_hours || '',
      qrcodeUrl: shopInfo.qrcode_url || '',
    },
  }
}
