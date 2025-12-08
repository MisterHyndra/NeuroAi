import { Button } from "@/components/ui/button"
import { Link as LinkIcon, Lock } from "lucide-react"
import Link from "next/link"

export default function PrivacyPage() {
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
          <div className="flex items-center gap-3 mb-2">
            <Lock className="w-6 h-6 text-accent" />
            <h1 className="text-4xl font-bold text-foreground">Política de Privacidade</h1>
          </div>
          <p className="text-muted-foreground">Última atualização: Dezembro de 2025</p>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="space-y-8">
          {/* Introdução */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">1. Introdução</h2>
            <p className="text-muted-foreground leading-relaxed">
              A NeuroAI Diagnostics ("nós", "nosso" ou "a Empresa") é compromissada com a proteção de sua privacidade. Esta
              Política de Privacidade explica como coletamos, usamos, divulgamos e salvaguardamos suas informações quando você
              usa nossa plataforma.
            </p>
          </section>

          {/* Informações que Coletamos */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">2. Informações que Coletamos</h2>
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold text-foreground mb-2">2.1 Informações de Identificação Pessoal</h3>
                <p className="text-muted-foreground">
                  Nome, email, número de telefone, endereço profissional e credenciais de registro profissional (para
                  profissionais de saúde).
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-foreground mb-2">2.2 Dados Médicos e de Imagem</h3>
                <p className="text-muted-foreground">
                  Imagens médicas (ressonância magnética, tomografia, etc.) que você faz upload para análise. Estes dados são
                  tratados com máxima confidencialidade.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-foreground mb-2">2.3 Dados de Uso</h3>
                <p className="text-muted-foreground">
                  Informações sobre como você interage com nossa plataforma, incluindo datas e horas de acesso, páginas
                  visualizadas, recursos utilizados e ações realizadas.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-foreground mb-2">2.4 Dados Técnicos</h3>
                <p className="text-muted-foreground">
                  Tipo de dispositivo, sistema operacional, navegador, endereço IP, identificadores únicos e dados de
                  localização aproximada.
                </p>
              </div>
            </div>
          </section>

          {/* Como Usamos */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">3. Como Usamos Suas Informações</h2>
            <p className="text-muted-foreground leading-relaxed mb-4">Utilizamos as informações coletadas para:</p>
            <ul className="list-disc list-inside text-muted-foreground space-y-2">
              <li>Fornecer, manter e melhorar nossos serviços</li>
              <li>Processar análises de imagens médicas</li>
              <li>Autenticar sua conta e verificar sua identidade</li>
              <li>Comunicar-se com você sobre atualizações de serviço, aviso importante e questões de segurança</li>
              <li>Gerar histórico de análises para referência futura</li>
              <li>Melhorar a precisão e eficácia do modelo de IA (com dados anonimizados)</li>
              <li>Cumprir com obrigações legais e regulatórias</li>
              <li>Responder a consultas e fornecer suporte ao cliente</li>
            </ul>
          </section>

          {/* Base Legal */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">4. Base Legal para Processamento</h2>
            <p className="text-muted-foreground leading-relaxed mb-4">
              Processamos seus dados com base em:
            </p>
            <ul className="list-disc list-inside text-muted-foreground space-y-2">
              <li>Seu consentimento explícito</li>
              <li>Necessidade de executar contrato contigo</li>
              <li>Conformidade com obrigações legais</li>
              <li>Proteção de interesses legítimos nossos e de terceiros</li>
              <li>Interesse público em cuidados de saúde</li>
            </ul>
          </section>

          {/* Compartilhamento de Dados */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">5. Compartilhamento de Dados</h2>
            <div className="space-y-4">
              <p className="text-muted-foreground">
                Não compartilhamos suas informações pessoais com terceiros, exceto:
              </p>
              <div>
                <h3 className="font-semibold text-foreground mb-2">5.1 Necessidade Legal</h3>
                <p className="text-muted-foreground">
                  Quando exigido por lei, regulação ou processo legal válido.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-foreground mb-2">5.2 Consentimento Explícito</h3>
                <p className="text-muted-foreground">
                  Quando você tiver dado consentimento específico para compartilhamento.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-foreground mb-2">5.3 Fornecedores de Serviço</h3>
                <p className="text-muted-foreground">
                  Com fornecedores terceirizados que processam dados em nosso nome (hospedagem, backup, etc.), sujeitos a
                  acordos de confidencialidade.
                </p>
              </div>
            </div>
          </section>

          {/* Segurança de Dados */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">6. Segurança de Dados</h2>
            <p className="text-muted-foreground leading-relaxed mb-4">
              Implementamos medidas de segurança técnicas e organizacionais para proteger suas informações:
            </p>
            <ul className="list-disc list-inside text-muted-foreground space-y-2">
              <li>Encriptação em trânsito (HTTPS/TLS)</li>
              <li>Encriptação em repouso para dados sensíveis</li>
              <li>Autenticação segura de usuário (JWT)</li>
              <li>Firewalls e sistemas de detecção de intrusão</li>
              <li>Backups regulares e recuperação de desastres</li>
              <li>Acesso restrito a dados pessoais apenas para pessoal autorizado</li>
              <li>Monitoramento de segurança contínuo</li>
            </ul>
          </section>

          {/* Direitos do Usuário */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">7. Seus Direitos</h2>
            <p className="text-muted-foreground leading-relaxed mb-4">
              Sob aplicável de proteção de dados (incluindo LGPD), você tem direito a:
            </p>
            <ul className="list-disc list-inside text-muted-foreground space-y-2">
              <li><strong>Acesso:</strong> Você pode solicitar uma cópia de seus dados pessoais</li>
              <li><strong>Retificação:</strong> Você pode corrigir informações imprecisas</li>
              <li><strong>Exclusão:</strong> Você pode solicitar a exclusão de seus dados</li>
              <li><strong>Portabilidade:</strong> Você pode receber seus dados em formato estruturado</li>
              <li><strong>Consentimento:</strong> Você pode retirar consentimento a qualquer momento</li>
              <li><strong>Oposição:</strong> Você pode se opor a certos processamentos</li>
            </ul>
            <p className="text-muted-foreground mt-4">
              Para exercer esses direitos, entre em contato conosco em privacy@neuroai.com
            </p>
          </section>

          {/* Retenção de Dados */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">8. Retenção de Dados</h2>
            <div className="space-y-3 text-muted-foreground">
              <p>
                <strong>Histórico de Análises:</strong> Mantido enquanto sua conta estiver ativa. Você pode solicitá-lo para exclusão a qualquer momento.
              </p>
              <p>
                <strong>Imagens Médicas:</strong> Retidas pelo período necessário para fornecer o serviço e cumprir obrigações legais (conforme exigido por regulações médicas).
              </p>
              <p>
                <strong>Dados de Log e Auditoria:</strong> Normalmente retidos por 12 meses para fins de segurança e conformidade.
              </p>
              <p>
                <strong>Contas Deletadas:</strong> Após exclusão de conta, os dados são anonimizados dentro de 30 dias, exceto quando legalmente obrigado a manter.
              </p>
            </div>
          </section>

          {/* Cookies */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">9. Cookies e Tecnologias Similares</h2>
            <p className="text-muted-foreground leading-relaxed mb-4">
              Usamos cookies e tecnologias similares para:
            </p>
            <ul className="list-disc list-inside text-muted-foreground space-y-2">
              <li>Manter sua sessão autenticada</li>
              <li>Lembrar suas preferências</li>
              <li>Melhorar a experiência do usuário</li>
              <li>Analisar padrões de uso (com dados agregados)</li>
            </ul>
            <p className="text-muted-foreground mt-4">
              Você pode controlar cookies através de configurações do navegador.
            </p>
          </section>

          {/* Crianças */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">10. Proteção de Menores</h2>
            <p className="text-muted-foreground leading-relaxed">
              Nosso Serviço não é destinado a menores de 18 anos. Não coletamos intencionalmente informações pessoais de
              menores. Se soubermos que um menor forneceu informações, tomaremos medidas para excluir tais informações
              imediatamente.
            </p>
          </section>

          {/* Transferências Internacionais */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">11. Transferências Internacionais de Dados</h2>
            <p className="text-muted-foreground leading-relaxed">
              Se seus dados forem transferidos para fora do Brasil, garantimos proteção equivalente através de cláusulas de
              transferência padrão e medidas de segurança adequadas em conformidade com a LGPD.
            </p>
          </section>

          {/* Contato */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">12. Responsável de Privacidade / Contato</h2>
            <p className="text-muted-foreground leading-relaxed mb-4">
              Se você tiver dúvidas sobre esta Política de Privacidade ou nossas práticas de privacidade, entre em contato:
            </p>
            <div className="bg-accent/10 border border-accent/20 rounded p-4 space-y-2">
              <p className="text-foreground font-semibold">NeuroAI Diagnostics - Responsável de Privacidade</p>
              <p className="text-muted-foreground text-sm">Email: privacy@neuroai.com</p>
              <p className="text-muted-foreground text-sm">Telefone: +55 (XX) XXXX-XXXX</p>
              <p className="text-muted-foreground text-sm">Website: www.neuroai.com</p>
            </div>
          </section>

          {/* Alterações */}
          <section className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-2xl font-bold text-foreground mb-4">13. Alterações a Esta Política</h2>
            <p className="text-muted-foreground leading-relaxed">
              Podemos atualizar esta Política de Privacidade periodicamente. Notificaremos você sobre mudanças significativas
              por email ou aviso proeminente na plataforma. Seu uso continuado após alterações constitui aceitação.
            </p>
          </section>
        </div>

        {/* Footer */}
        <div className="mt-16 pt-8 border-t border-border flex gap-4 justify-center">
          <Link href="/login">
            <Button variant="outline">Voltar ao Login</Button>
          </Link>
          <Link href="/terms">
            <Button variant="ghost">Termos de Serviço</Button>
          </Link>
        </div>
      </div>
    </div>
  )
}
