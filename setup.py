"""
Script de setup para instalar dependências do projeto de diagnóstico de câncer
"""
import subprocess
import sys
import os

def install_requirements():
    """Instala as dependências necessárias"""
    python_path = r"C:\Python313\python.exe"
    
    print("🔧 Instalando dependências...")
    
    try:
        # Instalar pip se necessário
        subprocess.check_call([python_path, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Instalar dependências
        subprocess.check_call([python_path, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✅ Dependências instaladas com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def create_directories():
    """Cria a estrutura de diretórios do projeto"""
    directories = [
        "datasets",
        "datasets/breast_cancer",
        "datasets/skin_cancer", 
        "datasets/lung_cancer",
        "datasets/brain_cancer",
        "models",
        "results",
        "src",
        "notebooks"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Criado diretório: {directory}")

if __name__ == "__main__":
    print("🚀 Configurando projeto de diagnóstico de câncer...")
    
    create_directories()
    
    if install_requirements():
        print("\n✅ Setup concluído com sucesso!")
        print("\nPróximos passos:")
        print("1. Configure sua API key do Kaggle")
        print("2. Execute o script de download dos dados")
        print("3. Inicie o treinamento dos modelos")
    else:
        print("\n❌ Falha no setup. Verifique as dependências.")