'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { auth } from '@/lib/api'
import Sidebar from '@/components/Sidebar'
import { easterEggs, achievementSystem } from '@/lib/easter-eggs'
import toast from 'react-hot-toast'
import { motion, AnimatePresence } from 'framer-motion'
import { Trophy, X } from 'lucide-react'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const [mounted, setMounted] = useState(false)
  const [showMatrix, setShowMatrix] = useState(false)
  const [showQuickStats, setShowQuickStats] = useState(false)
  const [showAchievement, setShowAchievement] = useState<any>(null)

  useEffect(() => {
    setMounted(true)
    
    // Check authentication
    if (!auth.isAuthenticated()) {
      router.push('/login')
      return
    }

    // Setup easter egg listeners
    easterEggs.onKonamiUnlock = () => {
      toast.success('🎮 Premium Analytics Unlocked!', {
        duration: 5000,
        icon: '🎮',
      })
    }

    easterEggs.onGodModeUnlock = () => {
      toast.success('👑 God Mode Activated!', {
        duration: 5000,
        icon: '👑',
      })
    }

    easterEggs.onTimeTravelerUnlock = () => {
      toast.success('⏰ Time Traveler Mode Unlocked!', {
        duration: 5000,
        icon: '⏰',
      })
    }

    easterEggs.onMatrixModeToggle = () => {
      setShowMatrix(prev => !prev)
    }

    easterEggs.onQuickStatsToggle = () => {
      setShowQuickStats(prev => !prev)
    }

    // Listen for achievement unlocks
    const handleAchievement = (e: any) => {
      setShowAchievement(e.detail.achievement)
      setTimeout(() => setShowAchievement(null), 5000)
    }

    window.addEventListener('achievementUnlock', handleAchievement)

    return () => {
      window.removeEventListener('achievementUnlock', handleAchievement)
    }
  }, [router])

  if (!mounted) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-purple-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    )
  }

  return (
    <div className="flex h-screen bg-slate-900 overflow-hidden">
      <Sidebar />
      
      <main className="flex-1 overflow-y-auto">
        {children}
      </main>

      {/* Matrix Rain Effect */}
      {showMatrix && <MatrixRain />}

      {/* Quick Stats Widget */}
      <AnimatePresence>
        {showQuickStats && (
          <motion.div
            initial={{ opacity: 0, x: 300 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 300 }}
            className="fixed top-4 right-4 w-64 bg-slate-800/90 backdrop-blur border border-slate-700 rounded-lg p-4 shadow-2xl z-50"
          >
            <div className="flex justify-between items-center mb-3">
              <h3 className="font-semibold">Quick Stats</h3>
              <button onClick={() => setShowQuickStats(false)}>
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-slate-400">Active:</span>
                <span className="text-green-400">3 accounts</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Today:</span>
                <span>156 actions</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Success:</span>
                <span className="text-green-400">98.5%</span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Achievement Notification */}
      <AnimatePresence>
        {showAchievement && (
          <motion.div
            initial={{ opacity: 0, y: -100 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -100 }}
            className="fixed top-4 left-1/2 -translate-x-1/2 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-lg p-4 shadow-2xl z-50 min-w-[300px]"
          >
            <div className="flex items-center gap-3">
              <Trophy className="w-8 h-8 text-white" />
              <div>
                <p className="font-bold text-white">Achievement Unlocked!</p>
                <p className="text-sm text-white/90">{showAchievement.icon} {showAchievement.title}</p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

// Matrix Rain Component
function MatrixRain() {
  useEffect(() => {
    const canvas = document.getElementById('matrix-canvas') as HTMLCanvasElement
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    const characters = 'アイウエオカキクケコサシスセソタチツテト01'
    const fontSize = 14
    const columns = canvas.width / fontSize
    const drops: number[] = []

    for (let i = 0; i < columns; i++) {
      drops[i] = Math.random() * -100
    }

    function draw() {
      if (!ctx || !canvas) return
      
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      ctx.fillStyle = '#0F0'
      ctx.font = fontSize + 'px monospace'

      for (let i = 0; i < drops.length; i++) {
        const text = characters.charAt(Math.floor(Math.random() * characters.length))
        ctx.fillText(text, i * fontSize, drops[i] * fontSize)

        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
          drops[i] = 0
        }
        drops[i]++
      }
    }

    const interval = setInterval(draw, 33)

    return () => clearInterval(interval)
  }, [])

  return (
    <canvas
      id="matrix-canvas"
      className="fixed inset-0 pointer-events-none z-0 opacity-30"
    />
  )
}
