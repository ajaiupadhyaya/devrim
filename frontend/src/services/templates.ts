import api from './api'
import { Template } from '@/types'

export const templatesService = {
  getAll: async (category?: string): Promise<Template[]> => {
    const params = category ? { category } : {}
    const response = await api.get('/api/templates', { params })
    return response.data
  },

  getById: async (id: number): Promise<Template> => {
    const response = await api.get(`/api/templates/${id}`)
    return response.data
  },

  create: async (data: { title: string; category?: string; content: string }): Promise<Template> => {
    const response = await api.post('/api/templates', data)
    return response.data
  },

  update: async (id: number, data: Partial<Template>): Promise<Template> => {
    const response = await api.put(`/api/templates/${id}`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/templates/${id}`)
  },

  compose: async (templateId: number, prospectId: number, customNote?: string) => {
    const response = await api.post('/api/templates/compose', {
      template_id: templateId,
      prospect_id: prospectId,
      custom_note: customNote,
    })
    return response.data
  },
}
