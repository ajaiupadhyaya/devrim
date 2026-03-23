import api from './api'
import { DashboardMetrics } from '@/types'

export const analyticsService = {
  getDashboard: async (): Promise<DashboardMetrics> => {
    const response = await api.get('/api/analytics/dashboard')
    return response.data
  },

  getActivityStats: async (days: number = 30) => {
    const response = await api.get('/api/analytics/activity-stats', {
      params: { days },
    })
    return response.data
  },

  getPipelineStats: async () => {
    const response = await api.get('/api/analytics/pipeline-stats')
    return response.data
  },
}
