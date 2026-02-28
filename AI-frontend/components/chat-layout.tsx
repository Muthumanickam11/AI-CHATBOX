"use client"

import { useState, useEffect } from "react"
import Sidebar from "@/components/sidebar"
import ChatBox from "@/components/chat-box"
import SettingsPage from "@/components/settings-page"
import { Button } from "@/components/ui/button"
import { Menu, X, Settings } from "lucide-react"

interface ChatLayoutProps {
  onLogout: () => void
  theme: "light" | "dark"
  toggleTheme: () => void
}

export default function ChatLayout({ onLogout, theme, toggleTheme }: ChatLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [isMobile, setIsMobile] = useState(false)
  const [showSettings, setShowSettings] = useState(false)

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768)
      if (window.innerWidth < 768) {
        setSidebarOpen(false)
      }
    }

    handleResize()
    window.addEventListener("resize", handleResize)
    return () => window.removeEventListener("resize", handleResize)
  }, [])

  if (showSettings) {
    return (
      <SettingsPage onBack={() => setShowSettings(false)} onLogout={onLogout} theme={theme} toggleTheme={toggleTheme} />
    )
  }

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <div
        className={`${sidebarOpen ? "w-64" : "w-0"} transition-all duration-300 border-r border-border overflow-hidden`}
      >
        <Sidebar onLogout={onLogout} onSettings={() => setShowSettings(true)} />
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="border-b border-border bg-card p-4 flex items-center justify-between">
          <Button variant="ghost" size="icon" onClick={() => setSidebarOpen(!sidebarOpen)} className="md:hidden">
            {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </Button>
          <h1 className="text-xl font-bold text-foreground">MM CHAT ASSISTANT</h1>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setShowSettings(true)}
            className="text-foreground hover:bg-muted"
          >
            <Settings size={20} />
          </Button>
        </div>

        {/* Chat Content */}
        <ChatBox />
      </div>

      {/* Mobile Overlay */}
      {isMobile && sidebarOpen && (
        <div className="fixed inset-0 bg-black/50 z-40" onClick={() => setSidebarOpen(false)} />
      )}
    </div>
  )
}
