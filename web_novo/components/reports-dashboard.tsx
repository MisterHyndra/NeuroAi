"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { BarChart3, Download, Calendar, TrendingUp } from "lucide-react"
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts"

const API_URL = 'http://localhost:5000/api'

interface ChartData {
  date: string
  analyses: number
  tumors: number
  normal: number
}

interface Stats {
  totalAnalyses: number
  totalTumors: number
  averageConfidence: number
  tumorRate: number
}

export function ReportsDashboard() {
  const [period, setPeriod] = useState<'week' | 'month' | 'year'>('month')
  const [chartData, setChartData] = useState<ChartData[]>([])
  const [stats, setStats] = useState<Stats>({
    totalAnalyses: 0,
    totalTumors: 0,
    averageConfidence: 0,
    tumorRate: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadReportData()
  }, [period])

  const loadReportData = async () => {
    setLoading(true)
    try {
      const token = localStorage.getItem('neuroai_token')
      
      const response = await fetch(`${API_URL}/history`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) throw new Error('Erro ao carregar dados')

      const data = await response.json()
      const history = data.history || []

      // Calcular data base para o período
      const now = new Date()
      let startDate = new Date()

      if (period === 'week') {
        startDate.setDate(now.getDate() - 7)
      } else if (period === 'month') {
        startDate.setMonth(now.getMonth() - 1)
      } else {
        startDate.setFullYear(now.getFullYear() - 1)
      }

      // Agrupar dados por dia
      const grouped: { [key: string]: { analyses: number; tumors: number; normal: number; confidences: number[] } } = {}
      let totalConfidences: number[] = []

      history.forEach((item: any) => {
        const itemDate = new Date(item.created_at)
        
        if (itemDate >= startDate) {
          const dateKey = itemDate.toLocaleDateString('pt-BR')
          
          if (!grouped[dateKey]) {
            grouped[dateKey] = { analyses: 0, tumors: 0, normal: 0, confidences: [] }
          }

          grouped[dateKey].analyses++
          grouped[dateKey].confidences.push(item.prediction_tumor)

          if (item.prediction_tumor > item.prediction_normal) {
            grouped[dateKey].tumors++
          } else {
            grouped[dateKey].normal++
          }

          totalConfidences.push(item.prediction_tumor)
        }
      })

      // Converter para array e ordenar
      const chartDataArray: ChartData[] = Object.entries(grouped)
        .map(([date, data]) => ({
          date,
          analyses: data.analyses,
          tumors: data.tumors,
          normal: data.normal,
        }))
        .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())

      setChartData(chartDataArray)

      // Calcular estatísticas
      const totalAnalyses = history.length
      const totalTumors = history.filter((item: any) => item.prediction_tumor > item.prediction_normal).length
      const averageConfidence = totalConfidences.length > 0 
        ? (totalConfidences.reduce((a, b) => a + b, 0) / totalConfidences.length) * 100
        : 0
      const tumorRate = totalAnalyses > 0 ? (totalTumors / totalAnalyses) * 100 : 0

      setStats({
        totalAnalyses,
        totalTumors,
        averageConfidence,
        tumorRate,
      })
    } catch (err) {
      console.error('Erro ao carregar relatório:', err)
    } finally {
      setLoading(false)
    }
  }

  const pieData = [
    { name: 'Normal', value: stats.totalAnalyses - stats.totalTumors },
    { name: 'Tumor', value: stats.totalTumors },
  ]

  const COLORS = ['#64ff64', '#ff6464']

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Relatórios</h1>
          <p className="text-muted-foreground mt-1">Análises estatísticas e desempenho do sistema</p>
        </div>
        <div className="flex gap-2">
          <Button 
            variant={period === 'week' ? 'default' : 'outline'}
            onClick={() => setPeriod('week')}
          >
            7 dias
          </Button>
          <Button 
            variant={period === 'month' ? 'default' : 'outline'}
            onClick={() => setPeriod('month')}
          >
            30 dias
          </Button>
          <Button 
            variant={period === 'year' ? 'default' : 'outline'}
            onClick={() => setPeriod('year')}
          >
            1 ano
          </Button>
          <Button variant="outline" className="gap-2">
            <Download className="w-4 h-4" />
            Exportar
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-muted-foreground">Total de Análises</p>
            <p className="text-3xl font-bold text-foreground mt-2">{stats.totalAnalyses}</p>
            <p className="text-xs text-muted-foreground mt-2">nos últimos {period === 'week' ? '7 dias' : period === 'month' ? '30 dias' : '1 ano'}</p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-muted-foreground">Casos com Tumor</p>
            <p className="text-3xl font-bold text-destructive mt-2">{stats.totalTumors}</p>
            <Badge className="mt-2 bg-destructive/20 text-destructive">{stats.tumorRate.toFixed(1)}%</Badge>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-muted-foreground">Confiança Média</p>
            <p className="text-3xl font-bold text-primary mt-2">{stats.averageConfidence.toFixed(1)}%</p>
            <p className="text-xs text-muted-foreground mt-2">das análises</p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-muted-foreground">Taxa Normal</p>
            <p className="text-3xl font-bold text-accent mt-2">{(100 - stats.tumorRate).toFixed(1)}%</p>
            <Badge className="mt-2 bg-accent/20 text-accent">{stats.totalAnalyses - stats.totalTumors} casos</Badge>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid md:grid-cols-3 gap-6">
        {/* Line Chart - Análises por dia */}
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Análises por Dia</CardTitle>
            <CardDescription>Evolução de análises realizadas</CardDescription>
          </CardHeader>
          <CardContent>
            {chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                  <XAxis dataKey="date" stroke="#999" style={{ fontSize: '12px' }} />
                  <YAxis stroke="#999" style={{ fontSize: '12px' }} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1a1f35', border: '1px solid #333' }}
                    labelStyle={{ color: '#fff' }}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="analyses" 
                    stroke="#00d9ff" 
                    name="Total de Análises"
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="tumors" 
                    stroke="#ff6464" 
                    name="Tumores Detectados"
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="normal" 
                    stroke="#64ff64" 
                    name="Normal"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[300px] flex items-center justify-center text-muted-foreground">
                Sem dados para este período
              </div>
            )}
          </CardContent>
        </Card>

        {/* Pie Chart - Distribuição */}
        <Card>
          <CardHeader>
            <CardTitle>Distribuição de Resultados</CardTitle>
            <CardDescription>Proporção geral</CardDescription>
          </CardHeader>
          <CardContent>
            {stats.totalAnalyses > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value, percent }) => `${name}: ${value} (${(percent * 100).toFixed(0)}%)`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {COLORS.map((color, index) => (
                      <Cell key={`cell-${index}`} fill={color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1a1f35', border: '1px solid #333' }}
                    labelStyle={{ color: '#fff' }}
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[300px] flex items-center justify-center text-muted-foreground">
                Sem dados
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Bar Chart - Comparação */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5" />
            Comparação Diária
          </CardTitle>
          <CardDescription>Análises Normais vs Tumores por dia</CardDescription>
        </CardHeader>
        <CardContent>
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="date" stroke="#999" style={{ fontSize: '12px' }} />
                <YAxis stroke="#999" style={{ fontSize: '12px' }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1a1f35', border: '1px solid #333' }}
                  labelStyle={{ color: '#fff' }}
                />
                <Legend />
                <Bar dataKey="normal" stackId="a" fill="#64ff64" name="Normal" />
                <Bar dataKey="tumors" stackId="a" fill="#ff6464" name="Tumor" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-[300px] flex items-center justify-center text-muted-foreground">
              Sem dados para este período
            </div>
          )}
        </CardContent>
      </Card>

      {/* Summary */}
      <Card className="bg-primary/5 border-primary/20">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            Resumo do Período
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          <p>
            <span className="text-muted-foreground">Período analisado:</span>{' '}
            <span className="font-semibold">
              {period === 'week' ? 'Últimos 7 dias' : period === 'month' ? 'Últimos 30 dias' : 'Último ano'}
            </span>
          </p>
          <p>
            <span className="text-muted-foreground">Taxa de detecção de tumores:</span>{' '}
            <span className="font-semibold text-destructive">{stats.tumorRate.toFixed(1)}%</span>
          </p>
          <p>
            <span className="text-muted-foreground">Confiança média do modelo:</span>{' '}
            <span className="font-semibold text-primary">{stats.averageConfidence.toFixed(1)}%</span>
          </p>
          <p>
            <span className="text-muted-foreground">Total de análises realizadas:</span>{' '}
            <span className="font-semibold">{stats.totalAnalyses}</span>
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
