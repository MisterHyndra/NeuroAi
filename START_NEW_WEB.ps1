#!/usr/bin/env powershell
# Script para iniciar o novo web_novo com todas as funcionalidades

Write-Host "
╔════════════════════════════════════════════════════════════╗
║       NeuroAI Diagnostics - Nova Web (Next.js)            ║
║                    Setup & Start Guide                    ║
╚════════════════════════════════════════════════════════════╝
" -ForegroundColor Cyan

Write-Host "📦 Status da Integração:" -ForegroundColor Green
Write-Host "  ✅ Estrutura Next.js copiada"
Write-Host "  ✅ Componentes integrados com API"
Write-Host "  ✅ Autenticação configurada"
Write-Host "  ✅ Upload de imagens integrado"
Write-Host "  ✅ Análise de imagens funcionando"
Write-Host "  ✅ Backup da web original criado"
Write-Host ""

Write-Host "📁 Localizações:" -ForegroundColor Cyan
Write-Host "  Nova Web (USE ESTA):     ./web_novo"
Write-Host "  Backup da Original:       ./web_backup_original"
Write-Host "  Web Original (deprecated): ./web"
Write-Host ""

Write-Host "🚀 Próximos passos:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Navegar para a pasta web_novo:"
Write-Host "   cd web_novo"
Write-Host ""
Write-Host "2. Instalar dependências:"
Write-Host "   npm install"
Write-Host ""
Write-Host "3. Iniciar servidor de desenvolvimento:"
Write-Host "   npm run dev"
Write-Host ""
Write-Host "4. Acessar a aplicação:"
Write-Host "   http://localhost:3000"
Write-Host ""
Write-Host "5. Fazer login com:"
Write-Host "   Usuário: admin"
Write-Host "   Senha: admin"
Write-Host ""

Write-Host "📋 Funcionalidades Implementadas:" -ForegroundColor Green
Write-Host ""
Write-Host "  🔐 Autenticação"
Write-Host "    - Login integrado com API Flask"
Write-Host "    - Tokens JWT"
Write-Host "    - Proteção de rotas"
Write-Host ""
Write-Host "  📊 Dashboard"
Write-Host "    - Estatísticas em tempo real"
Write-Host "    - Upload de imagens (drag & drop)"
Write-Host "    - Interface moderna"
Write-Host ""
Write-Host "  🔬 Análise de Imagens"
Write-Host "    - Predição com modelo IA"
Write-Host "    - Confiança dinâmica"
Write-Host "    - Ajuste de threshold"
Write-Host "    - Gráficos de probabilidade"
Write-Host ""
Write-Host "  📈 Histórico"
Write-Host "    - Registro de análises"
Write-Host "    - Filtros e busca"
Write-Host "    - Exportação de relatórios"
Write-Host ""

Write-Host "⚙️  Requisitos:" -ForegroundColor Cyan
Write-Host "  ✓ Node.js 18+ instalado"
Write-Host "  ✓ Backend Flask rodando (http://localhost:5000)"
Write-Host "  ✓ Banco de dados configurado"
Write-Host ""

Write-Host "🔌 API Endpoints Necessários:" -ForegroundColor Magenta
Write-Host "  POST   /api/auth/login"
Write-Host "  POST   /api/auth/verify"
Write-Host "  POST   /api/auth/logout"
Write-Host "  POST   /api/predict"
Write-Host "  GET    /api/analysis/history"
Write-Host "  POST   /api/analysis/history"
Write-Host "  GET    /api/health"
Write-Host ""

Write-Host "📚 Documentação:" -ForegroundColor Blue
Write-Host "  Setup completo:  ./web_novo/SETUP.md"
Write-Host "  Informações:     ./NOVO_WEB_INFO.md"
Write-Host ""

Write-Host "💡 Dicas:" -ForegroundColor Yellow
Write-Host "  • Se a porta 3000 estiver em uso:"
Write-Host "    npm run dev -- -p 3001"
Write-Host ""
Write-Host "  • Para build de produção:"
Write-Host "    npm run build && npm run start"
Write-Host ""
Write-Host "  • Limpar cache e reinstalar:"
Write-Host "    rm -r node_modules && npm install"
Write-Host ""

Write-Host "✅ Integração Concluída!" -ForegroundColor Green
Write-Host "   Você está pronto para usar a nova web!"
Write-Host ""
