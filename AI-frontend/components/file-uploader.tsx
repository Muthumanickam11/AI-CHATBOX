"use client"

import type React from "react"

import { useRef } from "react"
import { Button } from "@/components/ui/button"
import { Paperclip } from "lucide-react"

interface FileUploaderProps {
  onFilesSelected: (files: File[]) => void
}

export default function FileUploader({ onFilesSelected }: FileUploaderProps) {
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    if (files.length > 0) {
      onFilesSelected(files)
    }
    // Reset input
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  return (
    <>
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept=".pdf,.txt,.doc,.docx"
        onChange={handleFileChange}
        className="hidden"
      />
      <Button type="button" variant="outline" size="icon" onClick={() => fileInputRef.current?.click()}>
        <Paperclip size={20} />
      </Button>
    </>
  )
}
