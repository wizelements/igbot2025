'use client'

import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { apiClient } from '@/lib/api'
import { 
  Settings as SettingsIcon, 
  Shield, 
  Clock, 
  Zap,
  Globe,
  Bell,
  Save,
  RotateCcw
} from 'lucide-react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'

export default function SettingsPage() {
  const { data: config } = useQuery({
    queryKey: ['config'],
    queryFn: () => apiClient.getConfig(),
  })

  const [settings, setSettings] = useState({
    maxFollowsPerDay: 200,
    maxLikesPerDay: 500,
    maxCommentsPerDay: 50,
    maxUnfollowsPerDay: 150,
    peakHoursStart: 10,
    peakHoursEnd: 21,
    timezone: 'America/Los_Angeles',
    enableHumanSimulation: true,
    enableProxyRotation: false,
    minDelaySeconds: 30,
    maxDelaySeconds: 120,
    enableNotifications: true,
    notifyOnError: true,
    notifyOnSuccess: false,
  })

  const updateMutation = useMutation({
    mutationFn: (data: any) => apiClient.updateConfig(data),
    onSuccess: () => {
      toast.success('Settings saved successfully!', { icon: '✅' })
    },
    onError: () => {
      toast.error('Failed to save settings')
    },
  })

  const handleSave = () => {
    updateMutation.mutate(settings)
  }

  const handleReset = () => {
    if (config?.data) {
      setSettings({
        maxFollowsPerDay: config.data.anti_ban?.max_follows_per_day || 200,
        maxLikesPerDay: config.data.anti_ban?.max_likes_per_day || 500,
        maxCommentsPerDay: config.data.anti_ban?.max_comments_per_day || 50,
        maxUnfollowsPerDay: 150,
        peakHoursStart: config.data.scheduler?.peak_hours_start || 10,
        peakHoursEnd: config.data.scheduler?.peak_hours_end || 21,
        timezone: config.data.scheduler?.timezone || 'America/Los_Angeles',
        enableHumanSimulation: config.data.anti_ban?.enabled || true,
        enableProxyRotation: config.data.proxy?.enabled || false,
        minDelaySeconds: 30,
        maxDelaySeconds: 120,
        enableNotifications: true,
        notifyOnError: true,
        notifyOnSuccess: false,
      })
      toast.success('Settings reset to defaults')
    }
  }

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold mb-2">Settings</h1>
          <p className="text-slate-400">Configure bot behavior and limits</p>
        </div>
        
        <div className="flex gap-3">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleReset}
            className="px-6 py-3 bg-slate-700 hover:bg-slate-600 rounded-lg font-semibold flex items-center gap-2"
          >
            <RotateCcw className="w-5 h-5" />
            Reset
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleSave}
            disabled={updateMutation.isPending}
            className="px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold flex items-center gap-2 disabled:opacity-50"
          >
            <Save className="w-5 h-5" />
            {updateMutation.isPending ? 'Saving...' : 'Save Changes'}
          </motion.button>
        </div>
      </div>

      {/* Anti-Ban Settings */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-slate-800 rounded-xl p-6 border border-slate-700"
      >
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 bg-red-600/20 rounded-lg flex items-center justify-center">
            <Shield className="w-5 h-5 text-red-400" />
          </div>
          <div>
            <h3 className="text-lg font-semibold">Anti-Ban Protection</h3>
            <p className="text-sm text-slate-400">Daily action limits to avoid detection</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium mb-2">Max Follows Per Day</label>
            <input
              type="number"
              value={settings.maxFollowsPerDay}
              onChange={(e) => setSettings({ ...settings, maxFollowsPerDay: parseInt(e.target.value) })}
              className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg focus:outline-none focus:border-purple-500"
            />
            <p className="text-xs text-slate-500 mt-1">Recommended: 150-250</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Max Likes Per Day</label>
            <input
              type="number"
              value={settings.maxLikesPerDay}
              onChange={(e) => setSettings({ ...settings, maxLikesPerDay: parseInt(e.target.value) })}
              className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg focus:outline-none focus:border-purple-500"
            />
            <p className="text-xs text-slate-500 mt-1">Recommended: 400-600</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Max Comments Per Day</label>
            <input
              type="number"
              value={settings.maxCommentsPerDay}
              onChange={(e) => setSettings({ ...settings, maxCommentsPerDay: parseInt(e.target.value) })}
              className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg focus:outline-none focus:border-purple-500"
            />
            <p className="text-xs text-slate-500 mt-1">Recommended: 30-70</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Max Unfollows Per Day</label>
            <input
              type="number"
              value={settings.maxUnfollowsPerDay}
              onChange={(e) => setSettings({ ...settings, maxUnfollowsPerDay: parseInt(e.target.value) })}
              className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg focus:outline-none focus:border-purple-500"
            />
            <p className="text-xs text-slate-500 mt-1">Recommended: 100-200</p>
          </div>
        </div>

        <div className="mt-6 flex items-center gap-3">
          <input
            type="checkbox"
            id="humanSim"
            checked={settings.enableHumanSimulation}
            onChange={(e) => setSettings({ ...settings, enableHumanSimulation: e.target.checked })}
            className="w-4 h-4"
          />
          <label htmlFor="humanSim" className="text-sm">
            Enable human-like behavior simulation (recommended)
          </label>
        </div>
      </motion.div>

      {/* Scheduler Settings */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-slate-800 rounded-xl p-6 border border-slate-700"
      >
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 bg-blue-600/20 rounded-lg flex items-center justify-center">
            <Clock className="w-5 h-5 text-blue-400" />
          </div>
          <div>
            <h3 className="text-lg font-semibold">Scheduler</h3>
            <p className="text-sm text-slate-400">Configure active hours and timing</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="block text-sm font-medium mb-2">Peak Hours Start</label>
            <input
              type="number"
              min="0"
              max="23"
              value={settings.peakHoursStart}
              onChange={(e) => setSettings({ ...settings, peakHoursStart: parseInt(e.target.value) })}
              className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg focus:outline-none focus:border-purple-500"
            />
            <p className="text-xs text-slate-500 mt-1">Hour (0-23)</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Peak Hours End</label>
            <input
              type="number"
              min="0"
              max="23"
              value={settings.peakHoursEnd}
              onChange={(e) => setSettings({ ...settings, peakHoursEnd: parseInt(e.target.value) })}
              className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg focus:outline-none focus:border-purple-500"
            />
            <p className="text-xs text-slate-500 mt-1">Hour (0-23)</p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Timezone</label>
            <select
              value={settings.timezone}
              onChange={(e) => setSettings({ ...settings, timezone: e.target.value })}
              className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg focus:outline-none focus:border-purple-500"
            >
              <option value="America/New_York">Eastern Time</option>
              <option value="America/Chicago">Central Time</option>
              <option value="America/Denver">Mountain Time</option>
              <option value="America/Los_Angeles">Pacific Time</option>
              <option value="Europe/London">London</option>
              <option value="Europe/Paris">Paris</option>
              <option value="Asia/Tokyo">Tokyo</option>
            </select>
          </div>
        </div>
      </motion.div>

      {/* Action Delays */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-slate-800 rounded-xl p-6 border border-slate-700"
      >
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 bg-purple-600/20 rounded-lg flex items-center justify-center">
            <Zap className="w-5 h-5 text-purple-400" />
          </div>
          <div>
            <h3 className="text-lg font-semibold">Action Delays</h3>
            <p className="text-sm text-slate-400">Random delays between actions</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium mb-2">Minimum Delay (seconds)</label>
            <input
              type="number"
              value={settings.minDelaySeconds}
              onChange={(e) => setSettings({ ...settings, minDelaySeconds: parseInt(e.target.value) })}
              className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg focus:outline-none focus:border-purple-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Maximum Delay (seconds)</label>
            <input
              type="number"
              value={settings.maxDelaySeconds}
              onChange={(e) => setSettings({ ...settings, maxDelaySeconds: parseInt(e.target.value) })}
              className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg focus:outline-none focus:border-purple-500"
            />
          </div>
        </div>

        <div className="mt-4 p-4 bg-blue-950/20 border border-blue-500/30 rounded-lg">
          <p className="text-sm text-blue-400">
            ℹ️ Bot will wait between {settings.minDelaySeconds} and {settings.maxDelaySeconds} seconds between actions
          </p>
        </div>
      </motion.div>

      {/* Proxy Settings */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-slate-800 rounded-xl p-6 border border-slate-700"
      >
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 bg-green-600/20 rounded-lg flex items-center justify-center">
            <Globe className="w-5 h-5 text-green-400" />
          </div>
          <div>
            <h3 className="text-lg font-semibold">Proxy Settings</h3>
            <p className="text-sm text-slate-400">Rotate IP addresses for safety</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <input
            type="checkbox"
            id="proxyRotation"
            checked={settings.enableProxyRotation}
            onChange={(e) => setSettings({ ...settings, enableProxyRotation: e.target.checked })}
            className="w-4 h-4"
          />
          <label htmlFor="proxyRotation" className="text-sm">
            Enable proxy rotation (requires proxy service)
          </label>
        </div>

        {settings.enableProxyRotation && (
          <div className="mt-4 p-4 bg-orange-950/20 border border-orange-500/30 rounded-lg">
            <p className="text-sm text-orange-400">
              ⚠️ Configure PROXY_API_KEY in environment variables
            </p>
          </div>
        )}
      </motion.div>

      {/* Notifications */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-slate-800 rounded-xl p-6 border border-slate-700"
      >
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 bg-orange-600/20 rounded-lg flex items-center justify-center">
            <Bell className="w-5 h-5 text-orange-400" />
          </div>
          <div>
            <h3 className="text-lg font-semibold">Notifications</h3>
            <p className="text-sm text-slate-400">Alert preferences</p>
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              id="notifications"
              checked={settings.enableNotifications}
              onChange={(e) => setSettings({ ...settings, enableNotifications: e.target.checked })}
              className="w-4 h-4"
            />
            <label htmlFor="notifications" className="text-sm">
              Enable notifications
            </label>
          </div>

          {settings.enableNotifications && (
            <>
              <div className="flex items-center gap-3 ml-7">
                <input
                  type="checkbox"
                  id="notifyError"
                  checked={settings.notifyOnError}
                  onChange={(e) => setSettings({ ...settings, notifyOnError: e.target.checked })}
                  className="w-4 h-4"
                />
                <label htmlFor="notifyError" className="text-sm">
                  Notify on errors
                </label>
              </div>

              <div className="flex items-center gap-3 ml-7">
                <input
                  type="checkbox"
                  id="notifySuccess"
                  checked={settings.notifyOnSuccess}
                  onChange={(e) => setSettings({ ...settings, notifyOnSuccess: e.target.checked })}
                  className="w-4 h-4"
                />
                <label htmlFor="notifySuccess" className="text-sm">
                  Notify on milestones
                </label>
              </div>
            </>
          )}
        </div>
      </motion.div>
    </div>
  )
}
