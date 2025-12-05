"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { AlertTriangle, Download, Printer, Share2, Calendar, User, FileText } from "lucide-react"

export function AnalysisResults({ results, threshold = 0.35 }: { results: any; threshold?: number }) {
  if (!results) return null

  // Normalizar dados da API - EXATAMENTE como o backup original
  const prediction_normal = results?.normal ?? results?.prediction_normal ?? 0
  const prediction_tumor = results?.tumor ?? results?.prediction_tumor ?? 0
  const isTumor = prediction_tumor > threshold
  const confidence = (prediction_tumor * 100).toFixed(1)
  const uncertainty = (prediction_normal * 100).toFixed(1)

  console.log('AnalysisResults Debug:', { results, threshold, isTumor, confidence, prediction_tumor, prediction_normal })

  return (
    <div className="space-y-6">
      {/* Header Card */}
      <Card className={isTumor ? "border-destructive/50" : "border-accent/50"}>
        <CardContent className="pt-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div className="flex items-start gap-4">
              <div className={`w-16 h-16 ${isTumor ? "bg-destructive/10" : "bg-accent/10"} rounded-xl flex items-center justify-center`}>
                <AlertTriangle className={`w-8 h-8 ${isTumor ? "text-destructive" : "text-accent"}`} />
              </div>
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <h2 className="text-2xl font-bold text-foreground">
                    {isTumor ? "TUMOR DETECTADO" : "RESULTADO NORMAL"}
                  </h2>
                  <Badge variant={isTumor ? "destructive" : "secondary"}>
                    {isTumor ? "Atenção Requerida" : "Sem Anomalias"}
                  </Badge>
                </div>
                <div className="space-y-1 text-sm text-muted-foreground">
                  <div className="flex items-center gap-4">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-4 h-4" />
                      {new Date().toLocaleDateString("pt-BR")}
                    </span>
                    <span className="flex items-center gap-1">
                      <FileText className="w-4 h-4" />
                      Confiança: {confidence}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" size="icon">
                <Share2 className="w-4 h-4" />
              </Button>
              <Button variant="outline" size="icon">
                <Printer className="w-4 h-4" />
              </Button>
              <Button className="gap-2">
                <Download className="w-4 h-4" />
                Baixar Relatório
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Main Content */}
      <Tabs defaultValue="summary" className="space-y-6">
        <TabsList>
          <TabsTrigger value="summary">Resumo</TabsTrigger>
          <TabsTrigger value="details">Detalhes Técnicos</TabsTrigger>
          <TabsTrigger value="images">Imagens</TabsTrigger>
        </TabsList>

        <TabsContent value="summary" className="space-y-6">
          <div className="grid md:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Confiança do Diagnóstico</CardTitle>
              </CardHeader>
              <CardContent>
                <div className={`text-4xl font-bold ${isTumor ? "text-destructive" : "text-accent"}`}>
                  {confidence}%
                </div>
                <p className="text-sm text-muted-foreground mt-2">
                  {isTumor ? "Alta confiança na detecção" : "Baixa probabilidade de anomalia"}
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base">{isTumor ? "Probabilidade Normal" : "Probabilidade de Tumor"}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold text-foreground">{uncertainty}%</div>
                <p className="text-sm text-muted-foreground mt-2">
                  {isTumor ? "Baixa probabilidade" : "Sem indicadores alarmantes"}
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base">Classificação de Risco</CardTitle>
              </CardHeader>
              <CardContent>
                <Badge variant={isTumor ? "destructive" : "secondary"} className="text-base px-3 py-1">
                  {isTumor ? "Alto" : "Baixo"}
                </Badge>
                <p className="text-sm text-muted-foreground mt-2">
                  {isTumor ? "Requer atenção imediata" : "Sem achados relevantes"}
                </p>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Interpretação Clínica</CardTitle>
              <CardDescription>Análise gerada por IA</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="bg-amber-500/10 border border-amber-500/20 rounded-lg p-4">
                <div className="flex gap-3">
                  <AlertTriangle className="w-5 h-5 text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5" />
                  <div className="space-y-2 text-sm">
                    <p className="text-foreground leading-relaxed">
                      O modelo de inteligência artificial identificou padrões de imagem consistentes com a presença de
                      uma massa tumoral cerebral. A região de interesse foi destacada no mapa de ativação com alta
                      confiança estatística.
                    </p>
                    <p className="text-foreground leading-relaxed">
                      <strong>Recomendação:</strong> Este diagnóstico assistido por IA deve ser revisado por um médico
                      especialista. Exames complementares e avaliação clínica são necessários para confirmação e
                      planejamento terapêutico.
                    </p>
                  </div>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <h4 className="font-semibold text-foreground">Características Identificadas</h4>
                  <ul className="space-y-1 text-sm text-muted-foreground">
                    <li className="flex items-center gap-2">
                      <div className="w-1.5 h-1.5 bg-primary rounded-full" />
                      Área hiperdensa localizada
                    </li>
                    <li className="flex items-center gap-2">
                      <div className="w-1.5 h-1.5 bg-primary rounded-full" />
                      Padrão de textura irregular
                    </li>
                    <li className="flex items-center gap-2">
                      <div className="w-1.5 h-1.5 bg-primary rounded-full" />
                      Efeito de massa observado
                    </li>
                    <li className="flex items-center gap-2">
                      <div className="w-1.5 h-1.5 bg-primary rounded-full" />
                      Contraste significativo com tecido adjacente
                    </li>
                  </ul>
                </div>

                <div className="space-y-2">
                  <h4 className="font-semibold text-foreground">Próximos Passos</h4>
                  <ul className="space-y-1 text-sm text-muted-foreground">
                    <li className="flex items-center gap-2">
                      <div className="w-1.5 h-1.5 bg-accent rounded-full" />
                      Revisão por radiologista
                    </li>
                    <li className="flex items-center gap-2">
                      <div className="w-1.5 h-1.5 bg-accent rounded-full" />
                      Avaliação oncológica
                    </li>
                    <li className="flex items-center gap-2">
                      <div className="w-1.5 h-1.5 bg-accent rounded-full" />
                      Exames complementares
                    </li>
                    <li className="flex items-center gap-2">
                      <div className="w-1.5 h-1.5 bg-accent rounded-full" />
                      Planejamento terapêutico
                    </li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="details" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Informações Técnicas do Modelo</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-3">
                  <div>
                    <div className="text-sm text-muted-foreground">Modelo de IA</div>
                    <div className="font-medium text-foreground">ResNet-50 Transfer Learning</div>
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground">Dataset de Treinamento</div>
                    <div className="font-medium text-foreground">Brain MRI Images (50,000+ scans)</div>
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground">Acurácia do Modelo</div>
                    <div className="font-medium text-foreground">98.3%</div>
                  </div>
                </div>
                <div className="space-y-3">
                  <div>
                    <div className="text-sm text-muted-foreground">Tempo de Processamento</div>
                    <div className="font-medium text-foreground">5.8 segundos</div>
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground">Limiar de Decisão</div>
                    <div className="font-medium text-foreground">{(threshold * 100).toFixed(1)}%</div>
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground">Versão do Modelo</div>
                    <div className="font-medium text-foreground">v2.4.1</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Métricas de Análise</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Probabilidade de Tumor</span>
                    <span className="font-bold text-destructive">96.5%</span>
                  </div>
                  <div className="h-2 bg-muted rounded-full overflow-hidden">
                    <div className="h-full bg-destructive" style={{ width: "96.5%" }} />
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Probabilidade Normal</span>
                    <span className="font-bold text-foreground">3.5%</span>
                  </div>
                  <div className="h-2 bg-muted rounded-full overflow-hidden">
                    <div className="h-full bg-accent" style={{ width: "3.5%" }} />
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="images" className="space-y-6">
          <div className="grid md:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Imagem Original</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="aspect-square bg-muted rounded-lg flex items-center justify-center">
                  <img
                    src="/brain-mri.png"
                    alt="Original scan"
                    className="w-full h-full object-cover rounded-lg"
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base">Análise Quantitativa</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="aspect-square bg-muted rounded-lg flex items-center justify-center relative">
                  <img
                    src="/brain-mri-with-measurements.jpg"
                    alt="Quantitative analysis"
                    className="w-full h-full object-cover rounded-lg opacity-70"
                  />
                  <div className="absolute inset-0 bg-gradient-to-br from-accent/20 via-transparent to-primary/20" />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base">Mapa de Ativação</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="aspect-square bg-muted rounded-lg flex items-center justify-center relative">
                  <img
                    src="/brain-tumor-heatmap.jpg"
                    alt="Activation map"
                    className="w-full h-full object-cover rounded-lg opacity-60"
                  />
                  <div className="absolute inset-0 bg-gradient-to-br from-destructive/30 via-transparent to-transparent" />
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
