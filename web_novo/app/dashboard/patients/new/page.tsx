import { PatientRegistrationForm } from "@/components/patient-registration-form"
import { ArrowLeft } from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function NewPatientPage() {
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center gap-4">
        <Link href="/dashboard/patients">
          <Button variant="ghost" size="icon">
            <ArrowLeft className="w-5 h-5" />
          </Button>
        </Link>
        <div>
          <h1 className="text-3xl font-bold text-foreground">Novo Paciente</h1>
          <p className="text-muted-foreground mt-1">Cadastre um novo paciente no sistema</p>
        </div>
      </div>

      <PatientRegistrationForm />
    </div>
  )
}
