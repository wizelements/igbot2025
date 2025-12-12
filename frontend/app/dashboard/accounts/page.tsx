'use client'

import { useQuery, useMutation } from '@tanstack/react-query'
import { apiClient } from '@/lib/api'
import { Plus, Trash2, Play, Pause, AlertCircle, CheckCircle, Shield } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'
import toast from 'react-hot-toast'

export default function AccountsPage() {
  const [showAddModal, setShowAddModal] = useState(false)
  const [newAccount, setNewAccount] = useState({
    username: '',
    password: '',
    two_fa_secret: '',
  })

  const { data: accounts, refetch } = useQuery({
    queryKey: ['accounts'],
    queryFn: () => apiClient.getAccounts(),
    refetchInterval: 10000,
  })

  const addAccountMutation = useMutation({
    mutationFn: (data: typeof newAccount) => apiClient.addAccount(data),
    onSuccess: () => {
      toast.success('Account added successfully! 🎉')
      setShowAddModal(false)
      setNewAccount({ username: '', password: '', two_fa_secret: '' })
      refetch()
    },
    onError: () => {
      toast.error('Failed to add account')
    },
  })

  const handleAddAccount = () => {
    if (!newAccount.username || !newAccount.password) {
      toast.error('Username and password are required')
      return
    }
    addAccountMutation.mutate(newAccount)
  }

  const accountsData = accounts?.data || []

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold mb-2">Accounts</h1>
          <p className="text-slate-400">Manage your Instagram accounts</p>
        </div>
        
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setShowAddModal(true)}
          className="px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Add Account
        </motion.button>
      </div>

      {/* Accounts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {accountsData.length > 0 ? (
          accountsData.map((account: any, index: number) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-slate-800 rounded-xl p-6 border border-slate-700 hover:border-purple-500/50 transition-colors"
            >
              {/* Account Header */}
              <div className="flex items-start justify-between mb-6">
                <div className="flex items-center gap-4">
                  <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-2xl font-bold">
                    {account.username.charAt(0).toUpperCase()}
                  </div>
                  <div>
                    <h3 className="text-xl font-bold">@{account.username}</h3>
                    <div className="flex items-center gap-2 mt-1">
                      <div className={`w-2 h-2 rounded-full ${account.is_active ? 'bg-green-400 animate-pulse' : 'bg-slate-600'}`}></div>
                      <span className="text-sm text-slate-400">
                        {account.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div className="flex gap-2">
                  <button className="p-2 hover:bg-slate-700 rounded-lg transition-colors">
                    {account.is_active ? (
                      <Pause className="w-5 h-5 text-orange-400" />
                    ) : (
                      <Play className="w-5 h-5 text-green-400" />
                    )}
                  </button>
                  <button className="p-2 hover:bg-slate-700 rounded-lg transition-colors">
                    <Trash2 className="w-5 h-5 text-red-400" />
                  </button>
                </div>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-4 gap-4 mb-6">
                <div className="text-center">
                  <p className="text-2xl font-bold text-blue-400">{account.actions_today?.follow || 0}</p>
                  <p className="text-xs text-slate-400">Follows</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-purple-400">{account.actions_today?.like || 0}</p>
                  <p className="text-xs text-slate-400">Likes</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-green-400">{account.actions_today?.comment || 0}</p>
                  <p className="text-xs text-slate-400">Comments</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-orange-400">{account.actions_today?.unfollow || 0}</p>
                  <p className="text-xs text-slate-400">Unfollows</p>
                </div>
              </div>

              {/* Status Badges */}
              <div className="flex items-center gap-2 flex-wrap">
                <span className="px-3 py-1 bg-green-600/20 text-green-400 rounded-full text-xs flex items-center gap-1">
                  <CheckCircle className="w-3 h-3" />
                  Verified
                </span>
                <span className="px-3 py-1 bg-blue-600/20 text-blue-400 rounded-full text-xs flex items-center gap-1">
                  <Shield className="w-3 h-3" />
                  Protected
                </span>
                {account.status === 'active' && (
                  <span className="px-3 py-1 bg-purple-600/20 text-purple-400 rounded-full text-xs">
                    Running
                  </span>
                )}
              </div>

              {/* Last Action */}
              {account.last_action && (
                <div className="mt-4 pt-4 border-t border-slate-700">
                  <p className="text-xs text-slate-400">
                    Last action: <span className="text-white">{account.last_action}</span>
                  </p>
                </div>
              )}
            </motion.div>
          ))
        ) : (
          <div className="col-span-2 text-center py-20">
            <AlertCircle className="w-16 h-16 mx-auto mb-4 text-slate-600" />
            <h3 className="text-xl font-semibold mb-2">No accounts yet</h3>
            <p className="text-slate-400 mb-6">Add your first Instagram account to get started</p>
            <button
              onClick={() => setShowAddModal(true)}
              className="px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold inline-flex items-center gap-2"
            >
              <Plus className="w-5 h-5" />
              Add Account
            </button>
          </div>
        )}
      </div>

      {/* Add Account Modal */}
      <AnimatePresence>
        {showAddModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4"
            onClick={() => setShowAddModal(false)}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-slate-800 rounded-2xl p-8 max-w-md w-full border border-slate-700"
            >
              <h2 className="text-2xl font-bold mb-6">Add Instagram Account</h2>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Username</label>
                  <input
                    type="text"
                    value={newAccount.username}
                    onChange={(e) => setNewAccount({ ...newAccount, username: e.target.value })}
                    className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg focus:outline-none focus:border-purple-500"
                    placeholder="instagram_username"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Password</label>
                  <input
                    type="password"
                    value={newAccount.password}
                    onChange={(e) => setNewAccount({ ...newAccount, password: e.target.value })}
                    className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg focus:outline-none focus:border-purple-500"
                    placeholder="••••••••"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">
                    2FA Secret <span className="text-slate-500">(Optional)</span>
                  </label>
                  <input
                    type="text"
                    value={newAccount.two_fa_secret}
                    onChange={(e) => setNewAccount({ ...newAccount, two_fa_secret: e.target.value })}
                    className="w-full px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg focus:outline-none focus:border-purple-500"
                    placeholder="ABCD1234EFGH5678"
                  />
                </div>
              </div>

              <div className="flex gap-3 mt-8">
                <button
                  onClick={() => setShowAddModal(false)}
                  className="flex-1 px-6 py-3 bg-slate-700 hover:bg-slate-600 rounded-lg font-semibold transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleAddAccount}
                  disabled={addAccountMutation.isPending}
                  className="flex-1 px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold transition-colors disabled:opacity-50"
                >
                  {addAccountMutation.isPending ? 'Adding...' : 'Add Account'}
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
