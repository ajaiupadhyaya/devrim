import { useQuery } from '@tanstack/react-query'
import { analyticsService } from '@/services/analytics'
import { Users, UserCheck, MessageSquare, CheckCircle, TrendingUp, Activity } from 'lucide-react'

const Dashboard = () => {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ['dashboard-metrics'],
    queryFn: analyticsService.getDashboard,
  })

  if (isLoading) {
    return (
      <div className="p-8">
        <div className="text-center">Loading...</div>
      </div>
    )
  }

  const stats = [
    {
      label: 'Total Prospects',
      value: metrics?.total_prospects || 0,
      icon: Users,
      color: 'bg-blue-500',
    },
    {
      label: 'Contacted',
      value: metrics?.contacted || 0,
      icon: MessageSquare,
      color: 'bg-purple-500',
    },
    {
      label: 'Connected',
      value: metrics?.connected || 0,
      icon: UserCheck,
      color: 'bg-green-500',
    },
    {
      label: 'Qualified',
      value: metrics?.qualified || 0,
      icon: CheckCircle,
      color: 'bg-yellow-500',
    },
  ]

  const progressPercent = metrics ? (metrics.daily_activity_count / metrics.daily_limit) * 100 : 0

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Welcome back! Here's an overview of your outreach campaign.
        </p>
      </div>

      {/* Daily Activity */}
      <div className="mb-8 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Today's Activity</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {metrics?.daily_activity_count || 0} / {metrics?.daily_limit || 20} outreach activities
            </p>
          </div>
          <Activity className="w-8 h-8 text-primary-500" />
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
          <div
            className={`h-3 rounded-full transition-all ${
              progressPercent >= 100 ? 'bg-red-500' : 'bg-primary-500'
            }`}
            style={{ width: `${Math.min(progressPercent, 100)}%` }}
          />
        </div>
        {progressPercent >= 100 && (
          <p className="mt-2 text-sm text-red-600 dark:text-red-400">
            You've reached your daily limit. Consider taking a break.
          </p>
        )}
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <div
              key={stat.label}
              className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6"
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
              <div>
                <p className="text-3xl font-bold text-gray-900 dark:text-white">{stat.value}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{stat.label}</p>
              </div>
            </div>
          )
        })}
      </div>

      {/* Connection Rate */}
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Connection Acceptance Rate
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Percentage of accepted connection requests
            </p>
          </div>
          <TrendingUp className="w-8 h-8 text-green-500" />
        </div>
        <div className="flex items-baseline">
          <span className="text-4xl font-bold text-gray-900 dark:text-white">
            {metrics?.connection_acceptance_rate || 0}%
          </span>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
