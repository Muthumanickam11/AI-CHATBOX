"use client"

import { formatDistanceToNow } from "date-fns"
import { Paperclip } from "lucide-react"
import type { Message as MessageType } from "@/types"

interface MessageProps {
  message: MessageType
}

export default function Message({ message }: MessageProps) {
  const isUser = message.role === "user"

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} animate-slide-in-up`}>
      <div
        className={`max-w-xs lg:max-w-md xl:max-w-lg px-4 py-3 rounded-lg transition-smooth ${
          isUser
            ? "bg-primary text-primary-foreground rounded-br-none shadow-md hover:shadow-lg"
            : "bg-card text-card-foreground border border-border rounded-bl-none shadow-sm hover:shadow-md"
        }`}
      >
        <p className="text-sm leading-relaxed break-words">{message.content}</p>

        {message.files && message.files.length > 0 && (
          <div className="mt-2 space-y-1">
            {message.files.map((file, idx) => (
              <div
                key={idx}
                className="flex items-center gap-2 text-xs opacity-75 hover:opacity-100 transition-opacity"
              >
                <Paperclip size={14} />
                <span>{file.name}</span>
              </div>
            ))}
          </div>
        )}

        <p className="text-xs opacity-60 mt-2">
          {formatDistanceToNow(new Date(message.timestamp), { addSuffix: true })}
        </p>
      </div>
    </div>
  )
}
