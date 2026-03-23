import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { prospectsService } from '@/services/prospects'
import { Plus, Upload, Search } from 'lucide-react'
import ProspectCard from '@/components/prospects/ProspectCard'
import AddProspectModal from '@/components/prospects/AddProspectModal'
import ImportCSVModal from '@/components/prospects/ImportCSVModal'
import toast from 'react-hot-toast'

const Prospects = () => {
  const [selectedStatus, setSelectedStatus] = useState<string>('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [showAddModal, setShowAddModal] = useState(false)
  const [showImportModal, setShowImportModal] = useState(false)
  const queryClient = useQueryClient()

  const { data: prospects, isLoading } = useQuery({
    queryKey: ['prospects', selectedStatus],
    queryFn: () => prospectsService.getAll(selectedStatus === 'all' ? undefined : selectedStatus),
  })

  const statusOptions = [
    { value: 'all', label: 'All' },
    { value: 'new', label: 'New' },
    { value: 'contacted', label: 'Contacted' },
    { value: 'connected', label: 'Connected' },
    { value: 'replied', label: 'Replied' },
    { value: 'qualified', label: 'Qualified' },
  ]

  const filteredProspects = prospects?.filter((prospect) =>
    prospect.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    prospect.position?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    prospect.email?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Prospects</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              Manage your outreach prospects and pipeline
            </p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => setShowImportModal(true)}
              className="flex items-center gap-2 px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            >
              <Upload className="w-4 h-4" />
              Import CSV
            </button>
            <button
              onClick={() => setShowAddModal(true)}
              className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              <Plus className="w-4 h-4" />
              Add Prospect
            </button>
          </div>
        </div>

        {/* Filters */}
        <div className="flex gap-4 items-center">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search prospects..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <div className="flex gap-2">
            {statusOptions.map((option) => (
              <button
                key={option.value}
                onClick={() => setSelectedStatus(option.value)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  selectedStatus === option.value
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Prospects Grid */}
      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-gray-600 dark:text-gray-400">Loading prospects...</p>
        </div>
      ) : filteredProspects && filteredProspects.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProspects.map((prospect) => (
            <ProspectCard key={prospect.id} prospect={prospect} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
          <p className="text-gray-600 dark:text-gray-400">
            {searchTerm ? 'No prospects found matching your search' : 'No prospects yet. Add your first prospect to get started!'}
          </p>
        </div>
      )}

      {/* Modals */}
      {showAddModal && <AddProspectModal onClose={() => setShowAddModal(false)} />}
      {showImportModal && <ImportCSVModal onClose={() => setShowImportModal(false)} />}
    </div>
  )
}

export default Prospects
