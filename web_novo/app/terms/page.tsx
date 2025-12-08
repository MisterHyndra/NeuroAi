import { Button } from "@/components/ui/button"
import { Link as LinkIcon } from "lucide-react"
import Link from "next/link"

export default function TermsPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary/10 via-accent/10 to-primary/10 border-b border-border">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="flex items-center gap-2 mb-4">
            <LinkIcon className="w-5 h-5 text-primary" />
            <Link href="/" className="text-sm text-primary hover:underline">
              Voltar ao início
            </Link>
          </div>
          <h1 className="text-4xl font-bold text-foreground mb-2">Termos de Serviço</h1>
          <p className="text-muted-foreground">Última atualização: Dezembro de 2025</p>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="space-y-8">
          {/* Introdução */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">1. Aceitação dos Termos</h2>
            <p className="text-muted-foreground leading-relaxed">
              Ao acessar e usar a plataforma NeuroAI Diagnostics ("Serviço"), você concorda em cumprir e estar vinculado por
              estes Termos de Serviço. Se você não concorda com qualquer parte destes termos, não deve usar o Serviço.
            </p>
          </section>

          {/* Descrição do Serviço */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">2. Descrição do Serviço</h2>
            <p className="text-muted-foreground leading-relaxed mb-4">
              O NeuroAI Diagnostics é uma plataforma de análise de imagens médicas alimentada por Inteligência Artificial,
              projetada para auxiliar profissionais de saúde na identificação e diagnóstico de anormalidades cerebrais,
              incluindo tumores.
            </p>
            <div className="bg-destructive/5 border border-destructive/20 rounded p-4 text-sm text-muted-foreground">
              <p className="font-semibold text-foreground mb-2">⚠️ Aviso Importante:</p>
              <p>
                As análises fornecidas por esta plataforma são de natureza auxiliar e não devem ser usadas como diagnóstico
                definitivo. Sempre consulte um médico qualificado para diagnóstico e tratamento definitivos.
              </p>
            </div>
          </section>

          {/* Direitos do Usuário */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">3. Direitos e Responsabilidades do Usuário</h2>
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold text-foreground mb-2">3.1 Conta de Usuário</h3>
                <p className="text-muted-foreground">
                  Você é responsável por manter a confidencialidade de suas credenciais de login. Você concorda em aceitar
                  responsabilidade por todas as atividades que ocorrem em sua conta.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-foreground mb-2">3.2 Uso Adequado</h3>
                <p className="text-muted-foreground">
                  Você concorda em usar este Serviço apenas para fins legais e em conformidade com todas as leis e regulações
                  aplicáveis. Você não deve:
                </p>
                <ul className="list-disc list-inside text-muted-foreground mt-2 space-y-1">
                  <li>Usar o Serviço para diagnóstico definitivo sem supervisão médica</li>
                  <li>Tentar acessar sistemas não autorizados</li>
                  <li>Transmitir malware ou código malicioso</li>
                  <li>Usar o Serviço para fins ilegais ou prejudiciais</li>
                  <li>Compartilhar dados de pacientes sem consentimento apropriado</li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold text-foreground mb-2">3.3 Consentimento do Paciente</h3>
                <p className="text-muted-foreground">
                  Se você está analisando imagens de terceiros, você confirma que tem consentimento válido para fazê-lo e que
                  cumpre com todas as regulações de privacidade de dados médicos, incluindo LGPD (Lei Geral de Proteção de
                  Dados).
                </p>
              </div>
            </div>
          </section>

          {/* Propriedade Intelectual */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">4. Propriedade Intelectual</h2>
            <p className="text-muted-foreground leading-relaxed">
              Todo conteúdo, funcionalidades e tecnologia da plataforma NeuroAI Diagnostics, incluindo o modelo de IA,
              interfaces e documentação, são propriedade intelectual protegida. Você concorda em não reproduzir, distribuir
              ou transmitir qualquer conteúdo sem autorização prévia por escrito.
            </p>
          </section>

          {/* Limitação de Responsabilidade */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">5. Limitação de Responsabilidade</h2>
            <p className="text-muted-foreground leading-relaxed mb-4">
              A plataforma é fornecida "como está", sem garantias de qualquer tipo. Na medida permitida pela lei:
            </p>
            <ul className="list-disc list-inside text-muted-foreground space-y-2">
              <li>Não nos responsabilizamos por danos diretos, indiretos ou consequentes</li>
              <li>Não garantimos precisão absoluta das análises</li>
              <li>Não somos responsáveis por decisões médicas tomadas com base nas análises</li>
              <li>Não nos responsabilizamos por interrupções de serviço ou perda de dados</li>
            </ul>
          </section>

          {/* Conformidade Regulatória */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">6. Conformidade Regulatória</h2>
            <p className="text-muted-foreground leading-relaxed mb-4">
              O uso desta plataforma deve estar em conformidade com:
            </p>
            <ul className="list-disc list-inside text-muted-foreground space-y-2">
              <li>Regulações de proteção de dados (LGPD, GDPR, HIPAA, conforme aplicável)</li>
              <li>Diretrizes profissionais médicas e de saúde</li>
              <li>Leis de pesquisa e inovação em IA</li>
              <li>Regulações locais e internacionais de vigilância em saúde</li>
            </ul>
          </section>

          {/* Modificações */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">7. Modificações dos Termos</h2>
            <p className="text-muted-foreground leading-relaxed">
              Reservamos o direito de modificar estes Termos de Serviço a qualquer momento. As modificações entram em vigor
              imediatamente após a publicação. Seu uso continuado do Serviço constitui aceitação dos termos modificados.
            </p>
          </section>

          {/* Encerramento */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">8. Encerramento de Conta</h2>
            <p className="text-muted-foreground leading-relaxed">
              Podemos suspender ou encerrar sua conta a qualquer momento, sem aviso prévio, se determinarmos que você violou
              estes Termos de Serviço ou se usou o Serviço para fins ilegais ou prejudiciais.
            </p>
          </section>

          {/* Contato */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">9. Contato</h2>
            <p className="text-muted-foreground leading-relaxed mb-4">
              Se você tiver dúvidas sobre estes Termos de Serviço, entre em contato conosco em:
            </p>
            <div className="bg-accent/10 border border-accent/20 rounded p-4">
              <p className="text-foreground font-semibold">NeuroAI Diagnostics</p>
              <p className="text-muted-foreground text-sm">Email: legal@neuroai.com</p>
              <p className="text-muted-foreground text-sm">Website: www.neuroai.com</p>
            </div>
          </section>
        </div>

        {/* Footer */}
        <div className="mt-16 pt-8 border-t border-border flex gap-4 justify-center">
          <Link href="/login">
            <Button variant="outline">Voltar ao Login</Button>
          </Link>
          <Link href="/privacy">
            <Button variant="ghost">Política de Privacidade</Button>
          </Link>
        </div>
      </div>
    </div>
  )
}
