import { PatientDetails } from "@/components/patient-details"
import { ArrowLeft } from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function PatientDetailPage({ params }: { params: { id: string } }) {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link href="/dashboard/patients">
          <Button variant="ghost" size="icon">
            <ArrowLeft className="w-5 h-5" />
          </Button>
        </Link>
        <div>
          <h1 className="text-3xl font-bold text-foreground">Detalhes do Paciente</h1>
          <p className="text-muted-foreground mt-1">Visualize e acompanhe informações do paciente</p>
        </div>
      </div>

      <PatientDetails patientId={params.id} />
    </div>
  )
}
