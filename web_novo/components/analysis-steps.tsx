"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Check, Loader2 } from "lucide-react"
import { cn } from "@/lib/utils"

interface AnalysisStepsProps {
  currentStep: number
  isAnalyzing: boolean
  selectedImage: string | null
}

const steps = [
  { id: 1, name: "Imagem Original", description: "Processamento inicial" },
  { id: 2, name: "Análise Quantitativa", description: "Extração de características" },
  { id: 3, name: "Mapa de Ativação", description: "Identificação de regiões" },
]

export function AnalysisSteps({ currentStep, isAnalyzing, selectedImage }: AnalysisStepsProps) {
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
                    <div className="text-xs text-muted-foreground">Densidade Média</div>
                    <div className="text-lg font-bold text-foreground">42.3 HU</div>
                  </div>
                  <div className="absolute top-4 right-4 bg-card/90 backdrop-blur p-3 rounded-lg border border-border">
                    <div className="text-xs text-muted-foreground">Área Analisada</div>
                    <div className="text-lg font-bold text-foreground">1,234 mm²</div>
                  </div>
                </>
              ) : (
                <div className="h-80 flex items-center justify-center text-muted-foreground">Aguardando análise...</div>
              )}
            </div>
          </TabsContent>

          <TabsContent value="step-3" className="mt-4">
            <div className="bg-muted rounded-lg overflow-hidden border border-border relative">
              {selectedImage ? (
                <>
                  <img
                    src={selectedImage || "/placeholder.svg"}
                    alt="Activation map"
                    className="w-full h-auto object-contain max-h-80 opacity-60"
                  />
                  <div className="absolute inset-0 bg-gradient-to-br from-destructive/30 via-transparent to-transparent">
                    <div className="absolute top-1/3 right-1/3 w-24 h-24 bg-destructive/40 rounded-full blur-xl animate-pulse" />
                  </div>
                  <div className="absolute bottom-4 left-4 right-4 bg-card/90 backdrop-blur p-3 rounded-lg border border-border">
                    <div className="flex items-center justify-between">
                      <div className="text-sm font-medium text-foreground">Região de interesse identificada</div>
                      <div className="text-xs text-destructive font-semibold">Atenção requerida</div>
                    </div>
                  </div>
                </>
              ) : (
                <div className="h-80 flex items-center justify-center text-muted-foreground">Aguardando análise...</div>
              )}
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}
