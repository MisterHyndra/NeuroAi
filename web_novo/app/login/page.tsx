import { LoginForm } from "@/components/login-form"
import { Brain } from "lucide-react"

export default function LoginPage() {
  return (
    <div className="min-h-screen flex">
      {/* Left side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary via-primary/90 to-accent p-12 flex-col justify-between relative overflow-hidden">
        {/* Background pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-96 h-96 bg-primary-foreground rounded-full blur-3xl" />
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-accent rounded-full blur-3xl" />
        </div>

        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-8">
            <div className="w-12 h-12 bg-primary-foreground/20 backdrop-blur rounded-xl flex items-center justify-center">
              <Brain className="w-7 h-7 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-primary-foreground">NeuroAI Diagnostics</h1>
              <p className="text-primary-foreground/80 text-sm">Sistema Inteligente de Diagnóstico</p>
            </div>
          </div>
        </div>

        <div className="relative z-10 space-y-6">
          <div>
            <h2 className="text-4xl font-bold text-primary-foreground mb-4 text-balance">
              Detecção Avançada de Câncer com Inteligência Artificial
            </h2>
            <p className="text-primary-foreground/90 text-lg leading-relaxed">
              Análise precisa de imagens médicas utilizando deep learning para identificação precoce e diagnóstico
              assistido.
            </p>
          </div>

          <div className="grid grid-cols-3 gap-4 pt-8">
            <div className="bg-primary-foreground/10 backdrop-blur rounded-lg p-4">
              <div className="text-3xl font-bold text-primary-foreground">98.5%</div>
              <div className="text-primary-foreground/80 text-sm">Precisão</div>
            </div>
            <div className="bg-primary-foreground/10 backdrop-blur rounded-lg p-4">
              <div className="text-3xl font-bold text-primary-foreground">{"<"}2s</div>
              <div className="text-primary-foreground/80 text-sm">Análise</div>
            </div>
            <div className="bg-primary-foreground/10 backdrop-blur rounded-lg p-4">
              <div className="text-3xl font-bold text-primary-foreground">24/7</div>
              <div className="text-primary-foreground/80 text-sm">Disponível</div>
            </div>
          </div>
        </div>

        <div className="relative z-10 text-primary-foreground/60 text-sm">
          © 2025 NeuroAI Diagnostics. Powered by AI
        </div>
      </div>

      {/* Right side - Login Form */}
      <div className="flex-1 flex items-center justify-center p-8 bg-background">
        <div className="w-full max-w-md">
          {/* Mobile logo */}
          <div className="lg:hidden flex items-center gap-3 mb-8 justify-center">
            <div className="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center">
              <Brain className="w-6 h-6 text-primary" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-foreground">NeuroAI Diagnostics</h1>
            </div>
          </div>

          <div className="mb-8">
            <h2 className="text-3xl font-bold text-foreground mb-2">Bem-vindo de volta</h2>
            <p className="text-muted-foreground">Entre com suas credenciais para acessar o sistema</p>
          </div>

          <LoginForm />

          <p className="text-center text-sm text-muted-foreground mt-8">
            Ao fazer login, você concorda com nossos{" "}
            <a href="#" className="text-primary hover:underline">
              Termos de Serviço
            </a>{" "}
            e{" "}
            <a href="#" className="text-primary hover:underline">
              Política de Privacidade
            </a>
          </p>
        </div>
      </div>
    </div>
  )
}
