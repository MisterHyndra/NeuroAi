# 🚀 Guia de Setup Git - NeuroAI

## Passos para subir o projeto no GitHub

### 1. Inicializar repositório Git (se ainda não foi feito)

```bash
cd "C:\Users\pvpne\OneDrive\Desktop\Rede Neural"
git init
```

### 2. Adicionar remote do GitHub

```bash
git remote add origin https://github.com/MisterHyndra/NeuroAi.git
```

Se já existir um remote, remova primeiro:
```bash
git remote remove origin
git remote add origin https://github.com/MisterHyndra/NeuroAi.git
```

### 3. Verificar o que será commitado

```bash
git status
```

**IMPORTANTE**: Verifique se `datasets/` NÃO aparece na lista (deve estar no .gitignore)

### 4. Adicionar arquivos ao staging

```bash
git add .
```

### 5. Fazer commit inicial

```bash
git commit -m "Initial commit: NeuroAI - Sistema de Diagnóstico Cerebral com Docker e CI/CD"
```

### 6. Renomear branch para main (se necessário)

```bash
git branch -M main
```

### 7. Push para GitHub

```bash
git push -u origin main
```

## ⚠️ Verificações Importantes

### Antes de fazer push, verifique:

1. **Datasets não estão sendo commitados:**
   ```bash
   git check-ignore datasets/
   ```
   Deve retornar: `datasets/`

2. **Modelos grandes não estão sendo commitados:**
   ```bash
   git check-ignore models/*.h5
   ```

3. **Tamanho do repositório:**
   ```bash
   git count-objects -vH
   ```

## 📝 Comandos Úteis

### Ver o que será commitado:
```bash
git status
```

### Ver diferenças:
```bash
git diff
```

### Adicionar arquivo específico:
```bash
git add nome_do_arquivo.py
```

### Ver histórico:
```bash
git log --oneline
```

## 🔄 Atualizações Futuras

Para fazer atualizações no código:

```bash
# 1. Ver mudanças
git status

# 2. Adicionar mudanças
git add .

# 3. Commit
git commit -m "Descrição das mudanças"

# 4. Push
git push origin main
```

## 🐳 Docker Commands

Depois do push, você pode testar o Docker:

```bash
# Build
docker build -t neuroai .

# Run
docker-compose up
```



