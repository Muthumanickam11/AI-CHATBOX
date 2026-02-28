"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Moon, Sun, Bell, Lock, HelpCircle, LogOut, Download, Trash2 } from "lucide-react"

interface SettingsPageProps {
  onBack: () => void
  onLogout: () => void
  theme: "light" | "dark"
  toggleTheme: () => void
}

export default function SettingsPage({ onBack, onLogout, theme, toggleTheme }: SettingsPageProps) {
  const [notifications, setNotifications] = useState(true)
  const [autoSave, setAutoSave] = useState(true)

  const handleClearHistory = () => {
    if (confirm("Are you sure you want to clear all chat history? This cannot be undone.")) {
      localStorage.removeItem("conversations")
      alert("Chat history cleared successfully")
    }
  }

  const handleDownloadData = () => {
    const conversations = localStorage.getItem("conversations")
    const data = {
      conversations: conversations ? JSON.parse(conversations) : [],
      exportedAt: new Date().toISOString(),
    }
    const dataStr = JSON.stringify(data, null, 2)
    const dataBlob = new Blob([dataStr], { type: "application/json" })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement("a")
    link.href = url
    link.download = `mm-chat-backup-${Date.now()}.json`
    link.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="h-full flex flex-col bg-background animate-fade-in">
      {/* Header */}
      <div className="border-b border-border p-4 flex items-center gap-4 transition-smooth">
        <Button variant="ghost" size="icon" onClick={onBack} className="btn-hover-scale">
          <ArrowLeft size={20} />
        </Button>
        <h1 className="text-2xl font-bold text-foreground">Settings</h1>
      </div>

      {/* Settings Content */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="max-w-2xl space-y-6">
          {/* Theme Section */}
          <div className="bg-card rounded-lg p-6 border border-border transition-smooth hover:shadow-md animate-slide-in-up">
            <h2 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
              {theme === "light" ? <Sun size={20} /> : <Moon size={20} />}
              Appearance
            </h2>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-foreground font-medium">Theme</p>
                <p className="text-muted-foreground text-sm">{theme === "light" ? "Light Mode" : "Dark Mode"}</p>
              </div>
              <Button
                onClick={toggleTheme}
                variant="outline"
                className="gap-2 bg-transparent btn-hover-scale transition-smooth"
              >
                {theme === "light" ? (
                  <>
                    <Moon size={18} />
                    Dark
                  </>
                ) : (
                  <>
                    <Sun size={18} />
                    Light
                  </>
                )}
              </Button>
            </div>
          </div>

          {/* Notifications Section */}
          <div
            className="bg-card rounded-lg p-6 border border-border transition-smooth hover:shadow-md animate-slide-in-up"
            style={{ animationDelay: "50ms" }}
          >
            <h2 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
              <Bell size={20} />
              Notifications
            </h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-foreground font-medium">Enable Notifications</p>
                  <p className="text-muted-foreground text-sm">Get alerts for new messages</p>
                </div>
                <button
                  onClick={() => setNotifications(!notifications)}
                  className={`relative inline-flex h-8 w-14 items-center rounded-full transition-all duration-300 ${
                    notifications ? "bg-primary" : "bg-muted"
                  }`}
                >
                  <span
                    className={`inline-block h-6 w-6 transform rounded-full bg-white transition-transform duration-300 ${
                      notifications ? "translate-x-7" : "translate-x-1"
                    }`}
                  />
                </button>
              </div>
            </div>
          </div>

          {/* Preferences Section */}
          <div
            className="bg-card rounded-lg p-6 border border-border transition-smooth hover:shadow-md animate-slide-in-up"
            style={{ animationDelay: "100ms" }}
          >
            <h2 className="text-lg font-semibold text-foreground mb-4">Preferences</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-foreground font-medium">Auto-save Conversations</p>
                  <p className="text-muted-foreground text-sm">Automatically save your chats</p>
                </div>
                <button
                  onClick={() => setAutoSave(!autoSave)}
                  className={`relative inline-flex h-8 w-14 items-center rounded-full transition-all duration-300 ${
                    autoSave ? "bg-primary" : "bg-muted"
                  }`}
                >
                  <span
                    className={`inline-block h-6 w-6 transform rounded-full bg-white transition-transform duration-300 ${
                      autoSave ? "translate-x-7" : "translate-x-1"
                    }`}
                  />
                </button>
              </div>
            </div>
          </div>

          {/* Privacy & Security Section */}
          <div
            className="bg-card rounded-lg p-6 border border-border transition-smooth hover:shadow-md animate-slide-in-up"
            style={{ animationDelay: "150ms" }}
          >
            <h2 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
              <Lock size={20} />
              Privacy & Security
            </h2>
            <div className="space-y-3">
              <Button
                variant="outline"
                className="w-full justify-start bg-transparent btn-hover-scale transition-smooth"
              >
                Change Password
              </Button>
              <Button
                variant="outline"
                className="w-full justify-start bg-transparent btn-hover-scale transition-smooth hover:text-destructive"
                onClick={handleClearHistory}
              >
                <Trash2 size={16} className="mr-2" />
                Clear Chat History
              </Button>
              <Button
                variant="outline"
                className="w-full justify-start bg-transparent btn-hover-scale transition-smooth"
                onClick={handleDownloadData}
              >
                <Download size={16} className="mr-2" />
                Download Your Data
              </Button>
            </div>
          </div>

          {/* Help & Support Section */}
          <div
            className="bg-card rounded-lg p-6 border border-border transition-smooth hover:shadow-md animate-slide-in-up"
            style={{ animationDelay: "200ms" }}
          >
            <h2 className="text-lg font-semibold text-foreground mb-4 flex items-center gap-2">
              <HelpCircle size={20} />
              Help & Support
            </h2>
            <div className="space-y-3">
              <Button
                variant="outline"
                className="w-full justify-start bg-transparent btn-hover-scale transition-smooth"
              >
                Documentation
              </Button>
              <Button
                variant="outline"
                className="w-full justify-start bg-transparent btn-hover-scale transition-smooth"
              >
                Contact Support
              </Button>
              <Button
                variant="outline"
                className="w-full justify-start bg-transparent btn-hover-scale transition-smooth"
              >
                Report a Bug
              </Button>
            </div>
          </div>

          {/* Logout Section */}
          <div
            className="bg-card rounded-lg p-6 border border-border transition-smooth hover:shadow-md animate-slide-in-up"
            style={{ animationDelay: "250ms" }}
          >
            <Button onClick={onLogout} variant="destructive" className="w-full gap-2 btn-hover-scale transition-smooth">
              <LogOut size={18} />
              Logout
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
