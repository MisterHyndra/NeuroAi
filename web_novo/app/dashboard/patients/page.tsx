import { PatientsTable } from "@/components/patients-table"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { UserPlus, Search, Filter } from "lucide-react"
import Link from "next/link"

export default function PatientsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground">Pacientes</h1>
          <p className="text-muted-foreground mt-1">Gerencie e acompanhe seus pacientes</p>
        </div>
        <Link href="/dashboard/patients/new">
          <Button className="gap-2">
            <UserPlus className="w-4 h-4" />
            Novo Paciente
          </Button>
        </Link>
      </div>

      <div className="flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <Input placeholder="Buscar por nome, CPF ou ID..." className="pl-9 h-10" />
        </div>
        <Button variant="outline" className="gap-2 bg-transparent">
          <Filter className="w-4 h-4" />
          Filtros
        </Button>
      </div>

      <PatientsTable />
    </div>
  )
}
