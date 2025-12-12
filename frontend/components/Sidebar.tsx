'use client'

import { usePathname, useRouter } from 'next/navigation'
import { 
  LayoutDashboard, 
  Users, 
  BarChart3, 
  Settings, 
  LogOut,
  Zap,
  FileText,
  Trophy
} from 'lucide-react'
import { auth } from '@/lib/api'
import { motion } from 'framer-motion'
import { easterEggs } from '@/lib/easter-eggs'
import { useState } from 'react'

const menuItems = [
  { icon: LayoutDashboard, label: 'Dashboard', href: '/dashboard' },
  { icon: Users, label: 'Accounts', href: '/dashboard/accounts' },
  { icon: BarChart3, label: 'Analytics', href: '/dashboard/analytics' },
  { icon: Zap, label: 'Actions', href: '/dashboard/actions' },
  { icon: FileText, label: 'Logs', href: '/dashboard/logs' },
  { icon: Settings, label: 'Settings', href: '/dashboard/settings' },
]

export default function Sidebar() {
  const pathname = usePathname()
  const router = useRouter()
  const [logoClicks, setLogoClicks] = useState(0)

  const handleLogout = () => {
    auth.logout()
    router.push('/login')
  }

  const handleLogoClick = () => {
    const newCount = logoClicks + 1
    setLogoClicks(newCount)
    easterEggs.handleLogoClick()
    
    if (newCount >= 10) {
      setLogoClicks(0)
    }
  }

  return (
    <div className="w-64 bg-slate-800 border-r border-slate-700 h-screen flex flex-col">
      {/* Logo */}
      <div 
        className="p-6 border-b border-slate-700 cursor-pointer"
        onClick={handleLogoClick}
      >
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-500 rounded-lg flex items-center justify-center">
            <Zap className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold">IGBot 2025</h1>
            <p className="text-xs text-slate-400">v1.0.0</p>
          </div>
        </div>
      </div>

      {/* Menu */}
      <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.href
          
          return (
            <motion.button
              key={item.href}
              whileHover={{ x: 4 }}
              onClick={() => router.push(item.href)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-purple-600 text-white'
                  : 'text-slate-300 hover:bg-slate-700'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="font-medium">{item.label}</span>
            </motion.button>
          )
        })}

        {/* Easter egg menu items */}
        {easterEggs.isUnlocked('konami') && (
          <motion.button
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            whileHover={{ x: 4 }}
            onClick={() => router.push('/dashboard/premium')}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-yellow-400 hover:bg-slate-700 transition-colors border border-yellow-500/30"
          >
            <Trophy className="w-5 h-5" />
            <span className="font-medium">Premium Analytics</span>
          </motion.button>
        )}
      </nav>

      {/* User info & logout */}
      <div className="p-4 border-t border-slate-700">
        <div className="flex items-center justify-between mb-3">
          <div>
            <p className="text-sm font-medium">{auth.getUsername()}</p>
            <p className="text-xs text-slate-400">Administrator</p>
          </div>
        </div>
        
        <button
          onClick={handleLogout}
          className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors text-sm"
        >
          <LogOut className="w-4 h-4" />
          Logout
        </button>
      </div>
    </div>
  )
}
