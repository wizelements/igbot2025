'use client'

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/lib/api'
import { 
  Play, 
  Heart, 
  MessageCircle, 
  UserPlus, 
  UserMinus,
  Target,
  Zap,
  Clock,
  CheckCircle
} from 'lucide-react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'

interface QuickAction {
  id: string
  name: string
  description: string
  icon: any
  color: string
  action: string
}

const quickActions: QuickAction[] = [
  {
    id: 'follow',
    name: 'Follow Users',
    description: 'Follow targeted users from hashtags',
    icon: UserPlus,
    color: 'blue',
    action: 'follow',
  },
  {
    id: 'like',
    name: 'Like Posts',
    description: 'Like posts from your timeline',
    icon: Heart,
    color: 'red',
    action: 'like',
  },
  {
    id: 'comment',
    name: 'Comment',
    description: 'Comment on engaging posts',
    icon: MessageCircle,
    color: 'green',
    action: 'comment',
  },
  {
    id: 'unfollow',
    name: 'Unfollow',
    description: 'Unfollow non-followers',
    icon: UserMinus,
    color: 'orange',
    action: 'unfollow',
  },
]

export default function ActionsPage() {
  const [executingAction, setExecutingAction] = useState<string | null>(null)

  const { data: accounts } = useQuery({
    queryKey: ['accounts'],
    queryFn: () => apiClient.getAccounts(),
  })

  const accountsData = accounts?.data || []

  const handleExecuteAction = async (action: QuickAction) => {
    setExecutingAction(action.id)
    
    try {
      // Execute action for all active accounts
      for (const account of accountsData.filter((a: any) => a.is_active)) {
        await apiClient.executeCommand({
          action: action.action,
          username: account.username,
        })
      }
      
      toast.success(`${action.name} executed successfully!`, {
        icon: '✅',
      })
    } catch (error) {
      toast.error(`Failed to execute ${action.name}`)
    } finally {
      setExecutingAction(null)
    }
  }

  const colorClasses = {
    blue: 'from-blue-600 to-blue-700',
    red: 'from-red-600 to-red-700',
    green: 'from-green-600 to-green-700',
    orange: 'from-orange-600 to-orange-700',
    purple: 'from-purple-600 to-purple-700',
  }

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">Quick Actions</h1>
        <p className="text-slate-400">Execute instant actions across your accounts</p>
      </div>

      {/* Quick Actions Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {quickActions.map((action, index) => {
          const Icon = action.icon
          const isExecuting = executingAction === action.id
          
          return (
            <motion.div
              key={action.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.03 }}
              className={`bg-gradient-to-br ${colorClasses[action.color as keyof typeof colorClasses]} rounded-xl p-6 cursor-pointer relative overflow-hidden`}
              onClick={() => !isExecuting && handleExecuteAction(action)}
            >
              {/* Background pattern */}
              <div className="absolute inset-0 opacity-10">
                <div className="absolute inset-0" style={{
                  backgroundImage: 'radial-gradient(circle, white 1px, transparent 1px)',
                  backgroundSize: '20px 20px',
                }}></div>
              </div>

              <div className="relative z-10">
                <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center mb-4">
                  <Icon className="w-6 h-6 text-white" />
                </div>
                
                <h3 className="text-xl font-bold mb-2">{action.name}</h3>
                <p className="text-white/80 text-sm mb-4">{action.description}</p>
                
                {isExecuting ? (
                  <div className="flex items-center gap-2 text-sm">
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    <span>Executing...</span>
                  </div>
                ) : (
                  <div className="flex items-center gap-2 text-sm font-semibold">
                    <Play className="w-4 h-4" />
                    <span>Execute Now</span>
                  </div>
                )}
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* Scheduled Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-slate-800 rounded-xl p-6 border border-slate-700"
      >
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-purple-600/20 rounded-lg flex items-center justify-center">
              <Clock className="w-5 h-5 text-purple-400" />
            </div>
            <div>
              <h3 className="text-lg font-semibold">Scheduled Actions</h3>
              <p className="text-sm text-slate-400">Automated tasks running in background</p>
            </div>
          </div>
          <span className="px-3 py-1 bg-green-600/20 text-green-400 rounded-full text-sm">
            Active
          </span>
        </div>

        <div className="space-y-3">
          {[
            { name: 'Auto Follow', time: 'Every 2 hours', status: 'active' },
            { name: 'Auto Like', time: 'Every 30 minutes', status: 'active' },
            { name: 'Auto Comment', time: 'Every 4 hours', status: 'active' },
            { name: 'Auto Unfollow', time: 'Daily at 3 AM', status: 'active' },
          ].map((scheduled, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-4 bg-slate-900 rounded-lg"
            >
              <div className="flex items-center gap-3">
                <div className={`w-2 h-2 rounded-full ${scheduled.status === 'active' ? 'bg-green-400 animate-pulse' : 'bg-slate-600'}`}></div>
                <div>
                  <p className="font-medium">{scheduled.name}</p>
                  <p className="text-sm text-slate-400">{scheduled.time}</p>
                </div>
              </div>
              <CheckCircle className="w-5 h-5 text-green-400" />
            </div>
          ))}
        </div>
      </motion.div>

      {/* Action Statistics */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="bg-slate-800 rounded-xl p-6 border border-slate-700"
      >
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 bg-blue-600/20 rounded-lg flex items-center justify-center">
            <Target className="w-5 h-5 text-blue-400" />
          </div>
          <div>
            <h3 className="text-lg font-semibold">Today's Activity</h3>
            <p className="text-sm text-slate-400">Actions performed across all accounts</p>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'Follows', value: 127, color: 'blue' },
            { label: 'Likes', value: 456, color: 'red' },
            { label: 'Comments', value: 34, color: 'green' },
            { label: 'Unfollows', value: 89, color: 'orange' },
          ].map((stat, index) => (
            <div key={index} className="text-center p-4 bg-slate-900 rounded-lg">
              <p className={`text-3xl font-bold text-${stat.color}-400 mb-1`}>{stat.value}</p>
              <p className="text-sm text-slate-400">{stat.label}</p>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Pro Tip */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
        className="bg-gradient-to-r from-purple-600/20 to-blue-600/20 border border-purple-500/30 rounded-xl p-4"
      >
        <div className="flex items-start gap-3">
          <Zap className="w-5 h-5 text-purple-400 mt-0.5" />
          <div>
            <p className="font-semibold mb-1">💡 Pro Tip: Batch Mode</p>
            <p className="text-sm text-slate-300">
              Press <kbd className="px-2 py-1 bg-slate-800 rounded text-xs">B</kbd> to activate Batch Mode for executing actions on multiple accounts simultaneously!
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
