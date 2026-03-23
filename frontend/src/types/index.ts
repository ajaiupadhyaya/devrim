export interface User {
  id: number
  email: string
  full_name: string | null
  company: string | null
  position: string | null
  created_at: string
}

export interface Prospect {
  id: number
  user_id: number
  company_id: number | null
  first_name: string | null
  last_name: string | null
  full_name: string
  position: string | null
  email: string | null
  email_verified: boolean
  linkedin_url: string | null
  sector: string | null
  custom_tags: string | null
  status: ProspectStatus
  last_contacted: string | null
  added_date: string
  notes: string | null
  company_name?: string
}

export type ProspectStatus = 
  | 'new' 
  | 'contacted' 
  | 'connected' 
  | 'replied' 
  | 'qualified' 
  | 'unqualified' 
  | 'dead'

export interface Template {
  id: number
  user_id: number
  title: string
  category: string | null
  content: string
  created_at: string
  updated_at: string | null
  times_used: number
}

export interface Activity {
  id: number
  user_id: number
  prospect_id: number | null
  activity_type: string
  description: string | null
  created_at: string
}

export interface DashboardMetrics {
  total_prospects: number
  new_prospects: number
  contacted: number
  connected: number
  replied: number
  qualified: number
  connection_acceptance_rate: number
  daily_activity_count: number
  daily_limit: number
}

export interface ProspectCreate {
  first_name?: string
  last_name?: string
  full_name: string
  position?: string
  email?: string
  linkedin_url?: string
  sector?: string
  custom_tags?: string
  notes?: string
  company_name?: string
}

export interface ProspectUpdate {
  first_name?: string
  last_name?: string
  full_name?: string
  position?: string
  email?: string
  email_verified?: boolean
  linkedin_url?: string
  sector?: string
  custom_tags?: string
  status?: ProspectStatus
  notes?: string
  last_contacted?: string
}
