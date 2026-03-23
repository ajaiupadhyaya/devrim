import api from './api'
import { Prospect, ProspectCreate, ProspectUpdate } from '@/types'

export const prospectsService = {
  getAll: async (status?: string): Promise<Prospect[]> => {
    const params = status ? { status } : {}
    const response = await api.get('/api/prospects', { params })
    return response.data
  },

  getById: async (id: number): Promise<Prospect> => {
    const response = await api.get(`/api/prospects/${id}`)
    return response.data
  },

  create: async (data: ProspectCreate): Promise<Prospect> => {
    const response = await api.post('/api/prospects', data)
    return response.data
  },

  update: async (id: number, data: ProspectUpdate): Promise<Prospect> => {
    const response = await api.put(`/api/prospects/${id}`, data)
    return response.data
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/api/prospects/${id}`)
  },

  importCSV: async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/api/prospects/import-csv', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  findEmail: async (fullName: string, companyDomain: string) => {
    const response = await api.post('/api/prospects/find-email', {
      full_name: fullName,
      company_domain: companyDomain,
    })
    return response.data
  },
}
