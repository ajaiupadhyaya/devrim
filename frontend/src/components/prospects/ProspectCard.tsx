import { Prospect } from '@/types'
import { ExternalLink, Mail, Copy, Trash2, Edit, Check } from 'lucide-react'
import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { prospectsService } from '@/services/prospects'
import toast from 'react-hot-toast'

interface ProspectCardProps {
  prospect: Prospect
}

const ProspectCard = ({ prospect }: ProspectCardProps) => {
  const queryClient = useQueryClient()
  const [isEditing, setIsEditing] = useState(false)

  const updateMutation = useMutation({
    mutationFn: (data: { status: string }) => prospectsService.update(prospect.id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['prospects'] })
      toast.success('Prospect updated')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: () => prospectsService.delete(prospect.id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['prospects'] })
      toast.success('Prospect deleted')
    },
  })

  const statusColors: Record<string, string> = {
    new: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    contacted: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
    connected: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    replied: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    qualified: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200',
    unqualified: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200',
    dead: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
  }

  const handleCopyMessage = () => {
    const message = `Hi ${prospect.first_name || prospect.full_name}, I noticed you work at ${prospect.company_name || 'your company'}. I'd love to connect!`
    navigator.clipboard.writeText(message)
    toast.success('Message copied to clipboard')
  }

  const handleStatusChange = (newStatus: string) => {
    updateMutation.mutate({ status: newStatus })
  }

  const handleDelete = () => {
    if (confirm('Are you sure you want to delete this prospect?')) {
      deleteMutation.mutate()
    }
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 hover:shadow-lg transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            {prospect.full_name}
          </h3>
          {prospect.position && (
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {prospect.position} @ {prospect.company_name || 'Unknown Company'}
            </p>
          )}
        </div>
      </div>

      {/* Status Badge */}
      <div className="mb-4">
        <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${statusColors[prospect.status]}`}>
          {prospect.status.charAt(0).toUpperCase() + prospect.status.slice(1)}
        </span>
      </div>

      {/* Contact Info */}
      <div className="space-y-2 mb-4">
        {prospect.email && (
          <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
            <Mail className="w-4 h-4" />
            <span className="truncate">{prospect.email}</span>
            {prospect.email_verified && (
              <Check className="w-4 h-4 text-green-500" />
            )}
          </div>
        )}
        {prospect.sector && (
          <div className="flex items-center gap-2">
            <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-xs rounded text-gray-700 dark:text-gray-300">
              {prospect.sector}
            </span>
          </div>
        )}
      </div>

      {/* Actions */}
      <div className="flex flex-wrap gap-2">
        {prospect.linkedin_url && (
          <button
            onClick={() => window.open(prospect.linkedin_url!, '_blank')}
            className="flex items-center gap-1 px-3 py-1.5 text-xs bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded hover:bg-blue-100 dark:hover:bg-blue-900/40 transition-colors"
          >
            <ExternalLink className="w-3 h-3" />
            LinkedIn
          </button>
        )}
        <button
          onClick={handleCopyMessage}
          className="flex items-center gap-1 px-3 py-1.5 text-xs bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 rounded hover:bg-green-100 dark:hover:bg-green-900/40 transition-colors"
        >
          <Copy className="w-3 h-3" />
          Copy Message
        </button>
        <button
          onClick={handleDelete}
          className="flex items-center gap-1 px-3 py-1.5 text-xs bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded hover:bg-red-100 dark:hover:bg-red-900/40 transition-colors"
        >
          <Trash2 className="w-3 h-3" />
          Delete
        </button>
      </div>

      {/* Status Changer */}
      <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
        <select
          value={prospect.status}
          onChange={(e) => handleStatusChange(e.target.value)}
          className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500"
        >
          <option value="new">New</option>
          <option value="contacted">Contacted</option>
          <option value="connected">Connected</option>
          <option value="replied">Replied</option>
          <option value="qualified">Qualified</option>
          <option value="unqualified">Unqualified</option>
          <option value="dead">Dead</option>
        </select>
      </div>
    </div>
  )
}

export default ProspectCard
