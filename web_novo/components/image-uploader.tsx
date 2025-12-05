"use client"

import type React from "react"

import { useCallback } from "react"
import { Upload, X, ImageIcon } from "lucide-react"
import { Button } from "@/components/ui/button"

interface ImageUploaderProps {
  onImageSelect: (imageUrl: string, file?: File) => void
  selectedImage: string | null
}

export function ImageUploader({ onImageSelect, selectedImage }: ImageUploaderProps) {
  const handleFileSelect = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0]
      if (file && file.type.startsWith("image/")) {
        const reader = new FileReader()
        reader.onload = () => {
          onImageSelect(reader.result as string, file)
        }
        reader.readAsDataURL(file)
      }
    },
    [onImageSelect],
  )

  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault()
      const file = e.dataTransfer.files[0]
      if (file && file.type.startsWith("image/")) {
        const reader = new FileReader()
        reader.onload = () => {
          onImageSelect(reader.result as string, file)
        }
        reader.readAsDataURL(file)
      }
    },
    [onImageSelect],
  )

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
  }

  const handleClear = () => {
    onImageSelect("")
  }

  if (selectedImage) {
    return (
      <div className="relative">
        <div className="relative bg-muted rounded-lg overflow-hidden border-2 border-border">
          <img
            src={selectedImage || "/placeholder.svg"}
            alt="Selected medical scan"
            className="w-full h-auto object-contain max-h-96"
          />
        </div>
        <Button variant="destructive" size="icon" className="absolute top-2 right-2" onClick={handleClear}>
          <X className="w-4 h-4" />
        </Button>
      </div>
    )
  }

  return (
    <div
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      className="border-2 border-dashed border-border rounded-lg p-12 text-center hover:border-primary/50 transition-colors cursor-pointer bg-muted/30"
      onClick={() => document.getElementById("file-upload")?.click()}
    >
      <input id="file-upload" type="file" accept="image/*" className="hidden" onChange={handleFileSelect} />

      <div className="flex flex-col items-center gap-4">
        <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center">
          <ImageIcon className="w-8 h-8 text-primary" />
        </div>
        <div>
          <p className="text-lg font-medium text-foreground">Arraste uma imagem aqui</p>
          <p className="text-sm text-muted-foreground mt-1">ou clique para selecionar</p>
        </div>
        <Button type="button" variant="outline" className="gap-2 bg-transparent">
          <Upload className="w-4 h-4" />
          Selecionar Arquivo
        </Button>
        <p className="text-xs text-muted-foreground">Formatos suportados: PNG, JPG, DICOM (até 50MB)</p>
      </div>
    </div>
  )
}
