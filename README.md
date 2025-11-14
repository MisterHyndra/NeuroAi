# 🧠 NeuroAI - Sistema de Diagnóstico Cerebral

Sistema inteligente de diagnóstico de tumores cerebrais usando Deep Learning e Redes Neurais Convolucionais (CNN).

## 📋 Sobre o Projeto

O NeuroAI é um sistema de apoio ao diagnóstico médico que utiliza inteligência artificial para detectar tumores cerebrais em imagens de ressonância magnética (RM). O sistema classifica imagens em duas categorias principais:
- **Tecido Normal** (sem tumor)
- **Tumor Cerebral** (Glioma, Meningioma, Pituitário)

## 🚀 Tecnologias Utilizadas

- **Python 3.13**
- **TensorFlow/Keras** - Deep Learning
- **OpenCV** - Processamento de imagens
- **Tkinter** - Interface gráfica desktop
- **NumPy, Matplotlib** - Análise e visualização
- **Docker** - Containerização
- **GitHub Actions** - CI/CD

## 📁 Estrutura do Projeto

```
Rede Neural/
├── src/                    # Código fonte
├── models/                 # Modelos treinados (não versionado)
├── datasets/              # Datasets (não versionado - muito pesado)
├── results/               # Resultados e gráficos
├── visual_diagnosis_modern.py  # Interface principal
├── train_balanced_model.py     # Script de treinamento
├── requirements.txt       # Dependências Python
├── Dockerfile            # Configuração Docker
└── docker-compose.yml    # Orquestração Docker
```

## 🛠️ Instalação

### Opção 1: Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/MisterHyndra/NeuroAi.git
cd NeuroAi
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Baixe o modelo treinado (ou treine um novo):
```bash
# O modelo deve estar em models/brain_cancer_balanced.h5
# Se não existir, execute:
python train_balanced_model.py
```

4. Execute a interface:
```bash
python visual_diagnosis_modern.py
```

### Opção 2: Usando Docker

1. Build da imagem:
```bash
docker build -t neuroai .
```

2. Execute o container:
```bash
docker-compose up
```

Ou diretamente:
```bash
docker run -it --rm -v $(pwd)/models:/app/models neuroai
```

## 📊 Como Usar

1. **Inicie a aplicação** (local ou Docker)
2. **Carregue uma imagem** de ressonância magnética
3. **Ajuste o limiar de decisão** (recomendado: 0.35-0.45)
4. **Clique em "INICIAR DIAGNÓSTICO"**
5. **Visualize os resultados** nos painéis

### Limiar de Decisão

O limiar de decisão é o ponto de corte que determina se uma imagem é classificada como TUMOR ou NORMAL:
- **Limiar baixo (0.30-0.40)**: Mais sensível, detecta mais tumores (pode ter mais falsos positivos)
- **Limiar médio (0.40-0.50)**: Equilíbrio entre sensibilidade e especificidade
- **Limiar alto (0.60-0.80)**: Mais conservador, menos falsos positivos (pode perder alguns tumores)

**Recomendação**: Use 0.35 para melhor detecção de tumores.

## 🧪 Treinamento do Modelo

Para treinar um novo modelo:

```bash
python train_balanced_model.py
```

O modelo será salvo em `models/brain_cancer_balanced.h5`

## 📈 Performance

- **Acurácia geral**: ~55-60% (com limiar ajustado)
- **Imagens normais**: ~90% de acurácia
- **Gliomas**: ~80% de acurácia
- **Meningiomas/Pituitários**: ~40% de acurácia

## ⚠️ Aviso Médico

**Este sistema é uma FERRAMENTA DE APOIO ao diagnóstico médico.**
- NÃO substitui diagnóstico médico profissional
- Sempre consulte um médico especialista
- Resultados devem ser validados por profissionais qualificados

## 🐳 Docker

### Build
```bash
docker build -t neuroai .
```

### Run
```bash
docker-compose up
```

### Desenvolvimento
```bash
docker-compose up --build
```

## 🔄 CI/CD

O projeto utiliza GitHub Actions para:
- ✅ Validação de código
- ✅ Testes automatizados
- ✅ Build de imagens Docker
- ✅ Verificação de dependências

## 📝 Requisitos

- Python 3.13+
- TensorFlow 2.x
- OpenCV
- Tkinter (geralmente já incluído no Python)

## 👥 Autores

- **MisterHyndra** - Desenvolvimento inicial

## 📄 Licença

Este projeto é parte de um Projeto Integrador acadêmico.

## 🙏 Agradecimentos

- Dataset de câncer cerebral utilizado para treinamento
- Comunidade open source de Machine Learning
