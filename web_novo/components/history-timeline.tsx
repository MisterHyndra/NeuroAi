"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { AlertTriangle, CheckCircle2, Eye, Calendar, Clock, User } from "lucide-react"
import Link from "next/link"
import { cn } from "@/lib/utils"

const historyData = [
  {
    id: "1",
    date: "2025-01-10",
    time: "14:30",
    patient: "Maria Silva Santos",
    patientId: "1",
    type: "Ressonância Magnética",
    result: "positive",
    confidence: "96.5%",
    status: "completed",
  },
  {
    id: "2",
    date: "2025-01-10",
    time: "11:15",
    patient: "João Carlos Oliveira",
    patientId: "2",
    type: "Tomografia Computadorizada",
    result: "negative",
    confidence: "98.2%",
    status: "completed",
  },
  {
    id: "3",
    date: "2025-01-09",
    time: "16:45",
    patient: "Ana Paula Ferreira",
    patientId: "3",
    type: "Ressonância Magnética",
    result: "negative",
    confidence: "99.1%",
    status: "completed",
  },
  {
    id: "4",
    date: "2025-01-09",
    time: "10:20",
    patient: "Carlos Eduardo Lima",
    patientId: "4",
    type: "Ressonância Magnética",
    result: "positive",
    confidence: "94.8%",
    status: "completed",
  },
  {
    id: "5",
    date: "2025-01-08",
    time: "15:30",
    patient: "Patricia Mendes Costa",
    patientId: "5",
    type: "Tomografia Computadorizada",
    result: "negative",
    confidence: "97.5%",
    status: "completed",
  },
  {
    id: "6",
    date: "2025-01-08",
    time: "09:00",
    patient: "Roberto Silva Alves",
    patientId: "6",
    type: "Ressonância Magnética",
    result: "negative",
    confidence: "98.9%",
    status: "completed",
  },
  {
    id: "7",
    date: "2025-01-07",
    time: "14:15",
    patient: "Fernanda Costa Lima",
    patientId: "7",
    type: "Ressonância Magnética",
    result: "positive",
    confidence: "95.2%",
    status: "completed",
  },
  {
    id: "8",
    date: "2025-01-07",
    time: "11:00",
    patient: "Ricardo Mendes Santos",
    patientId: "8",
    type: "Tomografia Computadorizada",
    result: "negative",
    confidence: "99.3%",
    status: "completed",
  },
]

// Group by date
const groupedHistory = historyData.reduce(
  (acc, item) => {
    const date = item.date
    if (!acc[date]) {
      acc[date] = []
    }
    acc[date].push(item)
    return acc
  },
  {} as Record<string, typeof historyData>,
)

export function HistoryTimeline() {
  return (
    <div className="space-y-6">
      {Object.entries(groupedHistory).map(([date, items]) => (
        <div key={date} className="space-y-4">
          <div className="flex items-center gap-3 sticky top-0 bg-background/95 backdrop-blur py-2 z-10">
            <Calendar className="w-5 h-5 text-muted-foreground" />
            <h3 className="text-lg font-semibold text-foreground">
              {new Date(date).toLocaleDateString("pt-BR", {
                weekday: "long",
                year: "numeric",
                month: "long",
                day: "numeric",
              })}
            </h3>
            <div className="flex-1 h-px bg-border" />
          </div>

          <div className="space-y-3 pl-8 relative before:absolute before:left-2.5 before:top-0 before:bottom-0 before:w-px before:bg-border">
            {items.map((item, index) => (
              <Card
                key={item.id}
                className={cn(
                  "relative before:absolute before:-left-[31px] before:top-6 before:w-2 before:h-2 before:rounded-full",
                  item.result === "positive"
                    ? "border-destructive/30 before:bg-destructive"
                    : "border-border before:bg-emerald-500",
                )}
              >
                <CardContent className="pt-6">
                  <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                    <div className="flex-1 space-y-3">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <h4 className="text-lg font-semibold text-foreground">{item.patient}</h4>
                            {item.result === "positive" ? (
                              <Badge variant="destructive" className="gap-1">
                                <AlertTriangle className="w-3 h-3" />
                                Tumor Detectado
                              </Badge>
                            ) : (
                              <Badge
                                variant="outline"
                                className="gap-1 bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border-emerald-500/20"
                              >
                                <CheckCircle2 className="w-3 h-3" />
                                Normal
                              </Badge>
                            )}
                          </div>

                          <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
                            <span className="flex items-center gap-1">
                              <User className="w-4 h-4" />
                              ID: #{item.id.padStart(6, "0")}
                            </span>
                            <span className="flex items-center gap-1">
                              <Clock className="w-4 h-4" />
                              {item.time}
                            </span>
                            <span>{item.type}</span>
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center gap-6">
                        <div>
                          <div className="text-xs text-muted-foreground">Confiança</div>
                          <div
                            className={cn(
                              "text-lg font-bold",
                              item.result === "positive"
                                ? "text-destructive"
                                : "text-emerald-600 dark:text-emerald-400",
                            )}
                          >
                            {item.confidence}
                          </div>
                        </div>
                        <div className="h-8 w-px bg-border" />
                        <div>
                          <div className="text-xs text-muted-foreground">Status</div>
                          <div className="text-sm font-medium text-foreground">Concluído</div>
                        </div>
                      </div>
                    </div>

                    <div className="flex gap-2">
                      <Link href={`/dashboard/patients/${item.patientId}`}>
                        <Button variant="outline" size="sm" className="gap-2 bg-transparent">
                          <User className="w-4 h-4" />
                          Paciente
                        </Button>
                      </Link>
                      <Link href={`/dashboard/analysis/${item.id}`}>
                        <Button size="sm" className="gap-2">
                          <Eye className="w-4 h-4" />
                          Ver Análise
                        </Button>
                      </Link>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
