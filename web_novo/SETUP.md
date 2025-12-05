# Integração Web NeuroAI - Novo Layout (Next.js)

## 📋 Resumo da Migração

A pasta `web_novo` contém a nova versão do frontend usando **Next.js + TypeScript + Tailwind CSS** com todas as funcionalidades da versão anterior integradas.

## 🎯 Funcionalidades Implementadas

✅ **Autenticação**
- Login integrado com API Flask
- Tokens JWT
- Persistência com localStorage
- Credenciais demo (admin/admin)

✅ **Dashboard Principal**
- Upload de imagens com drag-and-drop
- Análise em tempo real
- Visualização de resultados
- Estatísticas de uso

✅ **Análise de Imagens**
- Chamadas à API `/api/predict`
- Processamento com threshold ajustável
- Histórico de análises
- Gráficos de confiança

✅ **Interface Moderna**
- Design responsivo
- Dark mode ready
- Componentes Shadcn/UI
- Tailwind CSS

## 🚀 Como Rodar

### 1. Instalação de dependências
```bash
cd web_novo
npm install
# ou
pnpm install
```

### 2. Configurar variáveis de ambiente
Crie um arquivo `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

### 3. Iniciar servidor de desenvolvimento
```bash
npm run dev
# ou
pnpm dev
```

A aplicação estará disponível em: **http://localhost:3000**

### 4. Build para produção
```bash
npm run build
npm run start
```

## 📁 Estrutura do Projeto

```
web_novo/
├── app/
│   ├── dashboard/          # Página do dashboard
│   │   ├── analysis/       # Análise detalhada
│   │   ├── history/        # Histórico de análises
│   │   ├── patients/       # Gerenciamento de pacientes
│   │   ├── reports/        # Relatórios
│   │   └── settings/       # Configurações
│   ├── login/              # Página de login
│   ├── layout.tsx          # Layout principal
│   ├── page.tsx            # Home/Landing page
│   └── globals.css         # Estilos globais
├── components/
│   ├── ui/                 # Componentes base (Shadcn)
│   ├── image-analysis-dashboard-integrated.tsx   # Dashboard com funcionalidade
│   ├── login-form.tsx      # Formulário de login integrado
│   ├── analysis-results.tsx # Resultados dinâmicos
│   ├── image-uploader.tsx  # Upload de imagens
│   └── ...                 # Outros componentes
├── lib/                    # Utilitários
├── styles/                 # Estilos customizados
└── package.json

```

## 🔑 Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `NEXT_PUBLIC_API_URL` | URL da API Flask | http://localhost:5000/api |

## 🛠️ Backend Requirements

O backend Flask deve estar rodando e fornecer as seguintes rotas:

### Autenticação
- `POST /api/auth/login` - Login do usuário
- `POST /api/auth/verify` - Verificar token
- `POST /api/auth/logout` - Logout

### Predição
- `POST /api/predict` - Analisar imagem (FormData)
  - Parâmetros: `image` (File), `threshold` (float)
  - Retorna: `{ prediction, confidence, ... }`

### Histórico
- `GET /api/analysis/history` - Listar análises
- `POST /api/analysis/history` - Salvar análise
- `GET /api/analysis/:id` - Detalhe de análise

### Saúde
- `GET /api/health` - Status do servidor

## 📝 Mudanças Principais em Relação à Web Original

| Aspecto | Antes | Depois |
|--------|-------|--------|
| Framework | HTML/CSS/JS puro | Next.js 16 + TypeScript |
| Styling | CSS customizado | Tailwind CSS 4 |
| Componentes | Vanilla JS | React Components |
| Dark Mode | Manual CSS | Next-themes |
| Build | Static | Next.js SSR/SSG |
| DX | Manual | Hot reload + TypeScript |

## 🔄 Próximos Passos

1. **[ ] Testar login** - Verificar autenticação com admin/admin
2. **[ ] Testar upload** - Enviar imagem e validar predição
3. **[ ] Testar histórico** - Verificar persistência de análises
4. **[ ] Adicionar mais tipos de câncer** - Expandir tipos suportados
5. **[ ] Implementar relatórios em PDF** - Exportar resultados
6. **[ ] Implementar pacientes** - Gerenciar dados de pacientes

## ⚡ Performance

- Componentes lazy-loaded
- Imagens otimizadas
- Code splitting automático
- Static site generation onde possível

## 🐛 Troubleshooting

### "Cannot find module '@/components/...'"
Verifique se o `tsconfig.json` contém o alias `@`:
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

### "API connection refused"
Certifique-se de que o backend Flask está rodando em `http://localhost:5000`

### Porta 3000 já em uso
Use: `npm run dev -- -p 3001`

## 📞 Suporte

Para dúvidas sobre a integração, consulte:
- Documentação Next.js: https://nextjs.org/docs
- Shadcn UI: https://ui.shadcn.com
- Tailwind CSS: https://tailwindcss.com

---

**Data de Criação:** Dezembro 2025  
**Status:** Em desenvolvimento  
**Versão:** 0.1.0
