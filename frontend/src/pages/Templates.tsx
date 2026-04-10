import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { templatesService } from '@/services/templates'
import { Plus, Trash2, Copy } from 'lucide-react'
import toast from 'react-hot-toast'
import CreateTemplateModal from '@/components/templates/CreateTemplateModal'

const Templates = () => {
  const [selectedCategory, setSelectedCategory] = useState<string>('all')
  const [showAddModal, setShowAddModal] = useState(false)
  const queryClient = useQueryClient()

  const { data: templates, isLoading } = useQuery({
    queryKey: ['templates', selectedCategory],
    queryFn: () => templatesService.getAll(selectedCategory === 'all' ? undefined : selectedCategory),
  })

  const deleteMutation = useMutation({
    mutationFn: (id: number) => templatesService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['templates'] })
      toast.success('Template deleted')
    },
  })

  const categories = [
    { value: 'all', label: 'All Templates' },
    { value: 'linkedin_connection', label: 'LinkedIn Connection' },
    { value: 'linkedin_followup', label: 'LinkedIn Follow-up' },
    { value: 'email_initial', label: 'Email Initial' },
    { value: 'email_followup', label: 'Email Follow-up' },
  ]

  const handleCopy = (content: string) => {
    navigator.clipboard.writeText(content)
    toast.success('Template copied to clipboard')
  }

  const handleDelete = (id: number, title: string) => {
    if (confirm(`Delete template "${title}"?`)) {
      deleteMutation.mutate(id)
    }
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Templates</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              Manage your message templates with smart variables
            </p>
          </div>
          <button
            onClick={() => setShowAddModal(true)}
            className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            <Plus className="w-4 h-4" />
            New Template
          </button>
        </div>

        {/* Category Filter */}
        <div className="flex gap-2 overflow-x-auto pb-2">
          {categories.map((category) => (
            <button
              key={category.value}
              onClick={() => setSelectedCategory(category.value)}
              className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-colors ${
                selectedCategory === category.value
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              {category.label}
            </button>
          ))}
        </div>
      </div>

      {/* Templates Grid */}
      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-gray-600 dark:text-gray-400">Loading templates...</p>
        </div>
      ) : templates && templates.length > 0 ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {templates.map((template) => (
            <div
              key={template.id}
              className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6"
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    {template.title}
                  </h3>
                  {template.category && (
                    <span className="inline-block mt-1 px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded">
                      {template.category.replace('_', ' ')}
                    </span>
                  )}
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleCopy(template.content)}
                    className="p-2 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                  >
                    <Copy className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(template.id, template.title)}
                    className="p-2 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>

              <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 mb-4">
                <p className="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                  {template.content}
                </p>
              </div>

              <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
                <span>Used {template.times_used} times</span>
                <span>{template.content.length} characters</span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
          <p className="text-gray-600 dark:text-gray-400">
            No templates yet. Create your first template to get started!
          </p>
        </div>
      )}

      {/* Info Box */}
      <div className="mt-8 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 dark:text-blue-200 mb-2">
          Available Variables
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2 text-sm text-blue-800 dark:text-blue-300">
          <span>{'{first_name}'}</span>
          <span>{'{last_name}'}</span>
          <span>{'{full_name}'}</span>
          <span>{'{company}'}</span>
          <span>{'{position}'}</span>
          <span>{'{sector}'}</span>
          <span>{'{my_name}'}</span>
          <span>{'{my_company}'}</span>
          <span>{'{custom_note}'}</span>
        </div>
      </div>

      {/* Modal */}
      {showAddModal && <CreateTemplateModal onClose={() => setShowAddModal(false)} />}
    </div>
  )
}

export default Templates
