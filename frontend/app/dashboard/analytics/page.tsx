'use client'

import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/lib/api'
import { TrendingUp, TrendingDown, Target, Award, Calendar, Download } from 'lucide-react'
import { motion } from 'framer-motion'
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { format } from 'date-fns'

export default function AnalyticsPage() {
  const { data: analytics } = useQuery({
    queryKey: ['analytics'],
    queryFn: () => apiClient.getAnalytics(),
    refetchInterval: 30000,
  })

  const { data: accounts } = useQuery({
    queryKey: ['accounts'],
    queryFn: () => apiClient.getAccounts(),
  })

  const analyticsData = analytics?.data
  const accountsData = accounts?.data || []

  // Mock data for charts
  const weeklyData = [
    { day: 'Mon', follows: 45, likes: 234, comments: 12, unfollows: 8 },
    { day: 'Tue', follows: 52, likes: 289, comments: 18, unfollows: 10 },
    { day: 'Wed', follows: 48, likes: 267, comments: 15, unfollows: 12 },
    { day: 'Thu', follows: 61, likes: 312, comments: 22, unfollows: 15 },
    { day: 'Fri', follows: 55, likes: 298, comments: 19, unfollows: 11 },
    { day: 'Sat', follows: 38, likes: 189, comments: 10, unfollows: 7 },
    { day: 'Sun', follows: 42, likes: 201, comments: 11, unfollows: 9 },
  ]

  const actionDistribution = [
    { name: 'Follows', value: 45, color: '#8b5cf6' },
    { name: 'Likes', value: 35, color: '#3b82f6' },
    { name: 'Comments', value: 15, color: '#10b981' },
    { name: 'Unfollows', value: 5, color: '#f59e0b' },
  ]

  const performanceData = accountsData.map((acc: any) => ({
    name: acc.username,
    actions: (acc.actions_today?.follow || 0) + (acc.actions_today?.like || 0) + (acc.actions_today?.comment || 0),
    success: 95 + Math.random() * 5,
  }))

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold mb-2">Analytics</h1>
          <p className="text-slate-400">Track your performance and growth</p>
        </div>
        
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="px-6 py-3 bg-slate-700 hover:bg-slate-600 rounded-lg font-semibold flex items-center gap-2"
        >
          <Download className="w-5 h-5" />
          Export Report
        </motion.button>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-br from-purple-600 to-purple-700 rounded-xl p-6"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center">
              <Target className="w-6 h-6 text-white" />
            </div>
            <TrendingUp className="w-5 h-5 text-white/80" />
          </div>
          <h3 className="text-3xl font-bold mb-1">{analyticsData?.total_actions || 0}</h3>
          <p className="text-purple-200 text-sm">Total Actions</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl p-6"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center">
              <Award className="w-6 h-6 text-white" />
            </div>
            <TrendingUp className="w-5 h-5 text-white/80" />
          </div>
          <h3 className="text-3xl font-bold mb-1">
            {analyticsData?.success_rate ? (analyticsData.success_rate * 100).toFixed(1) : 0}%
          </h3>
          <p className="text-blue-200 text-sm">Success Rate</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-gradient-to-br from-green-600 to-green-700 rounded-xl p-6"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center">
              <Calendar className="w-6 h-6 text-white" />
            </div>
            <TrendingUp className="w-5 h-5 text-white/80" />
          </div>
          <h3 className="text-3xl font-bold mb-1">{analyticsData?.active_accounts || 0}</h3>
          <p className="text-green-200 text-sm">Active Accounts</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-gradient-to-br from-orange-600 to-orange-700 rounded-xl p-6"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-white" />
            </div>
            <span className="text-white/80 text-sm">+24%</span>
          </div>
          <h3 className="text-3xl font-bold mb-1">892</h3>
          <p className="text-orange-200 text-sm">Avg. Daily Actions</p>
        </motion.div>
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Weekly Activity */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="lg:col-span-2 bg-slate-800 rounded-xl p-6 border border-slate-700"
        >
          <h3 className="text-lg font-semibold mb-6">Weekly Activity</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={weeklyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="day" stroke="#64748b" />
              <YAxis stroke="#64748b" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1e293b', 
                  border: '1px solid #334155', 
                  borderRadius: '8px' 
                }}
              />
              <Legend />
              <Bar dataKey="follows" fill="#8b5cf6" />
              <Bar dataKey="likes" fill="#3b82f6" />
              <Bar dataKey="comments" fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Action Distribution */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-slate-800 rounded-xl p-6 border border-slate-700"
        >
          <h3 className="text-lg font-semibold mb-6">Action Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={actionDistribution}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
              >
                {actionDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1e293b', 
                  border: '1px solid #334155', 
                  borderRadius: '8px' 
                }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-4 space-y-2">
            {actionDistribution.map((item, index) => (
              <div key={index} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></div>
                  <span>{item.name}</span>
                </div>
                <span className="font-semibold">{item.value}%</span>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Account Performance */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="bg-slate-800 rounded-xl p-6 border border-slate-700"
      >
        <h3 className="text-lg font-semibold mb-6">Account Performance</h3>
        
        {performanceData.length > 0 ? (
          <div className="space-y-4">
            {performanceData.map((account: any, index: number) => (
              <div key={index} className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="font-medium">@{account.name}</span>
                  <div className="flex items-center gap-4">
                    <span className="text-slate-400">{account.actions} actions</span>
                    <span className="text-green-400">{account.success.toFixed(1)}% success</span>
                  </div>
                </div>
                <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${account.success}%` }}
                    transition={{ duration: 1, delay: index * 0.1 }}
                    className="h-full bg-gradient-to-r from-purple-600 to-blue-600"
                  ></motion.div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-slate-400">
            No performance data available
          </div>
        )}
      </motion.div>

      {/* Growth Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border border-purple-500/30 rounded-xl p-6"
        >
          <div className="flex items-center gap-3 mb-4">
            <TrendingUp className="w-6 h-6 text-purple-400" />
            <h3 className="font-semibold">Best Day</h3>
          </div>
          <p className="text-3xl font-bold mb-2">Thursday</p>
          <p className="text-sm text-slate-400">61 follows, 312 likes on average</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border border-blue-500/30 rounded-xl p-6"
        >
          <div className="flex items-center gap-3 mb-4">
            <Award className="w-6 h-6 text-blue-400" />
            <h3 className="font-semibold">Top Performer</h3>
          </div>
          <p className="text-3xl font-bold mb-2">@{accountsData[0]?.username || 'N/A'}</p>
          <p className="text-sm text-slate-400">98.5% success rate this week</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9 }}
          className="bg-gradient-to-br from-green-600/20 to-green-800/20 border border-green-500/30 rounded-xl p-6"
        >
          <div className="flex items-center gap-3 mb-4">
            <Calendar className="w-6 h-6 text-green-400" />
            <h3 className="font-semibold">Growth Rate</h3>
          </div>
          <p className="text-3xl font-bold mb-2">+24.5%</p>
          <p className="text-sm text-slate-400">Compared to last week</p>
        </motion.div>
      </div>
    </div>
  )
}
