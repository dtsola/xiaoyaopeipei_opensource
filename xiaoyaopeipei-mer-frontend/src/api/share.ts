/**
 * 分享管理模块 API
 */

import { get, post } from '@/utils/request'
import type { QRCodeResponse, ShareStats } from '@/types'

/**
 * 获取专属二维码
 */
export function getQRCode() {
  return get<QRCodeResponse>('/share/qrcode')
}

/**
 * 刷新二维码
 */
export function refreshQRCode() {
  return post<QRCodeResponse>('/share/qrcode/refresh')
}

/**
 * 生成分享海报
 */
export function generatePoster(templateId: string) {
  return post<{ url: string }>('/share/poster', { template_id: templateId })
}

/**
 * 获取分享统计
 */
export function getShareStats(period: string = 'all') {
  return get<ShareStats>('/share/stats', { period })
}

/**
 * 获取分享统计趋势
 */
export function getShareTrend(days: number = 7) {
  return get('/share/stats/trend', { days })
}
