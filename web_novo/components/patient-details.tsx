"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { User, Calendar, Phone, Mail, MapPin, Edit, Activity, FileText, AlertTriangle } from "lucide-react"
import Link from "next/link"
import { cn } from "@/lib/utils"

// Mock patient data
const patientData = {
  id: "1",
  name: "Maria Silva Santos",
  cpf: "123.456.789-00",
  birthDate: "1975-03-15",
  gender: "Feminino",
  bloodType: "O+",
  email: "maria.silva@email.com",
  phone: "(11) 98765-4321",
  address: "Rua das Flores, 123, Apto 45",
  city: "São Paulo",
  state: "SP",
  zip: "01234-567",
  status: "active",
  risk: "low",
  allergies: "Penicilina, Dipirona",
  medications: "Losartana 50mg - 1x ao dia",
  history: "Hipertensão controlada. Sem histórico de câncer na família.",
  registrationDate: "2023-05-20",
}

const recentExams = [
  {
    id: "1",
    date: "2025-01-10",
    type: "Ressonância Magnética",
    result: "Tumor Detectado",
    confidence: "96.5%",
    status: "completed",
    risk: "high",
  },
  {
    id: "2",
    date: "2024-10-15",
    type: "Tomografia Computadorizada",
    result: "Normal",
    confidence: "97.2%",
    status: "completed",
    risk: "low",
  },
  {
    id: "3",
    date: "2024-07-22",
    type: "Ressonância Magnética",
    result: "Normal",
    confidence: "99.1%",
    status: "completed",
    risk: "low",
  },
  {
    id: "4",
    date: "2024-04-18",
    type: "Ressonância Magnética",
    result: "Normal",
    confidence: "98.8%",
    status: "completed",
    risk: "low",
  },
  {
    id: "5",
    date: "2024-01-12",
    type: "Tomografia Computadorizada",
    result: "Normal",
    confidence: "97.9%",
    status: "completed",
    risk: "low",
  },
]

