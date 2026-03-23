/**
 * 对话模块API
 * 对接后端C端对话接口
 */

import { get, post } from '@/utils/request'
import type { SendMessageRequest, SendMessageResponse, GetRecommendRequest, GetRecommendResponse } from '@/types'

/**
 * 转换后端提取信息格式（snake_case → camelCase）
 */
function convertExtractedInfo(backendInfo: any): SendMessageResponse['extractedInfo'] {
  return {
    budget: backendInfo.budget,
    deviceType: backendInfo.device_type,
    usage: backendInfo.usage,
    requirements: backendInfo.requirements,
    brand: backendInfo.brand,
    portable: backendInfo.portable,
  }
}

/**
 * 发送消息（AI意图识别）
 * POST /api/user/chat/message
 */
export async function sendMessage(req: SendMessageRequest): Promise<SendMessageResponse> {
  const res = await post<any>('/chat/message', {
    session_id: req.sessionId || undefined, // 首次传空
    shop_id: req.shopId,
    message: req.message,
  })

  // res 是 AxiosResponse<ApiResponse>, res.data 是 ApiResponse, 真正数据在 res.data.data
  const data = res.data.data || {}

  // 数据格式转换：后端 snake_case → 前端 camelCase
  return {
    sessionId: data.session_id,
    aiResponse: data.ai_response || '抱歉，我没能理解您的意思，能再说一遍吗？',
    extractedInfo: convertExtractedInfo(data.extracted_info || {}),
    isComplete: data.is_complete || false,
    nextAction: data.next_action || 'ask',
    quickReplies: data.quick_replies || [],
  }
}

/**
 * 获取推荐方案
 * POST /api/user/chat/recommend
 */
export async function getRecommendations(req: GetRecommendRequest): Promise<GetRecommendResponse> {
  const res = await post<any>('/chat/recommend', {
    session_id: req.sessionId,
    shop_id: req.shopId,
    needs: req.needs,
  })

  const data = res.data.data || {}

  // 数据格式转换：后端 snake_case → 前端 camelCase
  return {
    recommendations: (data.recommendations || []).map((item: any) => ({
      skuId: item.sku_id,
      name: item.name,
      deviceType: item.device_type,
      brand: item.brand,
      price: item.price,
      specs: item.specs,
      images: item.images || [],
      aiReason: item.ai_reason || '',
      matchScore: item.match_score || 0,
    })),
  }
}

/**
 * 获取对话历史
 * GET /api/user/chat/history
 */
export async function getChatHistory(sessionId: string) {
  const res = await get('/chat/history', { session_id: sessionId })

  const data = res.data.data || {}

  // 数据格式转换
  return {
    sessionId: data.session_id,
    messages: (data.messages || []).map((msg: any) => ({
      id: `${msg.created_at}_${msg.role}`,
      role: msg.role,
      content: msg.content,
      timestamp: new Date(msg.created_at).getTime(),
      quickReplies: msg.quick_replies,
    })),
    status: data.status || 'active',
  }
}

/**
 * 获取店铺预算区间建议（根据SKU价格分布动态生成）
 * GET /api/user/shop/{shop_id}/price-ranges
 */
export async function getPriceRanges(shopId: string): Promise<string[]> {
  const res = await get(`/shop/${shopId}/price-ranges`)
  const data = res.data.data || {}
  return data.price_ranges || []
}
