"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import apiClient from "@/lib/api"

interface AuthPageProps {
  onAuthenticate: () => void
}

export default function AuthPage({ onAuthenticate }: AuthPageProps) {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [isSignUp, setIsSignUp] = useState(false)
  const [error, setError] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setIsLoading(true)

    try {
      const cleanEmail = email.trim()
      const cleanPassword = password.trim()

      if (!cleanEmail || !cleanPassword) {
        setError("Please fill in all fields")
        setIsLoading(false)
        return
      }

      const endpoint = isSignUp ? "/auth/signup" : "/auth/login"
      const response = await apiClient.post(endpoint, {
        email: cleanEmail,
        password: cleanPassword,
      })

      const userData = response.data
      if (userData.login_status === "success" || userData.token) {
        localStorage.setItem("user", JSON.stringify({
          email,
          id: userData.user_id,
          token: userData.token
        }))
        localStorage.setItem("conversations", JSON.stringify([]))
        onAuthenticate()
      } else {
        setError("Authentication failed. Please check your credentials.")
      }
    } catch (err: any) {
      console.error("Auth error:", err)
      const detail = err.response?.data?.detail || "Authentication failed. Please try again."
      setError(typeof detail === 'string' ? detail : "Authentication failed.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-card flex items-center justify-center p-4">
      <Card className="w-full max-w-md p-8 shadow-lg">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-foreground mb-2">MM CHAT ASSISTANT</h1>
          <p className="text-muted-foreground">{isSignUp ? "Create your account" : "Welcome back"}</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">Email</label>
            <Input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              disabled={isLoading}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-2">Password</label>
            <Input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              disabled={isLoading}
            />
          </div>

          {error && (
            <div className="p-3 bg-destructive/10 border border-destructive/20 rounded-md text-destructive text-sm">
              {error}
            </div>
          )}

          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? "Loading..." : isSignUp ? "Sign Up" : "Sign In"}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-sm text-muted-foreground">
            {isSignUp ? "Already have an account?" : "Don't have an account?"}
            <button onClick={() => setIsSignUp(!isSignUp)} className="ml-2 text-primary hover:underline font-medium">
              {isSignUp ? "Sign In" : "Sign Up"}
            </button>
          </p>
        </div>
      </Card>
    </div>
  )
}
