import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { templatesService } from '@/services/templates'
import { X } from 'lucide-react'
import toast from 'react-hot-toast'

interface CreateTemplateModalProps {
  onClose: () => void
}

const CATEGORIES = [
  { value: 'linkedin_connection', label: 'LinkedIn Connection' },
  { value: 'linkedin_followup', label: 'LinkedIn Follow-up' },
  { value: 'email_initial', label: 'Email Initial' },
  { value: 'email_followup', label: 'Email Follow-up' },
]

const CreateTemplateModal = ({ onClose }: CreateTemplateModalProps) => {
  const queryClient = useQueryClient()
  const [formData, setFormData] = useState({
    title: '',
    category: '',
    content: '',
  })

  const mutation = useMutation({
    mutationFn: templatesService.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['templates'] })
      toast.success('Template created successfully')
      onClose()
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create template')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.title.trim()) {
      toast.error('Title is required')
      return
    }
    if (!formData.content.trim()) {
      toast.error('Content is required')
      return
    }
    mutation.mutate({
      title: formData.title,
      category: formData.category || undefined,
      content: formData.content,
    })
  }

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">New Template</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Title *
            </label>
            <input
              type="text"
              name="title"
              required
              value={formData.title}
              onChange={handleChange}
              placeholder="e.g., LinkedIn Connection Request"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Category
            </label>
            <select
              name="category"
              value={formData.category}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500"
            >
              <option value="">Select a category</option>
              {CATEGORIES.map((cat) => (
                <option key={cat.value} value={cat.value}>
                  {cat.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Content *
            </label>
            <textarea
              name="content"
              required
              value={formData.content}
              onChange={handleChange}
              rows={8}
              placeholder="Hi {first_name}, I noticed you work at {company}..."
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 font-mono text-sm"
            />
            <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
              {formData.content.length} characters
            </p>
          </div>

          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-3">
            <p className="text-xs font-medium text-blue-900 dark:text-blue-200 mb-1">
              Available variables:
            </p>
            <p className="text-xs text-blue-800 dark:text-blue-300">
              {'{first_name}'} &nbsp; {'{last_name}'} &nbsp; {'{full_name}'} &nbsp; {'{company}'} &nbsp; {'{position}'} &nbsp; {'{sector}'} &nbsp; {'{my_name}'} &nbsp; {'{my_company}'} &nbsp; {'{custom_note}'}
            </p>
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={mutation.isPending}
              className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {mutation.isPending ? 'Creating...' : 'Create Template'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CreateTemplateModal
