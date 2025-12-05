"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { AlertTriangle, FileText, Loader2 } from "lucide-react"
import Link from "next/link"

interface ResultCardProps {
  isAnalyzing: boolean
  analysisComplete: boolean
  results?: any
  threshold?: number
}

export function ResultCard({ isAnalyzing, analysisComplete, results, threshold = 0.35 }: ResultCardProps) {
  if (!isAnalyzing && !analysisComplete) {
    return (
      <Card className="h-fit">
        <CardHeader>
          <CardTitle>Resultado</CardTitle>
          <CardDescription>O resultado aparecerá aqui após a análise</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mx-auto mb-4">
              <FileText className="w-8 h-8 text-muted-foreground" />
            </div>
            <p className="text-sm text-muted-foreground">Aguardando upload e análise</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (isAnalyzing) {
    return (
      <Card className="h-fit border-primary/50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Loader2 className="w-5 h-5 animate-spin text-primary" />
            Analisando...
          </CardTitle>
          <CardDescription>Processamento em andamento</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="text-center py-8">
              <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Loader2 className="w-10 h-10 text-primary animate-spin" />
              </div>
              <p className="text-sm text-muted-foreground">Inteligência artificial analisando imagem...</p>
            </div>

            <div className="space-y-2 pt-4 border-t border-border">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Modelo</span>
                <span className="font-medium text-foreground">ResNet-50</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Tempo estimado</span>
                <span className="font-medium text-foreground">~6 segundos</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  // Analysis Complete
  const prediction_normal = results?.normal ?? results?.prediction_normal ?? 0
  const prediction_tumor = results?.tumor ?? results?.prediction_tumor ?? 0
  const isTumor = prediction_tumor > threshold
  const tumorPercent = (prediction_tumor * 100).toFixed(1)
  const normalPercent = (prediction_normal * 100).toFixed(1)

  console.log('ResultCard Debug:', { results, prediction_tumor, prediction_normal, threshold, isTumor })

  return (
    <Card className={`h-fit ${isTumor ? "border-destructive/50" : "border-accent/50"}`}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <AlertTriangle className={`w-5 h-5 ${isTumor ? "text-destructive" : "text-accent"}`} />
          Resultado Principal
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className={`${isTumor ? "bg-destructive/10 border-destructive/50" : "bg-accent/10 border-accent/50"} border-2 rounded-lg p-6 text-center`}>
          <AlertTriangle className={`w-12 h-12 ${isTumor ? "text-destructive" : "text-accent"} mx-auto mb-3`} />
          <div className={`text-2xl font-bold ${isTumor ? "text-destructive" : "text-accent"} mb-2`}>
            {isTumor ? "TUMOR DETECTADO" : "RESULTADO NORMAL"}
          </div>
          <div className="text-sm text-muted-foreground">
            Confiança: <span className="font-bold text-foreground">{tumorPercent}%</span>
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
            <span className="text-sm text-muted-foreground">Probabilidade Normal</span>
            <span className="font-bold text-foreground">{normalPercent}%</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
            <span className="text-sm text-muted-foreground">Probabilidade Tumor</span>
            <span className={`font-bold ${isTumor ? "text-destructive" : "text-accent"}`}>{tumorPercent}%</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
            <span className="text-sm text-muted-foreground">Limiar Aplicado</span>
            <span className="font-bold text-foreground">{(threshold * 100).toFixed(1)}%</span>
          </div>
        </div>

        <div className="pt-4 border-t border-border space-y-3">
          <div className="bg-card rounded-lg p-4 border border-border">
            <div className="text-xs font-semibold text-primary mb-2">INFORMAÇÕES DA ANÁLISE</div>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Timestamp</span>
                <span className="font-mono text-xs text-foreground">{new Date().toLocaleString("pt-BR")}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Modelo</span>
                <span className="font-medium text-foreground">ResNet-50</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Tempo de Análise</span>
                <span className="font-medium text-foreground">5.8s</span>
              </div>
            </div>
          </div>

          <div className="bg-amber-500/10 border border-amber-500/20 rounded-lg p-4">
            <div className="flex items-start gap-2">
              <AlertTriangle className="w-5 h-5 text-amber-600 dark:text-amber-400 mt-0.5 flex-shrink-0" />
              <div className="text-sm">
                <div className="font-semibold text-amber-700 dark:text-amber-400 mb-1">Interpretação Clínica</div>
                <p className="text-amber-900/80 dark:text-amber-200/80 text-xs leading-relaxed">
                  A IA identificou padrões consistentes com presença de tumor cerebral. Análise médica complementar é
                  necessária.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-2">
          <Link href="/dashboard/analysis/1">
            <Button className="w-full gap-2">
              <FileText className="w-4 h-4" />
              Gerar Relatório Completo
            </Button>
          </Link>
          <Button variant="outline" className="w-full bg-transparent">
            Salvar Resultado
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
