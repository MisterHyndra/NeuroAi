"use client"

import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Eye, Edit, MoreVertical } from "lucide-react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import Link from "next/link"

// Mock data
const patients = [
  {
    id: "1",
    name: "Maria Silva Santos",
    cpf: "123.456.789-00",
    birthDate: "1975-03-15",
    lastExam: "2025-01-10",
    status: "active",
    risk: "low",
  },
  {
    id: "2",
    name: "João Carlos Oliveira",
    cpf: "987.654.321-00",
    birthDate: "1968-07-22",
    lastExam: "2025-01-08",
    status: "active",
    risk: "medium",
  },
  {
    id: "3",
    name: "Ana Paula Ferreira",
    cpf: "456.789.123-00",
    birthDate: "1982-11-30",
    lastExam: "2024-12-20",
    status: "active",
    risk: "high",
  },
  {
    id: "4",
    name: "Carlos Eduardo Lima",
    cpf: "321.654.987-00",
    birthDate: "1955-05-10",
    lastExam: "2025-01-05",
    status: "monitoring",
    risk: "high",
  },
  {
    id: "5",
    name: "Patricia Mendes Costa",
    cpf: "789.123.456-00",
    birthDate: "1990-09-18",
    lastExam: "2024-11-15",
    status: "active",
    risk: "low",
  },
]

const statusLabels = {
  active: "Ativo",
  monitoring: "Em Monitoramento",
  inactive: "Inativo",
}

const riskLabels = {
  low: "Baixo",
  medium: "Médio",
  high: "Alto",
}

const riskColors = {
  low: "bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border-emerald-500/20",
  medium: "bg-amber-500/10 text-amber-700 dark:text-amber-400 border-amber-500/20",
  high: "bg-rose-500/10 text-rose-700 dark:text-rose-400 border-rose-500/20",
}

export function PatientsTable() {
  return (
    <div className="bg-card rounded-xl border border-border overflow-hidden">
      <Table>
        <TableHeader>
          <TableRow className="bg-muted/50">
            <TableHead className="font-semibold">Nome</TableHead>
            <TableHead className="font-semibold">CPF</TableHead>
            <TableHead className="font-semibold">Data de Nascimento</TableHead>
            <TableHead className="font-semibold">Último Exame</TableHead>
            <TableHead className="font-semibold">Status</TableHead>
            <TableHead className="font-semibold">Risco</TableHead>
            <TableHead className="text-right font-semibold">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {patients.map((patient) => (
            <TableRow key={patient.id} className="hover:bg-muted/30">
              <TableCell className="font-medium">{patient.name}</TableCell>
              <TableCell className="font-mono text-sm">{patient.cpf}</TableCell>
              <TableCell>{new Date(patient.birthDate).toLocaleDateString("pt-BR")}</TableCell>
              <TableCell>{new Date(patient.lastExam).toLocaleDateString("pt-BR")}</TableCell>
              <TableCell>
                <Badge variant="secondary" className="font-normal">
                  {statusLabels[patient.status as keyof typeof statusLabels]}
                </Badge>
              </TableCell>
              <TableCell>
                <Badge
                  variant="outline"
                  className={`font-normal ${riskColors[patient.risk as keyof typeof riskColors]}`}
                >
                  {riskLabels[patient.risk as keyof typeof riskLabels]}
                </Badge>
              </TableCell>
              <TableCell className="text-right">
                <div className="flex items-center justify-end gap-2">
                  <Link href={`/dashboard/patients/${patient.id}`}>
                    <Button variant="ghost" size="icon" className="h-8 w-8">
                      <Eye className="w-4 h-4" />
                    </Button>
                  </Link>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="icon" className="h-8 w-8">
                        <MoreVertical className="w-4 h-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem>
                        <Edit className="w-4 h-4 mr-2" />
                        Editar
                      </DropdownMenuItem>
                      <DropdownMenuItem>Ver Histórico</DropdownMenuItem>
                      <DropdownMenuItem className="text-destructive">Desativar</DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
