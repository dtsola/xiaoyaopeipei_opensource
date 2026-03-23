/**
 * Mock API 服务
 * 模拟后端接口返回数据
 */

import type {
  SendMessageRequest,
  SendMessageResponse,
  GetRecommendRequest,
  GetRecommendResponse,
  SubmitLeadRequest,
  SubmitLeadResponse,
  ShopInfo,
  Sku,
  UserNeeds,
} from '@/types'

// 生成唯一ID
const generateId = (): string => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2)
}

// 延迟模拟网络请求
const delay = (ms: number = 800) => new Promise(resolve => setTimeout(resolve, ms))

// ==================== Mock 数据 ====================

/** Mock 店铺信息 */
const mockShopInfo: ShopInfo = {
  id: '1234567890123456789',
  shopName: '小遥电脑城',
  phone: '138-1234-5678',
  address: '北京市朝阳区科技路88号数码广场3层',
  businessHours: '9:00 - 21:00',
  qrcodeUrl: 'https://via.placeholder.com/200',
}

/** Mock SKU 数据 */
const mockSkus: Sku[] = [
  {
    skuId: '1234567890123456790',
    name: '联想拯救者Y7000P',
    deviceType: 'laptop',
    brand: '联想',
    price: 7499,
    specs: {
      cpu: 'Intel Core i7-12700H (14核20线程)',
      gpu: 'NVIDIA RTX 4060 8GB',
      ram: '16GB DDR5 4800MHz (可扩展至32GB)',
      storage: '512GB PCIe 4.0 SSD',
      screen: '15.6英寸 2.5K (2560×1440) 165Hz',
      weight: '约2.4kg',
      battery: '约5-6小时',
    },
    images: [
      'https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=800&q=80', // laptop on desk
    ],
    aiReason: '这款笔记本搭载RTX 4060显卡，原神可以稳定60帧高画质运行，屏幕是2.5K 165Hz游戏体验非常流畅！💪 性价比很高，强烈推荐！',
    matchScore: 95,
  },
  {
    skuId: '1234567890123456791',
    name: '华硕天选4',
    deviceType: 'laptop',
    brand: '华硕',
    price: 6799,
    specs: {
      cpu: 'AMD Ryzen 7 7735HS (8核16线程)',
      gpu: 'NVIDIA RTX 4050 6GB',
      ram: '16GB DDR5 4800MHz',
      storage: '512GB PCIe 4.0 SSD',
      screen: '15.6英寸 2.5K (2560×1440) 144Hz',
      weight: '约2.3kg',
      battery: '约4-5小时',
    },
    images: [
      'https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800&q=80', // PC laptop setup
    ],
    aiReason: '这款性价比超高！RTX 4050显卡玩原神能稳定60帧高画质，价格比预算便宜200元💰 AMD处理器性能强劲！',
    matchScore: 92,
  },
  {
    skuId: '1234567890123456792',
    name: '惠普暗影精灵9',
    deviceType: 'laptop',
    brand: '惠普',
    price: 6499,
    specs: {
      cpu: 'Intel Core i5-12500H (12核16线程)',
      gpu: 'NVIDIA RTX 4050 6GB',
      ram: '16GB DDR4 3200MHz',
      storage: '512GB PCIe 4.0 SSD',
      screen: '16.1英寸 FHD (1920×1080) 144Hz',
      weight: '约2.5kg',
      battery: '约5小时',
    },
    images: [
      'https://images.unsplash.com/photo-1593640408182-31c70c8268f5?w=800&q=80', // notebook computer
    ],
    aiReason: '这款最便宜！比预算便宜1500元，玩原神完全够用。16.1英寸大屏幕，游戏视野更广。惠普品质有保障👍',
    matchScore: 88,
  },
  {
    skuId: '1234567890123456793',
    name: '联想GeekPro G5000',
    deviceType: 'laptop',
    brand: '联想',
    price: 5999,
    specs: {
      cpu: 'Intel Core i5-13500H (12核16线程)',
      gpu: 'NVIDIA RTX 4050 6GB',
      ram: '16GB DDR5',
      storage: '512GB SSD',
      screen: '15.6英寸 FHD 165Hz',
      weight: '约2.4kg',
      battery: '约5小时',
    },
    images: [
      'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=800&q=80', // workspace laptop
    ],
    aiReason: '超值选择！最新13代i5处理器搭配RTX 4050，性能释放强劲，价格控制在6000以内，性价比之选！',
    matchScore: 85,
  },
]

