/**
 * 类型定义文件
 * 小遥配配 - C端原型
 */

// ==================== 基础类型 ====================

/** 设备类型 */
export type DeviceType = 'desktop' | 'laptop' | 'aio'

/** 设备类型中文映射 */
export const DEVICE_TYPE_LABELS: Record<DeviceType, string> = {
  desktop: '台式机',
  laptop: '笔记本',
  aio: '一体机',
}

/** 用途类型 */
export type UsageType = 'office' | 'game' | 'design' | 'study' | 'programming'

/** 对话状态 */
export type ConversationStatus = 'active' | 'completed' | 'abandoned'

/** 线索状态 */
export type LeadStatus = 'pending' | 'contacted' | 'closed' | 'abandoned'

// ==================== 消息类型 ====================

/** 消息角色 */
export type MessageRole = 'user' | 'assistant'

/** 聊天消息 */
export interface ChatMessage {
  id: string
  role: MessageRole
  content: string
  timestamp: number
  quickReplies?: string[]
  isLoading?: boolean
}

// ==================== 需求信息 ====================

/** 用户需求信息 */
export interface UserNeeds {
  budget: string
  deviceType: string
  usage: string
  requirements?: string
  brand?: string
  portable?: string
}

// ==================== SKU配置相关 ====================

/** 配置参数 */
export interface Specs {
  cpu: string
  gpu?: string
  ram: string
  storage: string
  screen?: string
  weight?: string
  battery?: string
  motherboard?: string
  powerSupply?: string
  case?: string
}

/** SKU配置 */
export interface Sku {
  skuId: string
  name: string
  deviceType: DeviceType
  brand: string
  price: number
  specs: Specs
  images: string[]
  aiReason: string
  matchScore: number
}

// ==================== 店铺信息 ====================

/** 店铺信息 */
export interface ShopInfo {
  id: string
  shopName: string
  phone: string
  address: string
  businessHours: string
  qrcodeUrl?: string
}

// ==================== 线索相关 ====================

/** 提交线索请求 */
export interface SubmitLeadRequest {
  sessionId: string
  shopId: string
  skuId: string
  phone: string
  wechat?: string
  remark?: string
}

/** 提交线索响应 */
export interface SubmitLeadResponse {
  leadId: string
  shopInfo: ShopInfo
}

// ==================== 对话相关 ====================

/** 发送消息请求 */
export interface SendMessageRequest {
  sessionId: string
  shopId: string
  message: string
}

/** 发送消息响应 */
export interface SendMessageResponse {
  sessionId: string
  aiResponse: string
  extractedInfo: UserNeeds
  isComplete: boolean
  nextAction: 'ask' | 'recommend'
  quickReplies: string[]
}

/** 获取推荐请求 */
export interface GetRecommendRequest {
  sessionId: string
  shopId: string
  needs: UserNeeds
}

/** 获取推荐响应 */
export interface GetRecommendResponse {
  recommendations: Sku[]
}

// ==================== 路由相关 ====================

/** 路由元信息 */
export interface RouteMetaCustom {
  title?: string
  showBack?: boolean
  keepAlive?: boolean
}

// ==================== 表单相关 ====================

/** 联系方式表单 */
export interface ContactForm {
  phone: string
  wechat: string
  remark: string
  agreedToPrivacy: boolean
}

/** 表单验证错误 */
export interface FormErrors {
  phone?: string
  wechat?: string
  privacy?: string
}

// ==================== 应用状态 ====================

/** 应用全局状态 */
export interface AppState {
  sessionId: string
  shopId: string
  currentRoute: string
  needs: UserNeeds | null
  selectedSku: Sku | null
  chatHistory: ChatMessage[]
  recommendations: Sku[]
}

// ==================== UI相关 ====================

/** 快捷回复按钮配置 */
export interface QuickReplyButton {
  text: string
  icon?: string
  action: () => void
}

/** 方案卡片配置 */
export interface RecommendationCardConfig {
  sku: Sku
  onSelect: (sku: Sku) => void
  onViewDetail: (sku: Sku) => void
}
