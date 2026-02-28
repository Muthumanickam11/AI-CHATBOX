"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import AuthPage from "@/components/auth-page"
import ChatLayout from "@/components/chat-layout"

export default function Home() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [theme, setTheme] = useState<"light" | "dark">("light")
  const [mounted, setMounted] = useState(false)
  const router = useRouter()

  useEffect(() => {
    setMounted(true)
    // Check if user is authenticated (stored in localStorage)
    const user = localStorage.getItem("user")
    if (user) {
      setIsAuthenticated(true)
    }

    const savedTheme = localStorage.getItem("theme") as "light" | "dark" | null
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches
    const initialTheme = savedTheme || (prefersDark ? "dark" : "light")
    setTheme(initialTheme)
    document.documentElement.classList.toggle("dark", initialTheme === "dark")

    setIsLoading(false)
  }, [])

  const toggleTheme = () => {
    const newTheme = theme === "light" ? "dark" : "light"
    setTheme(newTheme)
    localStorage.setItem("theme", newTheme)
    document.documentElement.classList.toggle("dark", newTheme === "dark")
  }

  if (isLoading || !mounted) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-foreground">Loading...</p>
        </div>
      </div>
    )
  }

  return isAuthenticated ? (
    <ChatLayout onLogout={() => setIsAuthenticated(false)} theme={theme} toggleTheme={toggleTheme} />
  ) : (
    <AuthPage onAuthenticate={() => setIsAuthenticated(true)} />
  )
}
