"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import Message from "@/components/message"
import FileUploader from "@/components/file-uploader"
import { Send, Paperclip, Zap, Bot } from "lucide-react"
import type { Message as MessageType } from "@/types"
import { chatAPI, hybridChatAPI } from "@/lib/api"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

export default function ChatBox() {
  const [messages, setMessages] = useState<MessageType[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([])
  const [chatMode, setChatMode] = useState<"standard" | "hybrid">("standard")
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isLoading])

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() && uploadedFiles.length === 0) return

    const userMessage: MessageType = {
      id: Date.now().toString(),
      content: input,
      role: "user",
      timestamp: new Date().toISOString(),
      files: uploadedFiles.map((f) => ({ name: f.name, size: f.size })),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setUploadedFiles([])
    setIsLoading(true)

    try {
      let response
      if (chatMode === "hybrid") {
        response = await hybridChatAPI.sendMessage(input)
      } else {
        response = await chatAPI.sendMessage(input)
      }

      const assistantMessage: MessageType = {
        id: (Date.now() + 1).toString(),
        content: response.data.reply || response.data.answer || "No response received",
        role: "assistant",
        timestamp: new Date().toISOString(),
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (error: any) {
      console.error("Error sending message:", error)
      const assistantMessage: MessageType = {
        id: (Date.now() + 1).toString(),
        content: "Error: Could not connect to the backend. Please ensure the server is running on port 8000.",
        role: "assistant",
        timestamp: new Date().toISOString(),
      }
      setMessages((prev) => [...prev, assistantMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleFileUpload = (files: File[]) => {
    setUploadedFiles((prev) => [...prev, ...files])
  }

  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full animate-fade-in">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-foreground mb-2">Start a Conversation</h2>
              <p className="text-muted-foreground">Ask me anything or upload documents to get started</p>
            </div>
          </div>
        ) : (
          messages.map((msg) => <Message key={msg.id} message={msg} />)
        )}
        {isLoading && (
          <div className="flex justify-start animate-slide-in-left">
            <div className="bg-card text-card-foreground border border-border rounded-lg rounded-bl-none px-4 py-3">
              <div className="flex gap-1">
                <div
                  className="w-2 h-2 bg-muted-foreground rounded-full animate-pulse-dot"
                  style={{ animationDelay: "0ms" }}
                />
                <div
                  className="w-2 h-2 bg-muted-foreground rounded-full animate-pulse-dot"
                  style={{ animationDelay: "150ms" }}
                />
                <div
                  className="w-2 h-2 bg-muted-foreground rounded-full animate-pulse-dot"
                  style={{ animationDelay: "300ms" }}
                />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-border bg-card p-4 transition-smooth">
        {uploadedFiles.length > 0 && (
          <div className="mb-4 flex flex-wrap gap-2 animate-slide-in-up">
            {uploadedFiles.map((file, idx) => (
              <div
                key={idx}
                className="flex items-center gap-2 bg-muted px-3 py-2 rounded-lg text-sm transition-smooth hover:bg-muted/80"
              >
                <Paperclip size={16} />
                <span className="truncate max-w-xs">{file.name}</span>
                <button
                  onClick={() => setUploadedFiles((prev) => prev.filter((_, i) => i !== idx))}
                  className="text-muted-foreground hover:text-foreground transition-colors"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        )}

        <form onSubmit={handleSendMessage} className="flex gap-2 items-center">
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  type="button"
                  variant="outline"
                  size="icon"
                  onClick={() => setChatMode(chatMode === "standard" ? "hybrid" : "standard")}
                  className={`shrink-0 transition-all ${chatMode === "hybrid" ? "border-primary text-primary" : ""}`}
                >
                  {chatMode === "hybrid" ? <Zap size={20} /> : <Bot size={20} />}
                </Button>
              </TooltipTrigger>
              <TooltipContent>
                <p>Switch to {chatMode === "standard" ? "Hybrid (Fast)" : "Standard"} Chat</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>

          <FileUploader onFilesSelected={handleFileUpload} />
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={`Type your ${chatMode} message...`}
            disabled={isLoading}
            className="flex-1 input-focus-ring"
          />
          <Button
            type="submit"
            disabled={isLoading || (!input.trim() && uploadedFiles.length === 0)}
            size="icon"
            className="btn-hover-scale"
          >
            <Send size={20} />
          </Button>
        </form>
      </div>
    </div>
  )
}
