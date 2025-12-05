"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Calendar, Download, FileText, ChevronDown, AlertCircle } from "lucide-react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog"
import { 
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

const API_URL = 'http://localhost:5000/api'

interface AnalysisRecord {
  id: number
  image_name: string
  prediction: string
  confidence: number
  threshold: number
  created_at: string
  metadata?: any
  prediction_tumor?: number
  prediction_normal?: number
}

export function HistoryTimeline() {
  const [analyses, setAnalyses] = useState<AnalysisRecord[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [expandedId, setExpandedId] = useState<number | null>(null)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)

  useEffect(() => {
    loadHistory()
  }, [])

  const deleteAllHistory = async () => {
    setIsDeleting(true)
    try {
      const token = localStorage.getItem('neuroai_token')
      
      // Buscar todos os IDs primeiro
      const response = await fetch(`${API_URL}/history`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error('Erro ao buscar histórico')
      }

      const data = await response.json()
      const historyIds = data.history?.map((item: any) => item.id) || []

      // Deletar cada análise
      for (const id of historyIds) {
        await fetch(`${API_URL}/history/${id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
      }

      // Recarregar histórico
      setAnalyses([])
      setShowDeleteModal(false)
    } catch (err) {
      console.error('Erro ao deletar histórico:', err)
      alert('Erro ao deletar histórico')
    } finally {
      setIsDeleting(false)
    }
  }

  const handleDeleteClick = () => {
    setShowDeleteModal(true)
  }

  const loadHistory = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const token = localStorage.getItem('neuroai_token')
      
      const response = await fetch(`${API_URL}/history`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error(`Erro ao carregar histórico: ${response.status}`)
      }

      const data = await response.json()
      
      // Mapear dados do banco para o formato esperado
      const mappedAnalyses = data.history?.map((item: any) => ({
        id: item.id,
        image_name: item.image_name,
        prediction: item.result || 'unknown',
        confidence: item.confidence,
        threshold: item.threshold_used,
        created_at: item.created_at,
        prediction_normal: item.prediction_normal,
        prediction_tumor: item.prediction_tumor
      })) || []
      
      setAnalyses(mappedAnalyses)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar histórico')
      console.error('Erro:', err)
      // Dados fictícios para demonstração
      setAnalyses([
        {
          id: 1,
          image_name: "scan_001.jpg",
          prediction: "tumor",
          confidence: 0.96,
          threshold: 0.35,
          created_at: new Date().toISOString(),
          metadata: { cancer_type: "brain_cancer" }
        },
        {
          id: 2,
          image_name: "scan_002.jpg",
          prediction: "normal",
          confidence: 0.92,
          threshold: 0.35,
          created_at: new Date(Date.now() - 3600000).toISOString(),
          metadata: { cancer_type: "brain_cancer" }
        }
      ])
    } finally {
      setIsLoading(false)
    }
  }

  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString)
      return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    } catch {
      return dateString
    }
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.9) return 'bg-green-500/20 text-green-700'
    if (confidence >= 0.7) return 'bg-yellow-500/20 text-yellow-700'
    return 'bg-red-500/20 text-red-700'
  }

  const getPredictionBadge = (prediction: string, prediction_tumor?: number, prediction_normal?: number) => {
    // Se temos os valores de probabilidade, usa eles (mais confiável)
    if (prediction_tumor !== undefined && prediction_normal !== undefined) {
      const isTumor = prediction_tumor > prediction_normal
      if (isTumor) {
        return <Badge variant="destructive">Tumor Detectado</Badge>
      }
      return <Badge variant="secondary">Normal</Badge>
    }
    
    // Fallback para a string de prediction
    if (prediction === 'tumor' || prediction === 'cancer') {
      return <Badge variant="destructive">Tumor Detectado</Badge>
    }
    return <Badge variant="secondary">Normal</Badge>
  }

  if (isLoading) {
    return (
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            <p className="ml-3">Carregando histórico...</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Histórico de Análises</h1>
          <p className="text-muted-foreground mt-1">Registros de todas as imagens analisadas</p>
        </div>
        <div className="flex gap-2">
          <Button onClick={loadHistory} variant="outline">
            Atualizar
          </Button>
          <Button onClick={handleDeleteClick} variant="destructive">
            Limpar Histórico
          </Button>
        </div>
      </div>

      {error && (
        <Card className="border-amber-500/50 bg-amber-500/10">
          <CardContent className="pt-6">
            <p className="text-sm text-amber-800">⚠️ {error}</p>
            <p className="text-xs text-amber-700 mt-2">Exibindo dados de exemplo</p>
          </CardContent>
        </Card>
      )}

      {analyses.length === 0 ? (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-12">
              <FileText className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">Nenhuma análise realizada ainda</p>
            </div>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>Análises Registradas</CardTitle>
            <CardDescription>Total: {analyses.length} análise(s)</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="border rounded-lg overflow-hidden">
              <Table>
                <TableHeader>
                  <TableRow className="bg-muted/50">
                    <TableHead>Imagem</TableHead>
                    <TableHead>Resultado</TableHead>
                    <TableHead>Confiança</TableHead>
                    <TableHead>Data/Hora</TableHead>
                    <TableHead>Ações</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {analyses.map((analysis, idx) => (
                    <TableRow key={analysis.id || idx} className="hover:bg-muted/50">
                      <TableCell className="font-medium">{analysis.image_name}</TableCell>
                      <TableCell>
                        {getPredictionBadge(analysis.prediction, analysis.prediction_tumor, analysis.prediction_normal)}
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <div className="flex-1">
                            <div className="h-2 bg-muted rounded-full overflow-hidden">
                              <div
                                className={`h-full transition-all ${
                                  (analysis.confidence * 100) >= 90
                                    ? 'bg-green-500'
                                    : (analysis.confidence * 100) >= 70
                                    ? 'bg-yellow-500'
                                    : 'bg-red-500'
                                }`}
                                style={{ width: `${analysis.confidence * 100}%` }}
                              />
                            </div>
                          </div>
                          <span className={`text-sm font-semibold px-2 py-1 rounded ${getConfidenceColor(analysis.confidence)}`}>
                            {(analysis.confidence * 100).toFixed(1)}%
                          </span>
                        </div>
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        <div className="flex items-center gap-2">
                          <Calendar className="w-4 h-4" />
                          {formatDate(analysis.created_at)}
                        </div>
                      </TableCell>
                      <TableCell>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setExpandedId(expandedId === analysis.id ? null : analysis.id)}
                          className="gap-2"
                        >
                          <ChevronDown className={`w-4 h-4 transition-transform ${expandedId === analysis.id ? 'rotate-180' : ''}`} />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>

            {/* Detalhes expandidos */}
            {expandedId && (
              <div className="mt-4 p-4 bg-muted/50 rounded-lg space-y-4">
                {analyses.find(a => a.id === expandedId) && (
                  <>
                    <div className="grid md:grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-muted-foreground">Limiar de Confiança</p>
                        <p className="text-lg font-semibold">{(analyses.find(a => a.id === expandedId)!.threshold * 100).toFixed(1)}%</p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground">Tipo de Câncer</p>
                        <p className="text-lg font-semibold">
                          {analyses.find(a => a.id === expandedId)?.metadata?.cancer_type || 'Cérebro'}
                        </p>
                      </div>
                    </div>

                    <div className="flex gap-2">
                      <Button variant="outline" className="gap-2" size="sm">
                        <Download className="w-4 h-4" />
                        Baixar Relatório
                      </Button>
                    </div>
                  </>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Estatísticas */}
      {analyses.length > 0 && (
        <div className="grid md:grid-cols-3 gap-4">
          <Card>
            <CardContent className="pt-6">
              <p className="text-sm text-muted-foreground">Total de Análises</p>
              <p className="text-3xl font-bold mt-2">{analyses.length}</p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <p className="text-sm text-muted-foreground">Casos Positivos</p>
              <p className="text-3xl font-bold text-red-600 mt-2">
                {analyses.filter(a => {
                  // Se tem os valores de probabilidade, usa eles
                  if (a.prediction_tumor !== undefined && a.prediction_normal !== undefined) {
                    return a.prediction_tumor > a.prediction_normal
                  }
                  // Fallback
                  return a.prediction === 'tumor' || a.prediction === 'cancer'
                }).length}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <p className="text-sm text-muted-foreground">Confiança Média</p>
              <p className="text-3xl font-bold text-green-600 mt-2">
                {(
                  analyses.reduce((sum, a) => sum + a.confidence, 0) / analyses.length * 100
                ).toFixed(1)}%
              </p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Modal de Confirmação de Deleção */}
      <Dialog open={showDeleteModal} onOpenChange={setShowDeleteModal}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader className="flex flex-row items-start gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-destructive/10">
              <AlertCircle className="h-6 w-6 text-destructive" />
            </div>
            <div className="flex flex-col gap-2">
              <DialogTitle>Limpar todos os objetos?</DialogTitle>
              <DialogDescription>
                Esta ação não pode ser desfeita. Todos os objetos adicionados serão removidos.
              </DialogDescription>
            </div>
          </DialogHeader>
          <DialogFooter className="gap-2 sm:gap-0">
            <Button 
              variant="outline" 
              onClick={() => setShowDeleteModal(false)}
              disabled={isDeleting}
            >
              Cancelar
            </Button>
            <Button 
              variant="destructive"
              onClick={deleteAllHistory}
              disabled={isDeleting}
            >
              {isDeleting ? 'Deletando...' : 'Sim, limpar tudo'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

export { HistoryTimeline as HistoryTimelineIntegrated }
