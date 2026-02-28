import axios from "axios"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
})

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const user = localStorage.getItem("user")
  if (user) {
    const { token } = JSON.parse(user)
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
  }
  return config
})

export const chatAPI = {
  sendMessage: (prompt: string, conversationId?: string) => {
    return apiClient.post("/chat/", {
      prompt,
      conversation_id: conversationId,
    })
  },

  getHistory: (userId: string, limit?: number) => {
    return apiClient.post("/history/", {
      user_id: userId,
      limit: limit || 10
    })
  },

  uploadFile: (file: File) => {
    const formData = new FormData()
    formData.append("file", file)
    return apiClient.post("/documents/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
  },
}

export const hybridChatAPI = {
  sendMessage: (prompt: string, sessionId?: string, userId?: string) => {
    return apiClient.post("/hybrid/chat", {
      prompt,
      session_id: sessionId,
      user_id: userId,
      mode: "chat"
    })
  },
}

export default apiClient
