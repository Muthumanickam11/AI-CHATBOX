export interface Message {
  id: string
  content: string
  role: "user" | "assistant"
  timestamp: string
  files?: Array<{ name: string; size: number }>
}

export interface Conversation {
  id: string
  title: string
  messages: Message[]
  createdAt: string
  updatedAt: string
}

export interface User {
  id: string
  email: string
}
