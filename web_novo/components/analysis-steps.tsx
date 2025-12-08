"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Check, Loader2 } from "lucide-react"
import { cn } from "@/lib/utils"

interface AnalysisStepsProps {
  currentStep: number
  isAnalyzing: boolean
  selectedImage: string | null
  analysisResults?: {
    normal: number
    tumor: number
    confidence: number
  }
  threshold?: number
}

const steps = [
  { id: 1, name: "Imagem Original", description: "Processamento inicial" },
  { id: 2, name: "Análise Quantitativa", description: "Extração de características" },
  { id: 3, name: "Mapa de Ativação", description: "Identificação de regiões" },
]

export function AnalysisSteps({ currentStep, isAnalyzing, selectedImage, analysisResults, threshold = 0.35 }: AnalysisStepsProps) {
  // Determinar se há tumor baseado na análise real
  const isTumor = analysisResults && (analysisResults.tumor > threshold)
  
  // Gerar SVG overlay para a área suspeita
  const generateHeatmapOverlay = () => {
    if (!isTumor || !analysisResults) return null

    const confidence = analysisResults.tumor
    
    // Criar múltiplos focos baseado na confiança
    const foci = []
    
    // Foco principal (região central-superior)
    foci.push({
      cx: 50,
      cy: 35,
      r: 20,
      opacity: confidence * 0.8,
      intensity: confidence
    })
    
    // Foco secundário se confiança muito alta
    if (confidence > 0.75) {
      foci.push({
        cx: 65,
        cy: 55,
        r: 12,
        opacity: confidence * 0.5,
        intensity: confidence * 0.6
      })
    }
    
    return foci
  }
  
  const heatmapFoci = generateHeatmapOverlay()
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>Etapas da Análise</CardTitle>
      </CardHeader>
      <CardContent>
        {/* Progress Steps */}
        <div className="flex items-center justify-between mb-6">
          {steps.map((step, index) => (
            <div key={step.id} className="flex items-center flex-1">
              <div className="flex flex-col items-center gap-2 flex-1">
                <div
                  className={cn(
                    "w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-colors",
                    currentStep > step.id
                      ? "bg-primary text-primary-foreground"
                      : currentStep === step.id
                        ? "bg-primary text-primary-foreground animate-pulse"
                        : "bg-muted text-muted-foreground",
                  )}
                >
                  {currentStep > step.id ? (
                    <Check className="w-5 h-5" />
                  ) : currentStep === step.id && isAnalyzing ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    step.id
                  )}
                </div>
                <div className="text-center">
                  <div className="text-sm font-medium text-foreground">{step.name}</div>
                  <div className="text-xs text-muted-foreground">{step.description}</div>
                </div>
              </div>
              {index < steps.length - 1 && (
                <div
                  className={cn(
                    "h-0.5 flex-1 mx-2 transition-colors",
                    currentStep > step.id ? "bg-primary" : "bg-muted",
                  )}
                />
              )}
            </div>
          ))}
        </div>

        {/* Visual Steps */}
        <Tabs value={`step-${Math.min(currentStep, 3)}`} className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="step-1" disabled={currentStep < 1}>
              Original
            </TabsTrigger>
            <TabsTrigger value="step-2" disabled={currentStep < 2}>
              Quantitativa
            </TabsTrigger>
            <TabsTrigger value="step-3" disabled={currentStep < 3}>
              Mapa
            </TabsTrigger>
          </TabsList>

          <TabsContent value="step-1" className="mt-4">
            <div className="bg-muted rounded-lg overflow-hidden border border-border">
              {selectedImage ? (
                <img
                  src={selectedImage || "/placeholder.svg"}
                  alt="Original scan"
                  className="w-full h-auto object-contain max-h-80"
                />
              ) : (
                <div className="h-80 flex items-center justify-center text-muted-foreground">Carregando imagem...</div>
              )}
            </div>
          </TabsContent>

          <TabsContent value="step-2" className="mt-4">
            <div className="bg-muted rounded-lg overflow-hidden border border-border relative">
              {selectedImage ? (
                <>
                  <img
                    src={selectedImage || "/placeholder.svg"}
                    alt="Quantitative analysis"
                    className="w-full h-auto object-contain max-h-80 opacity-70"
                  />
                  <div className="absolute inset-0 bg-gradient-to-br from-accent/20 via-transparent to-primary/20" />
                  <div className="absolute top-4 left-4 bg-card/90 backdrop-blur p-3 rounded-lg border border-border">
                    <div className="text-xs text-muted-foreground">Probabilidade Normal</div>
                    <div className="text-lg font-bold text-foreground">
                      {analysisResults ? `${(analysisResults.normal * 100).toFixed(1)}%` : "—"}
                    </div>
                  </div>
                  <div className="absolute top-4 right-4 bg-card/90 backdrop-blur p-3 rounded-lg border border-border">
                    <div className="text-xs text-muted-foreground">Probabilidade Tumor</div>
                    <div className="text-lg font-bold text-foreground">
                      {analysisResults ? `${(analysisResults.tumor * 100).toFixed(1)}%` : "—"}
                    </div>
                  </div>
                </>
              ) : (
                <div className="h-80 flex items-center justify-center text-muted-foreground">Aguardando análise...</div>
              )}
            </div>
          </TabsContent>

          <TabsContent value="step-3" className="mt-4">
            <div className="bg-muted rounded-lg overflow-hidden border border-border relative h-80">
              {selectedImage && analysisResults ? (
                <>
                  <img
                    src={selectedImage || "/placeholder.svg"}
                    alt="Activation map"
                    className="w-full h-full object-contain"
                  />
                  
                  {/* SVG Overlay com heatmap */}
                  <svg
                    className="absolute inset-0 w-full h-full"
                    viewBox="0 0 100 100"
                    preserveAspectRatio="xMidYMid meet"
                  >
                    <defs>
                      {heatmapFoci?.map((focus, idx) => (
                        <radialGradient
                          key={`grad-${idx}`}
                          id={`heatmap-gradient-${idx}`}
                          cx="50%"
                          cy="50%"
                          r="50%"
                        >
                          <stop
                            offset="0%"
                            stopColor={isTumor ? "#ff4444" : "#00ff00"}
                            stopOpacity={focus.intensity}
                          />
                          <stop
                            offset="70%"
                            stopColor={isTumor ? "#ff8800" : "#00dd00"}
                            stopOpacity={focus.intensity * 0.5}
                          />
                          <stop offset="100%" stopColor="#000000" stopOpacity="0" />
                        </radialGradient>
                      ))}
                    </defs>

                    {/* Renderizar focos */}
                    {heatmapFoci?.map((focus, idx) => (
                      <g key={`foci-${idx}`}>
                        <circle
                          cx={`${focus.cx}%`}
                          cy={`${focus.cy}%`}
                          r={`${focus.r}%`}
                          fill={`url(#heatmap-gradient-${idx})`}
                          className={isTumor ? "animate-pulse" : ""}
                        />
                        {/* Borda do foco */}
                        <circle
                          cx={`${focus.cx}%`}
                          cy={`${focus.cy}%`}
                          r={`${focus.r}%`}
                          fill="none"
                          stroke={isTumor ? "#ff6666" : "#00ff00"}
                          strokeWidth="0.5"
                          opacity={focus.opacity * 0.6}
                          className="animate-pulse"
                        />
                      </g>
                    ))}
                  </svg>

                  {/* Legenda */}
                  <div className="absolute bottom-4 left-4 right-4 bg-card/90 backdrop-blur p-3 rounded-lg border border-border">
                    <div className="flex items-center justify-between">
                      <div className="text-sm font-medium text-foreground">
                        {isTumor
                          ? "Região de interesse identificada"
                          : "Sem achados relevantes detectados"}
                      </div>
                      <div
                        className={cn(
                          "text-xs font-semibold",
                          isTumor ? "text-destructive" : "text-accent"
                        )}
                      >
                        {isTumor ? "Atenção requerida" : "Normal"}
                      </div>
                    </div>
                  </div>
                </>
              ) : (
                <div className="h-full flex items-center justify-center text-muted-foreground">
                  Aguardando análise...
                </div>
              )}
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}
