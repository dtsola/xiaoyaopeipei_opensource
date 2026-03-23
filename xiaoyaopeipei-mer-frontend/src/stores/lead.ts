/**
 * 小遥配配 B端 - 线索状态管理
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Lead, LeadDetail, LeadListParams } from '@/types'
import * as leadApi from '@/api/lead'

export const useLeadStore = defineStore('lead', () => {
  // 状态
  const leadList = ref<Lead[]>([])
  const currentLead = ref<LeadDetail | null>(null)
  const total = ref(0)
  const loading = ref(false)

  // 获取列表
  async function fetchList(params: LeadListParams) {
    loading.value = true
    try {
      const res = await leadApi.getLeadList(params)
      leadList.value = res.data.data.items
      total.value = res.data.data.total
      return res.data.data
    } finally {
      loading.value = false
    }
  }

  // 获取详情
  async function fetchDetail(id: string | number) {
    loading.value = true
    try {
      const res = await leadApi.getLeadDetail(id)
      currentLead.value = res.data.data
      return res.data.data
    } finally {
      loading.value = false
    }
  }

  // 更新状态
  async function updateStatus(id: string | number, status: string) {
    await leadApi.updateLeadStatus(id, status)
  }

  // 添加备注
  async function addNote(id: string | number, content: string) {
    await leadApi.addLeadNote(id, content)
  }

  return {
    leadList,
    currentLead,
    total,
    loading,
    fetchList,
    fetchDetail,
    updateStatus,
    addNote
  }
})
