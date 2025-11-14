# NeuroAI - Dockerfile
# Imagem base Python 3.11 (compatível com TensorFlow)
FROM python:3.11-slim

# Metadados
LABEL maintainer="MisterHyndra"
LABEL description="NeuroAI - Sistema de Diagnóstico Cerebral com IA"
LABEL version="1.0"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (cache layer)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p models results datasets

# Expor porta (para futura versão web)
EXPOSE 8501

# Comando padrão - executar interface gráfica
# Nota: Para GUI, precisa de X11 forwarding ou modo headless
CMD ["python", "visual_diagnosis_modern.py"]

# Alternativa para modo headless (se necessário)
# CMD ["python", "-c", "print('NeuroAI Docker container running')"]



