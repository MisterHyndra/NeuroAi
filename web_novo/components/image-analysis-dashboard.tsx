"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Upload, Brain, Activity, AlertCircle } from "lucide-react"
import { ImageUploader } from "@/components/image-uploader"
import { AnalysisSteps } from "@/components/analysis-steps"
import { ResultCard } from "@/components/result-card"

export function ImageAnalysisDashboard() {
  const [selectedImage, setSelectedImage] = useState<string | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisComplete, setAnalysisComplete] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)

  const handleImageSelect = (imageUrl: string) => {
    setSelectedImage(imageUrl)
    setAnalysisComplete(false)
    setCurrentStep(0)
  }

  const handleStartAnalysis = async () => {
    if (!selectedImage) return

    setIsAnalyzing(true)
    setCurrentStep(1)

    // Simulate analysis steps
    await new Promise((resolve) => setTimeout(resolve, 2000))
    setCurrentStep(2)

    await new Promise((resolve) => setTimeout(resolve, 2000))
    setCurrentStep(3)

    await new Promise((resolve) => setTimeout(resolve, 2000))
    setIsAnalyzing(false)
    setAnalysisComplete(true)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground">Análise de Imagens</h1>
        <p className="text-muted-foreground mt-1">Faça upload de imagens médicas para análise por IA</p>
      </div>

      {/* Stats Cards */}
      <div className="grid md:grid-cols-3 gap-6">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Análises Hoje</p>
                <p className="text-3xl font-bold text-foreground mt-1">24</p>
              </div>
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                <Activity className="w-6 h-6 text-primary" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Precisão Média</p>
                <p className="text-3xl font-bold text-foreground mt-1">98.3%</p>
              </div>
              <div className="w-12 h-12 bg-accent/10 rounded-lg flex items-center justify-center">
                <Brain className="w-6 h-6 text-accent" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Casos Críticos</p>
                <p className="text-3xl font-bold text-foreground mt-1">3</p>
              </div>
              <div className="w-12 h-12 bg-destructive/10 rounded-lg flex items-center justify-center">
                <AlertCircle className="w-6 h-6 text-destructive" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Analysis Area */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Upload Section */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="w-5 h-5" />
                Carregar Imagem
              </CardTitle>
              <CardDescription>Arraste e solte ou clique para selecionar uma imagem médica</CardDescription>
            </CardHeader>
            <CardContent>
              <ImageUploader onImageSelect={handleImageSelect} selectedImage={selectedImage} />

              {selectedImage && !isAnalyzing && !analysisComplete && (
                <div className="mt-4 flex justify-end">
                  <Button onClick={handleStartAnalysis} size="lg" className="gap-2">
                    <Brain className="w-5 h-5" />
                    Iniciar Diagnóstico
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Analysis Steps */}
          {(isAnalyzing || analysisComplete) && (
            <AnalysisSteps currentStep={currentStep} isAnalyzing={isAnalyzing} selectedImage={selectedImage} />
          )}
        </div>

        {/* Result Section */}
        <div>
          <ResultCard isAnalyzing={isAnalyzing} analysisComplete={analysisComplete} />
        </div>
      </div>
    </div>
  )
}
