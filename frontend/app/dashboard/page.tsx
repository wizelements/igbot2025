'use client'

import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/lib/api'
import { 
  Activity, 
  Users, 
  TrendingUp, 
  Zap,
  Play,
  Pause,
  AlertCircle,
  CheckCircle,
  Clock
} from 'lucide-react'
import { motion } from 'framer-motion'
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import toast from 'react-hot-toast'
import { useState } from 'react'

export default function DashboardPage() {
  const [isStarting, setIsStarting] = useState(false)
  const [isStopping, setIsStopping] = useState(false)

  const { data: status, refetch: refetchStatus } = useQuery({
    queryKey: ['status'],
    queryFn: () => apiClient.getStatus(),
    refetchInterval: 5000,
  })

  const { data: accounts } = useQuery({
    queryKey: ['accounts'],
    queryFn: () => apiClient.getAccounts(),
    refetchInterval: 10000,
  })

  const { data: analytics } = useQuery({
    queryKey: ['analytics'],
    queryFn: () => apiClient.getAnalytics(),
    refetchInterval: 30000,
  })

  const handleStartBot = async () => {
    setIsStarting(true)
    try {
      await apiClient.startBot()
      toast.success('🚀 Bot started successfully!')
      refetchStatus()
    } catch (error) {
      toast.error('Failed to start bot')
    } finally {
      setIsStarting(false)
    }
  }

  const handleStopBot = async () => {
    setIsStopping(true)
    try {
      await apiClient.stopBot()
      toast.success('⏸️ Bot stopped successfully!')
      refetchStatus()
    } catch (error) {
      toast.error('Failed to stop bot')
    } finally {
      setIsStopping(false)
    }
  }

  const statusData = status?.data
  const accountsData = accounts?.data || []
  const analyticsData = analytics?.data

  // Mock chart data
  const chartData = [
    { time: '00:00', follows: 12, likes: 45, comments: 8 },
    { time: '04:00', follows: 19, likes: 67, comments: 12 },
    { time: '08:00', follows: 25, likes: 89, comments: 15 },
    { time: '12:00', follows: 38, likes: 134, comments: 23 },
    { time: '16:00', follows: 42, likes: 156, comments: 28 },
    { time: '20:00', follows: 35, likes: 123, comments: 19 },
  ]

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
          <p className="text-slate-400">Monitor and control your Instagram automation</p>
        </div>
        
        <div className="flex gap-3">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleStartBot}
            disabled={isStarting}
            className="px-6 py-3 bg-green-600 hover:bg-green-700 rounded-lg font-semibold flex items-center gap-2 disabled:opacity-50"
          >
            {isStarting ? (
              <>
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                Starting...
              </>
            ) : (
              <>
                <Play className="w-5 h-5" />
                Start Bot
              </>
            )}
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleStopBot}
            disabled={isStopping}
            className="px-6 py-3 bg-red-600 hover:bg-red-700 rounded-lg font-semibold flex items-center gap-2 disabled:opacity-50"
          >
            {isStopping ? (
              <>
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                Stopping...
              </>
            ) : (
              <>
                <Pause className="w-5 h-5" />
                Stop Bot
              </>
            )}
          </motion.button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-slate-800 rounded-xl p-6 border border-slate-700"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-blue-600/20 rounded-lg flex items-center justify-center">
              <Users className="w-6 h-6 text-blue-400" />
            </div>
            <span className="text-green-400 text-sm font-semibold flex items-center gap-1">
              <TrendingUp className="w-4 h-4" />
              +12%
            </span>
          </div>
          <h3 className="text-2xl font-bold mb-1">{statusData?.accounts || 0}</h3>
          <p className="text-slate-400 text-sm">Active Accounts</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-slate-800 rounded-xl p-6 border border-slate-700"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-purple-600/20 rounded-lg flex items-center justify-center">
              <Activity className="w-6 h-6 text-purple-400" />
            </div>
            <span className="text-green-400 text-sm font-semibold flex items-center gap-1">
              <TrendingUp className="w-4 h-4" />
              +34%
            </span>
          </div>
          <h3 className="text-2xl font-bold mb-1">{statusData?.total_actions || 0}</h3>
          <p className="text-slate-400 text-sm">Total Actions</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-slate-800 rounded-xl p-6 border border-slate-700"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-green-600/20 rounded-lg flex items-center justify-center">
              <CheckCircle className="w-6 h-6 text-green-400" />
            </div>
            <span className="text-green-400 text-sm font-semibold">Excellent</span>
          </div>
          <h3 className="text-2xl font-bold mb-1">{analyticsData?.success_rate ? (analyticsData.success_rate * 100).toFixed(1) : 0}%</h3>
          <p className="text-slate-400 text-sm">Success Rate</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-slate-800 rounded-xl p-6 border border-slate-700"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="w-12 h-12 bg-orange-600/20 rounded-lg flex items-center justify-center">
              <Zap className="w-6 h-6 text-orange-400" />
            </div>
            <span className="text-sm font-semibold text-yellow-400">Live</span>
          </div>
          <h3 className="text-2xl font-bold mb-1">{statusData?.status === 'running' ? 'Active' : 'Idle'}</h3>
          <p className="text-slate-400 text-sm">Bot Status</p>
        </motion.div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Activity Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-slate-800 rounded-xl p-6 border border-slate-700"
        >
          <h3 className="text-lg font-semibold mb-4">Activity Overview</h3>
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="colorFollows" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="time" stroke="#64748b" />
              <YAxis stroke="#64748b" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
              />
              <Area type="monotone" dataKey="follows" stroke="#8b5cf6" fillOpacity={1} fill="url(#colorFollows)" />
            </AreaChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Actions Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-slate-800 rounded-xl p-6 border border-slate-700"
        >
          <h3 className="text-lg font-semibold mb-4">Actions Breakdown</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="time" stroke="#64748b" />
              <YAxis stroke="#64748b" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
              />
              <Line type="monotone" dataKey="likes" stroke="#3b82f6" strokeWidth={2} />
              <Line type="monotone" dataKey="comments" stroke="#10b981" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Accounts Status */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7 }}
        className="bg-slate-800 rounded-xl p-6 border border-slate-700"
      >
        <h3 className="text-lg font-semibold mb-4">Account Status</h3>
        
        {accountsData.length > 0 ? (
          <div className="space-y-3">
            {accountsData.map((account: any, index: number) => (
              <div key={index} className="flex items-center justify-between p-4 bg-slate-900 rounded-lg">
                <div className="flex items-center gap-4">
                  <div className={`w-3 h-3 rounded-full ${account.is_active ? 'bg-green-400 animate-pulse' : 'bg-slate-600'}`}></div>
                  <div>
                    <p className="font-medium">@{account.username}</p>
                    <p className="text-sm text-slate-400">{account.status}</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-6 text-sm">
                  <div className="text-center">
                    <p className="text-slate-400">Follows</p>
                    <p className="font-semibold">{account.actions_today?.follow || 0}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-slate-400">Likes</p>
                    <p className="font-semibold">{account.actions_today?.like || 0}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-slate-400">Comments</p>
                    <p className="font-semibold">{account.actions_today?.comment || 0}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-slate-400">
            <AlertCircle className="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p>No accounts configured yet</p>
          </div>
        )}
      </motion.div>

      {/* Quick Tip */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
        className="bg-gradient-to-r from-purple-600/20 to-blue-600/20 border border-purple-500/30 rounded-xl p-4"
      >
        <div className="flex items-start gap-3">
          <Clock className="w-5 h-5 text-purple-400 mt-0.5" />
          <div>
            <p className="font-semibold mb-1">💡 Pro Tip</p>
            <p className="text-sm text-slate-300">
              Press <kbd className="px-2 py-1 bg-slate-800 rounded text-xs">?</kbd> for quick stats or try the Konami code for premium features!
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
