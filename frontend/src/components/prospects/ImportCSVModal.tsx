import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { prospectsService } from '@/services/prospects'
import { X, Upload, FileText } from 'lucide-react'
import toast from 'react-hot-toast'

interface ImportCSVModalProps {
  onClose: () => void
}

const ImportCSVModal = ({ onClose }: ImportCSVModalProps) => {
  const queryClient = useQueryClient()
  const [file, setFile] = useState<File | null>(null)
  const [dragActive, setDragActive] = useState(false)

  const mutation = useMutation({
    mutationFn: (file: File) => prospectsService.importCSV(file),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['prospects'] })
      toast.success(`Imported ${data.imported} prospects! Skipped: ${data.skipped}`)
      onClose()
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to import CSV')
    },
  })

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0]
      if (droppedFile.name.endsWith('.csv')) {
        setFile(droppedFile)
      } else {
        toast.error('Please upload a CSV file')
      }
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const handleSubmit = () => {
    if (!file) {
      toast.error('Please select a file')
      return
    }
    mutation.mutate(file)
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg max-w-2xl w-full">
        <div className="border-b border-gray-200 dark:border-gray-700 px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">Import CSV</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="p-6 space-y-4">
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
            <h3 className="font-medium text-blue-900 dark:text-blue-200 mb-2">CSV Format</h3>
            <p className="text-sm text-blue-800 dark:text-blue-300 mb-2">
              Your CSV file should have the following columns:
            </p>
            <ul className="text-sm text-blue-800 dark:text-blue-300 list-disc list-inside space-y-1">
              <li><strong>company</strong> - Company name (required)</li>
              <li><strong>name or full_name</strong> - Full name (required)</li>
              <li><strong>sector</strong> - Industry sector (optional)</li>
              <li><strong>desired_role or position</strong> - Job title (optional)</li>
              <li><strong>email</strong> - Email address (optional)</li>
              <li><strong>linkedin_url</strong> - LinkedIn profile URL (optional)</li>
            </ul>
          </div>

          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
              dragActive
                ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                : 'border-gray-300 dark:border-gray-600'
            }`}
          >
            {file ? (
              <div className="flex items-center justify-center gap-3">
                <FileText className="w-8 h-8 text-primary-600 dark:text-primary-400" />
                <div className="text-left">
                  <p className="font-medium text-gray-900 dark:text-white">{file.name}</p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {(file.size / 1024).toFixed(2)} KB
                  </p>
                </div>
                <button
                  onClick={() => setFile(null)}
                  className="ml-4 text-red-600 hover:text-red-700 dark:text-red-400"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            ) : (
              <div>
                <Upload className="w-12 h-12 mx-auto text-gray-400 mb-4" />
                <p className="text-gray-700 dark:text-gray-300 mb-2">
                  Drag and drop your CSV file here
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">or</p>
                <label className="inline-block px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 cursor-pointer transition-colors">
                  Browse Files
                  <input
                    type="file"
                    accept=".csv"
                    onChange={handleFileChange}
                    className="hidden"
                  />
                </label>
              </div>
            )}
          </div>

          <div className="flex gap-3 pt-4">
            <button
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={handleSubmit}
              disabled={!file || mutation.isPending}
              className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {mutation.isPending ? 'Importing...' : 'Import CSV'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ImportCSVModal