export function PatientDetails({ patientId }: { patientId: string }) {
  const patient = patientData // In real app, fetch by ID

  const age = Math.floor(
    (new Date().getTime() - new Date(patient.birthDate).getTime()) / (365.25 * 24 * 60 * 60 * 1000),
  )

  return (
    <div className="space-y-6">
      {/* Patient Overview Card */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-6">
            <div className="flex gap-4">
              <div className="w-20 h-20 bg-primary/10 rounded-xl flex items-center justify-center">
                <User className="w-10 h-10 text-primary" />
              </div>
              <div className="space-y-3">
                <div>
                  <h2 className="text-2xl font-bold text-foreground">{patient.name}</h2>
                  <div className="flex items-center gap-4 mt-1 text-sm text-muted-foreground">
                    <span className="font-mono">{patient.cpf}</span>
                    <span>•</span>
                    <span>{age} anos</span>
                    <span>•</span>
                    <span>{patient.gender}</span>
                    <span>•</span>
                    <span>Tipo {patient.bloodType}</span>
                  </div>
                </div>
                <div className="flex flex-wrap gap-2">
                  <Badge variant="secondary">Ativo</Badge>
                  <Badge
                    variant="outline"
                    className="bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border-emerald-500/20"
                  >
                    Risco Baixo
                  </Badge>
                </div>
              </div>
            </div>
            <Link href={`/dashboard/patients/${patientId}/edit`}>
              <Button variant="outline" className="gap-2 bg-transparent">
                <Edit className="w-4 h-4" />
                Editar
              </Button>
            </Link>
          </div>
        </CardContent>
      </Card>

      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="grid w-full grid-cols-3 lg:w-auto">
          <TabsTrigger value="overview">Visão Geral</TabsTrigger>
          <TabsTrigger value="exams">Exames</TabsTrigger>
          <TabsTrigger value="medical">Histórico Médico</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            {/* Contact Information */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Phone className="w-5 h-5" />
                  Informações de Contato
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-start gap-3">
                  <Mail className="w-5 h-5 text-muted-foreground mt-0.5" />
                  <div>
                    <div className="text-sm text-muted-foreground">Email</div>
                    <div className="font-medium">{patient.email}</div>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <Phone className="w-5 h-5 text-muted-foreground mt-0.5" />
                  <div>
                    <div className="text-sm text-muted-foreground">Telefone</div>
                    <div className="font-medium">{patient.phone}</div>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <MapPin className="w-5 h-5 text-muted-foreground mt-0.5" />
                  <div>
                    <div className="text-sm text-muted-foreground">Endereço</div>
                    <div className="font-medium">
                      {patient.address}
                      <br />
                      {patient.city} - {patient.state}, {patient.zip}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Registration Info */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calendar className="w-5 h-5" />
                  Informações de Cadastro
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="text-sm text-muted-foreground">Data de Cadastro</div>
                  <div className="font-medium">
                    {new Date(patient.registrationDate).toLocaleDateString("pt-BR", {
                      day: "numeric",
                      month: "long",
                      year: "numeric",
                    })}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-muted-foreground">Data de Nascimento</div>
                  <div className="font-medium">
                    {new Date(patient.birthDate).toLocaleDateString("pt-BR", {
                      day: "numeric",
                      month: "long",
                      year: "numeric",
                    })}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-muted-foreground">ID do Paciente</div>
                  <div className="font-medium font-mono">#{patient.id.padStart(6, "0")}</div>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="flex items-center gap-2">
                    <Activity className="w-5 h-5" />
                    Histórico de Exames e Evolução
                  </CardTitle>
                  <CardDescription>Acompanhamento temporal dos resultados</CardDescription>
                </div>
                <Link href="/dashboard/history">
                  <Button variant="outline" size="sm">
                    Ver Todos
                  </Button>
                </Link>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Trend Alert */}
              <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-4">
                <div className="flex items-start gap-3">
                  <AlertTriangle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
                  <div className="flex-1">
                    <div className="font-semibold text-foreground mb-1">Alteração Detectada</div>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      Último exame (10/01/2025) apresentou resultado positivo após sequência de 4 exames normais.
                      Recomenda-se avaliação médica imediata.
                    </p>
                  </div>
                </div>
              </div>

              {/* Timeline */}
              <div className="space-y-3">
                {recentExams.map((exam, index) => (
                  <div
                    key={exam.id}
                    className={cn(
                      "flex items-center gap-4 p-4 rounded-lg border transition-colors",
                      exam.risk === "high" ? "bg-destructive/5 border-destructive/30" : "bg-muted/30 border-border",
                    )}
                  >
                    <div
                      className={cn(
                        "w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0",
                        exam.risk === "high" ? "bg-destructive/10" : "bg-primary/10",
                      )}
                    >
                      <FileText className={cn("w-6 h-6", exam.risk === "high" ? "text-destructive" : "text-primary")} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <div className="font-medium text-foreground truncate">{exam.type}</div>
                        {index === 0 && exam.risk === "high" && (
                          <Badge variant="destructive" className="text-xs">
                            Novo
                          </Badge>
                        )}
                      </div>
                      <div className="text-sm text-muted-foreground">
                        {new Date(exam.date).toLocaleDateString("pt-BR")}
                      </div>
                    </div>
                    <div className="text-right flex-shrink-0">
                      <Badge variant={exam.risk === "high" ? "destructive" : "secondary"} className="mb-1">
                        {exam.result}
                      </Badge>
                      <div className="text-sm text-muted-foreground">{exam.confidence}</div>
                    </div>
                    <Link href={`/dashboard/analysis/${exam.id}`}>
                      <Button variant="ghost" size="icon" className="flex-shrink-0">
                        <FileText className="w-4 h-4" />
                      </Button>
                    </Link>
                  </div>
                ))}
              </div>

              <div className="grid grid-cols-3 gap-4 pt-4 border-t border-border">
                <div className="text-center">
                  <div className="text-2xl font-bold text-foreground">5</div>
                  <div className="text-xs text-muted-foreground">Total de Exames</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">4</div>
                  <div className="text-xs text-muted-foreground">Normais</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-destructive">1</div>
                  <div className="text-xs text-muted-foreground">Positivos</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="exams" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Histórico Completo de Exames</CardTitle>
              <CardDescription>Todos os exames realizados pelo paciente em ordem cronológica</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {recentExams.map((exam) => (
                <div
                  key={exam.id}
                  className={cn(
                    "flex items-center justify-between p-4 rounded-lg border",
                    exam.risk === "high" ? "bg-destructive/5 border-destructive/30" : "bg-muted/30 border-border",
                  )}
                >
                  <div className="flex items-center gap-4">
                    <div
                      className={cn(
                        "w-12 h-12 rounded-lg flex items-center justify-center",
                        exam.risk === "high" ? "bg-destructive/10" : "bg-primary/10",
                      )}
                    >
                      <FileText className={cn("w-6 h-6", exam.risk === "high" ? "text-destructive" : "text-primary")} />
                    </div>
                    <div>
                      <div className="font-medium text-foreground">{exam.type}</div>
                      <div className="text-sm text-muted-foreground">
                        {new Date(exam.date).toLocaleDateString("pt-BR", {
                          day: "2-digit",
                          month: "long",
                          year: "numeric",
                        })}
                      </div>
                    </div>
                  </div>
                  <div className="text-right flex items-center gap-4">
                    <div>
                      <Badge variant={exam.risk === "high" ? "destructive" : "secondary"} className="mb-1">
                        {exam.result}
                      </Badge>
                      <div className="text-sm text-muted-foreground">Confiança: {exam.confidence}</div>
                    </div>
                    <Link href={`/dashboard/analysis/${exam.id}`}>
                      <Button size="sm" variant="outline">
                        Ver Detalhes
                      </Button>
                    </Link>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="medical" className="space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-amber-500" />
                  Alergias
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-foreground">{patient.allergies || "Nenhuma alergia registrada"}</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Activity className="w-5 h-5" />
                  Medicações em Uso
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-foreground">{patient.medications || "Nenhuma medicação registrada"}</p>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Histórico Médico</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-foreground leading-relaxed">{patient.history || "Nenhum histórico registrado"}</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
