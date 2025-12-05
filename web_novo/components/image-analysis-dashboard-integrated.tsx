"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Upload, Brain, Activity, AlertCircle, BarChart3 } from "lucide-react"
import { ImageUploader } from "@/components/image-uploader"
import { AnalysisSteps } from "@/components/analysis-steps"
import { ResultCard } from "@/components/result-card"
import { AnalysisResults } from "@/components/analysis-results"

const API_URL = 'http://localhost:5000/api'

export function ImageAnalysisDashboardIntegrated() {
  const [selectedImage, setSelectedImage] = useState<string | null>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisComplete, setAnalysisComplete] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)
  const [analysisResults, setAnalysisResults] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const [threshold, setThreshold] = useState(0.35)
  const [stats, setStats] = useState({
    today: 0,
    accuracy: 98.3,
    critical: 0
  })
  const [currentUser, setCurrentUser] = useState<any>(null)

  // Verificar autenticação
  useEffect(() => {
    const token = localStorage.getItem('neuroai_token')
    const user = localStorage.getItem('neuroai_user')
    
    if (!token || !user) {
      window.location.href = '/login'
      return
    }

    setCurrentUser(JSON.parse(user))
    loadStats()
  }, [])

  // Carregar estatísticas
  const loadStats = async () => {
    try {
      // Aqui você pode buscar dados reais da API
      setStats({
        today: 24,
        accuracy: 98.3,
        critical: 3
      })
    } catch (err) {
      console.error('Erro ao carregar estatísticas:', err)
    }
  }

  const handleImageSelect = (imageUrl: string, file?: File) => {
    setSelectedImage(imageUrl)
    if (file) setSelectedFile(file)
    setAnalysisComplete(false)
    setCurrentStep(0)
    setError(null)
    setAnalysisResults(null)
  }

  const handleStartAnalysis = async () => {
    if (!selectedFile) {
      setError('Por favor, selecione uma imagem')
      return
    }

    setIsAnalyzing(true)
    setError(null)
    setCurrentStep(1)

    try {
      // Etapa 1: Pré-processamento
      await new Promise((resolve) => setTimeout(resolve, 1000))
      setCurrentStep(2)

      // Etapa 2: Predição
      const formData = new FormData()
      formData.append('image', selectedFile)
      formData.append('threshold', threshold.toString())

      const token = localStorage.getItem('neuroai_token')
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      })

      if (!response.ok) {
        throw new Error('Erro ao analisar imagem')
      }

      const data = await response.json()
      
      // DEBUG: Log da resposta
      console.log('Resposta da API:', data)
      
      // Etapa 3: Análise completa
      await new Promise((resolve) => setTimeout(resolve, 1000))
      setCurrentStep(3)

      // Normalizar dados da API - EXATAMENTE como vem do backend
      const normalizedResults = {
        normal: data.predictions?.normal ?? 0,
        tumor: data.predictions?.tumor ?? 0,
        confidence: data.confidence ?? 0,
        predictions: {
          normal: data.predictions?.normal ?? 0,
          tumor: data.predictions?.tumor ?? 0
        }
      }

      console.log('Dados normalizados:', normalizedResults)

      // Salvar no histórico
      await saveToHistory(normalizedResults)

      setAnalysisResults(normalizedResults)
      setAnalysisComplete(true)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao analisar imagem')
      console.error('Erro na análise:', err)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const saveToHistory = async (results: any) => {
    try {
      const token = localStorage.getItem('neuroai_token')
      
      const response = await fetch(`${API_URL}/history`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          image_name: selectedFile?.name,
          prediction_normal: results.normal ?? 0,
          prediction_tumor: results.tumor ?? 0,
          confidence: results.confidence ?? 0,
          threshold_used: threshold,
          result: (results.tumor ?? 0) > threshold ? 'Tumor' : 'Normal'
        })
      })

      if (!response.ok) {
        const error = await response.json()
        console.error('Erro ao salvar histórico:', error)
      } else {
        const data = await response.json()
        console.log('Análise salva com sucesso:', data)
      }
    } catch (err) {
      console.error('Erro ao salvar no histórico:', err)
      // Não bloqueia a análise se falhar o histórico
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Análise de Imagens</h1>
          <p className="text-muted-foreground mt-1">Faça upload de imagens médicas para análise por IA</p>
        </div>
        {currentUser && (
          <div className="text-right">
            <p className="text-sm text-muted-foreground">👤 {currentUser.full_name || currentUser.username}</p>
          </div>
        )}
      </div>

      {/* Stats Cards */}
      <div className="grid md:grid-cols-3 gap-6">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Análises Hoje</p>
                <p className="text-3xl font-bold text-foreground mt-1">{stats.today}</p>
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
                <p className="text-3xl font-bold text-foreground mt-1">{stats.accuracy.toFixed(1)}%</p>
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
                <p className="text-3xl font-bold text-foreground mt-1">{stats.critical}</p>
              </div>
              <div className="w-12 h-12 bg-destructive/10 rounded-lg flex items-center justify-center">
                <AlertCircle className="w-6 h-6 text-destructive" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Error Message */}
      {error && (
        <Card className="border-destructive/50 bg-destructive/10">
          <CardContent className="pt-6 flex gap-3 items-start">
            <AlertCircle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-destructive">Erro na análise</p>
              <p className="text-sm text-destructive/80">{error}</p>
            </div>
          </CardContent>
        </Card>
      )}

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

              {/* Threshold Control */}
              {selectedImage && (
                <div className="mt-6 space-y-2">
                  <div className="flex items-center justify-between">
                    <label className="text-sm font-medium">Limiar de Confiança: {(threshold * 100).toFixed(1)}%</label>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.01"
                    value={threshold}
                    onChange={(e) => setThreshold(parseFloat(e.target.value))}
                    className="w-full"
                  />
                  <p className="text-xs text-muted-foreground">
                    Ajuste o limiar para classificações mais agressivas (menor) ou conservadoras (maior)
                  </p>
                </div>
              )}

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

          {/* Results */}
          {analysisResults && analysisComplete && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="w-5 h-5" />
                  Resultados Detalhados
                </CardTitle>
              </CardHeader>
              <CardContent>
                <AnalysisResults results={analysisResults} threshold={threshold} />
              </CardContent>
            </Card>
          )}
        </div>

        {/* Result Section */}
        <div>
          <ResultCard 
            isAnalyzing={isAnalyzing} 
            analysisComplete={analysisComplete}
            results={analysisResults}
            threshold={threshold}
          />
        </div>
      </div>
    </div>
  )
}