// ==================== API 接口 ====================

/**
 * 发送消息 (AI意图识别)
 */
export async function sendMessage(req: SendMessageRequest): Promise<SendMessageResponse> {
  await delay(1000)

  // 首次发送，创建sessionId
  const sessionId = req.sessionId || generateId()

  // 模拟AI对话逻辑
  const userMessage = req.message.toLowerCase()
  let aiResponse = ''
  let quickReplies: string[] = []
  let isComplete = false

  // 根据用户输入返回不同回复
  if (userMessage.includes('预算') || userMessage.includes('3000') || userMessage.includes('5000') ||
      userMessage.includes('8000') || userMessage.includes('6000') || userMessage.includes('12000')) {
    aiResponse = '明白了！我记下了您的预算～请问您主要用来做什么呢？办公、游戏、还是设计？'
    quickReplies = ['办公文档', '玩游戏', '设计创作', '编程开发']
  } else if (userMessage.includes('游戏') || userMessage.includes('原神') || userMessage.includes('玩')) {
    aiResponse = '好的！游戏本的话，您需要经常携带吗？还是主要在家用？'
    quickReplies = ['经常携带', '主要在家用', '不确定']
  } else if (userMessage.includes('携带') || userMessage.includes('家用') || userMessage.includes('不')) {
    aiResponse = '了解～最后确认一下，您对品牌有偏好吗？比如联想、华硕、惠普等'
    quickReplies = ['联想', '华硕', '惠普', '没有偏好']
  } else if (userMessage.includes('品牌') || userMessage.includes('联想') || userMessage.includes('华硕') ||
             userMessage.includes('惠普') || userMessage.includes('没有') || userMessage.includes('都可以')) {
    aiResponse = '太好了！我已经了解您的需求，正在为您推荐最合适的配置～'
    isComplete = true
    quickReplies = []
  } else {
    // 默认开场
    aiResponse = '您好！我是小遥，我来帮您选一台合适的电脑～请问您的预算大概是多少呢？'
    quickReplies = ['3000-5000元', '5000-8000元', '8000-12000元', '12000元以上']
  }

  // 模拟提取的需求信息
  const extractedInfo: UserNeeds = {
    budget: userMessage.includes('6000') ? '6000左右' : '5000-8000元',
    deviceType: '笔记本',
    usage: userMessage.includes('游戏') || userMessage.includes('原神') ? '游戏' : '办公',
    requirements: userMessage.includes('原神') ? '玩原神' : '日常使用',
  }

  return {
    sessionId,
    aiResponse,
    extractedInfo,
    isComplete,
    nextAction: isComplete ? 'recommend' : 'ask',
    quickReplies,
  }
}

/**
 * 获取推荐方案
 */
export async function getRecommendations(req: GetRecommendRequest): Promise<GetRecommendResponse> {
  await delay(1200)

  // 根据需求过滤并排序SKU
  let filteredSkus = [...mockSkus]

  // 根据预算筛选
  const budget = parseInt(req.needs.budget.replace(/\D/g, '')) || 8000
  filteredSkus = filteredSkus.filter(sku => sku.price <= budget + 2000)

  // 根据用途排序
  if (req.needs.usage === '游戏') {
    filteredSkus.sort((a, b) => b.matchScore - a.matchScore)
  }

  // 返回Top3
  return {
    recommendations: filteredSkus.slice(0, 3),
  }
}

/**
 * 提交客户线索
 */
export async function submitLead(req: SubmitLeadRequest): Promise<SubmitLeadResponse> {
  await delay(800)

  return {
    leadId: generateId(),
    shopInfo: mockShopInfo,
  }
}

/**
 * 获取店铺信息
 */
export async function getShopInfo(shopId: string): Promise<ShopInfo> {
  await delay(300)
  return mockShopInfo
}

// ==================== 导出 ====================

const mockApi = {
  sendMessage,
  getRecommendations,
  submitLead,
  getShopInfo,
}

export default mockApi
