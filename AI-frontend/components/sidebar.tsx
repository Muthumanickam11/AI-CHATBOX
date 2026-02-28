"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Plus, Trash2, LogOut, Settings } from "lucide-react"
import type { Conversation } from "@/types"

interface SidebarProps {
  onLogout: () => void
  onSettings: () => void
}

export default function Sidebar({ onLogout, onSettings }: SidebarProps) {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [selectedId, setSelectedId] = useState<string | null>(null)

  useEffect(() => {
    const stored = localStorage.getItem("conversations")
    if (stored) {
      const convs = JSON.parse(stored)
      setConversations(convs)
      if (convs.length > 0) {
        setSelectedId(convs[0].id)
      }
    }
  }, [])

  const handleNewChat = () => {
    const newConversation: Conversation = {
      id: Date.now().toString(),
      title: "New Chat",
      messages: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }
    const updated = [newConversation, ...conversations]
    setConversations(updated)
    localStorage.setItem("conversations", JSON.stringify(updated))
    setSelectedId(newConversation.id)
  }

  const handleDelete = (id: string) => {
    const updated = conversations.filter((c) => c.id !== id)
    setConversations(updated)
    localStorage.setItem("conversations", JSON.stringify(updated))
    if (selectedId === id) {
      setSelectedId(updated.length > 0 ? updated[0].id : null)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem("user")
    localStorage.removeItem("conversations")
    onLogout()
  }

  return (
    <div className="h-full bg-sidebar text-sidebar-foreground flex flex-col p-4 transition-smooth">
      <Button
        onClick={handleNewChat}
        className="w-full mb-4 bg-sidebar-primary hover:bg-sidebar-primary/90 btn-hover-scale"
      >
        <Plus size={18} className="mr-2" />
        New Chat
      </Button>

      <div className="flex-1 overflow-y-auto space-y-2">
        {conversations.map((conv, idx) => (
          <div
            key={conv.id}
            className={`p-3 rounded-lg cursor-pointer transition-all duration-200 flex items-center justify-between group animate-slide-in-left ${
              selectedId === conv.id
                ? "bg-sidebar-accent text-sidebar-accent-foreground shadow-md"
                : "hover:bg-sidebar-accent/50"
            }`}
            style={{ animationDelay: `${idx * 50}ms` }}
            onClick={() => setSelectedId(conv.id)}
          >
            <span className="truncate text-sm font-medium">{conv.title}</span>
            <button
              onClick={(e) => {
                e.stopPropagation()
                handleDelete(conv.id)
              }}
              className="opacity-0 group-hover:opacity-100 transition-opacity duration-200 hover:text-destructive"
            >
              <Trash2 size={16} />
            </button>
          </div>
        ))}
      </div>

      <div className="space-y-2 mt-4">
        <Button
          onClick={onSettings}
          variant="ghost"
          className="w-full text-sidebar-foreground hover:bg-sidebar-accent/20 justify-start transition-smooth btn-hover-scale"
        >
          <Settings size={18} className="mr-2" />
          Settings
        </Button>
        <Button
          onClick={handleLogout}
          variant="ghost"
          className="w-full text-sidebar-foreground hover:bg-sidebar-accent/20 justify-start transition-smooth btn-hover-scale"
        >
          <LogOut size={18} className="mr-2" />
          Logout
        </Button>
      </div>
    </div>
  )
}
