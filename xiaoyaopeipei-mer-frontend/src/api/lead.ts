/**
 * 线索管理模块 API
 */

import { get, post, put } from '@/utils/request'
import type { Lead, LeadDetail, LeadListParams, Note, ConversationMessagesResponse } from '@/types'

/**
 * 获取线索列表
 */
export function getLeadList(params: LeadListParams) {
  return get<{
    items: Lead[]
    total: number
    page: number
    limit: number
    pages: number
  }>('/leads', params)
}

/**
 * 获取线索详情
 */
export function getLeadDetail(id: string | number) {
  return get<LeadDetail>(`/leads/${id}`)
}

/**
 * 修改线索状态
 */
export function updateLeadStatus(id: string | number, status: string) {
  return put(`/leads/${id}/status`, { status })
}

/**
 * 添加跟进备注
 */
export function addLeadNote(id: string | number, content: string) {
  return post(`/leads/${id}/notes`, { content })
}

/**
 * 获取跟进记录
 */
export function getLeadNotes(id: string | number) {
  return get<Note[]>(`/leads/${id}/notes`)
}

/**
 * 获取线索统计
 */
export function getLeadSummary() {
  return get<{
    total: number
    pending_count: number
    contacted_count: number
    closed_count: number
    abandoned_count: number
  }>('/leads/stats/summary')
}

/**
 * 获取线索的对话消息列表
 */
export function getLeadMessages(id: string | number) {
  return get<ConversationMessagesResponse>(`/leads/${id}/messages`)
}
