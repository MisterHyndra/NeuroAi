"use client"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Card, CardContent } from "@/components/ui/card"
import { Search, Filter, Download } from "lucide-react"

export function HistoryFilters() {
  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input placeholder="Buscar por paciente, ID ou data..." className="pl-9 h-10" />
          </div>

          <Select defaultValue="all">
            <SelectTrigger className="w-full md:w-48">
              <SelectValue placeholder="Tipo de Resultado" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos os Resultados</SelectItem>
              <SelectItem value="positive">Positivo (Tumor)</SelectItem>
              <SelectItem value="negative">Negativo (Normal)</SelectItem>
            </SelectContent>
          </Select>

          <Select defaultValue="30">
            <SelectTrigger className="w-full md:w-48">
              <SelectValue placeholder="Período" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7">Últimos 7 dias</SelectItem>
              <SelectItem value="30">Últimos 30 dias</SelectItem>
              <SelectItem value="90">Últimos 3 meses</SelectItem>
              <SelectItem value="365">Último ano</SelectItem>
              <SelectItem value="all">Todo período</SelectItem>
            </SelectContent>
          </Select>

          <Button variant="outline" className="gap-2 bg-transparent">
            <Filter className="w-4 h-4" />
            Mais Filtros
          </Button>

          <Button variant="outline" className="gap-2 bg-transparent">
            <Download className="w-4 h-4" />
            Exportar
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
