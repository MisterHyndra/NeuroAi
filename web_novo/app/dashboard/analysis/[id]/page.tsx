import { AnalysisResults } from "@/components/analysis-results"
import { ArrowLeft } from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function AnalysisResultPage({ params }: { params: { id: string } }) {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link href="/dashboard">
          <Button variant="ghost" size="icon">
            <ArrowLeft className="w-5 h-5" />
          </Button>
        </Link>
        <div>
          <h1 className="text-3xl font-bold text-foreground">Resultado da Análise</h1>
          <p className="text-muted-foreground mt-1">Visualização detalhada do diagnóstico</p>
        </div>
      </div>

      <AnalysisResults analysisId={params.id} />
    </div>
  )
}
