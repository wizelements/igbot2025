'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { auth } from '@/lib/api'
import { Zap, Shield, TrendingUp, Users, ArrowRight, Sparkles } from 'lucide-react'
import { motion } from 'framer-motion'

export default function Home() {
  const router = useRouter()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    // Redirect if already authenticated
    if (auth.isAuthenticated()) {
      router.push('/dashboard')
    }
  }, [router])

  if (!mounted) return null

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
      
      {/* Floating orbs */}
      <div className="absolute top-20 left-20 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse-slow"></div>
      <div className="absolute bottom-20 right-20 w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse-slow" style={{ animationDelay: '1s' }}></div>

      <div className="relative z-10 min-h-screen flex flex-col">
        {/* Header */}
        <nav className="p-6 flex justify-between items-center">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent"
          >
            IGBot 2025
          </motion.div>
          
          <motion.button
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            onClick={() => router.push('/login')}
            className="px-6 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors"
          >
            Login
          </motion.button>
        </nav>

        {/* Hero Section */}
        <div className="flex-1 flex items-center justify-center px-6">
          <div className="max-w-6xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-purple-500/20 rounded-full mb-8 border border-purple-500/30">
                <Sparkles className="w-4 h-4 text-purple-400" />
                <span className="text-sm text-purple-300">Advanced Instagram Automation</span>
              </div>

              <h1 className="text-6xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-white via-purple-200 to-blue-200 bg-clip-text text-transparent">
                Grow Your Instagram
                <br />
                <span className="text-purple-400">On Autopilot</span>
              </h1>

              <p className="text-xl text-slate-300 mb-12 max-w-2xl mx-auto">
                Enterprise-grade automation with AI-powered features, anti-ban protection, 
                and real-time analytics. Scale your presence safely.
              </p>

              <div className="flex gap-4 justify-center mb-16">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => router.push('/login')}
                  className="px-8 py-4 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold flex items-center gap-2 transition-colors"
                >
                  Get Started
                  <ArrowRight className="w-5 h-5" />
                </motion.button>
                
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-8 py-4 bg-slate-800 hover:bg-slate-700 rounded-lg font-semibold transition-colors"
                >
                  View Demo
                </motion.button>
              </div>
            </motion.div>

            {/* Features */}
            <motion.div 
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="grid md:grid-cols-4 gap-6 max-w-5xl mx-auto"
            >
              <div className="p-6 bg-slate-800/50 backdrop-blur rounded-xl border border-slate-700">
                <div className="w-12 h-12 bg-purple-600/20 rounded-lg flex items-center justify-center mb-4 mx-auto">
                  <Zap className="w-6 h-6 text-purple-400" />
                </div>
                <h3 className="font-semibold mb-2">Lightning Fast</h3>
                <p className="text-sm text-slate-400">Automated actions in milliseconds</p>
              </div>

              <div className="p-6 bg-slate-800/50 backdrop-blur rounded-xl border border-slate-700">
                <div className="w-12 h-12 bg-blue-600/20 rounded-lg flex items-center justify-center mb-4 mx-auto">
                  <Shield className="w-6 h-6 text-blue-400" />
                </div>
                <h3 className="font-semibold mb-2">Anti-Ban Protection</h3>
                <p className="text-sm text-slate-400">Human-like behavior simulation</p>
              </div>

              <div className="p-6 bg-slate-800/50 backdrop-blur rounded-xl border border-slate-700">
                <div className="w-12 h-12 bg-green-600/20 rounded-lg flex items-center justify-center mb-4 mx-auto">
                  <TrendingUp className="w-6 h-6 text-green-400" />
                </div>
                <h3 className="font-semibold mb-2">Real-Time Analytics</h3>
                <p className="text-sm text-slate-400">Track growth and performance</p>
              </div>

              <div className="p-6 bg-slate-800/50 backdrop-blur rounded-xl border border-slate-700">
                <div className="w-12 h-12 bg-orange-600/20 rounded-lg flex items-center justify-center mb-4 mx-auto">
                  <Users className="w-6 h-6 text-orange-400" />
                </div>
                <h3 className="font-semibold mb-2">Multi-Account</h3>
                <p className="text-sm text-slate-400">Manage unlimited accounts</p>
              </div>
            </motion.div>
          </div>
        </div>

        {/* Footer */}
        <footer className="p-6 text-center text-slate-400 text-sm">
          <p>Built with ❤️ using Next.js, FastAPI, and AI</p>
          <p className="mt-2 text-xs">Press Ctrl+Shift+M for a surprise 👀</p>
        </footer>
      </div>
    </div>
  )
}
