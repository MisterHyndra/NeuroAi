"""
Script de início rápido para o sistema de diagnóstico de câncer
"""
import os
import sys
import subprocess

def check_python():
    """Verifica se o Python está disponível"""
    python_path = r"C:\Python313\python.exe"
    
    if not os.path.exists(python_path):
        print("❌ Python não encontrado em C:\\Python313\\python.exe")
        print("📝 Instale o Python 3.13 ou ajuste o caminho no script")
        return False
    
    print(f"✅ Python encontrado: {python_path}")
    return True

def run_setup():
    """Executa setup inicial"""
    print("🔧 Executando setup inicial...")
    try:
        result = subprocess.run([r"C:\Python313\python.exe", "setup.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Setup concluído com sucesso!")
            return True
        else:
            print(f"❌ Erro no setup: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erro ao executar setup: {e}")
        return False

def check_datasets():
    """Verifica se os datasets estão disponíveis"""
    datasets_dir = "datasets"
    
    if not os.path.exists(datasets_dir):
        print("📁 Diretório de datasets não encontrado")
        return False
    
    subdirs = [d for d in os.listdir(datasets_dir) 
              if os.path.isdir(os.path.join(datasets_dir, d))]
    
    if not subdirs:
        print("📁 Nenhum dataset encontrado")
        return False
    
    print(f"✅ Datasets encontrados: {subdirs}")
    return True

def quick_train_demo():
    """Executa treinamento de demonstração rápido"""
    print("🚀 Iniciando treinamento de demonstração...")
    
    # Criar arquivo de configuração demo
    demo_config = '''
# Configuração para demonstração rápida
config = {
    'img_size': (128, 128),      # Imagens menores
    'batch_size': 8,             # Batch pequeno
    'epochs': 3,                 # Poucas épocas
    'learning_rate': 0.001,
    'model_type': 'basic_cnn'    # Modelo simples
}
'''
    
    print("📝 Usando configuração de demonstração:")
    print("   - Imagens: 128x128 pixels")
    print("   - Épocas: 3")
    print("   - Modelo: CNN básica")
    print("\n⏱️ Tempo estimado: 5-10 minutos")
    
    choice = input("\nContinuar com treinamento demo? (s/n): ").lower()
    
    if choice == 's':
        try:
            result = subprocess.run([r"C:\Python313\python.exe", "src/train_model.py"],
                                  capture_output=False)
            
            if result.returncode == 0:
                print("✅ Treinamento demo concluído!")
                return True
            else:
                print("❌ Erro no treinamento")
                return False
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    return False

def main():
    """Função principal do início rápido"""
    
    print("🎯 INÍCIO RÁPIDO - Sistema de Diagnóstico de Câncer")
    print("=" * 60)
    
    # Verificar Python
    if not check_python():
        input("Pressione Enter para sair...")
        return
    
    # Menu de início rápido
    while True:
        print("\n📋 OPÇÕES DE INÍCIO RÁPIDO:")
        print("1. 🔧 Setup completo (primeira vez)")
        print("2. 📥 Baixar datasets")
        print("3. 🚀 Treinamento demo (rápido)")
        print("4. 🔍 Interface de predições")
        print("5. 📊 Verificar status do projeto")
        print("6. 🚪 Sair")
        
        choice = input("\nEscolha uma opção (1-6): ").strip()
        
        if choice == "1":
            print("\n🔧 SETUP COMPLETO")
            print("-" * 20)
            
            # Executar setup
            if run_setup():
                print("\n📥 Agora baixe os datasets (opção 2)")
            
        elif choice == "2":
            print("\n📥 DOWNLOAD DE DATASETS")
            print("-" * 20)
            print("⚠️ Você precisa configurar a API do Kaggle primeiro!")
            print("📝 Instruções:")
            print("   1. Acesse https://www.kaggle.com/account")
            print("   2. Clique em 'Create API Token'")
            print("   3. Salve kaggle.json em C:\\Users\\{seu_usuario}\\.kaggle\\")
            
            continue_download = input("\nAPI configurada? Continuar com download? (s/n): ").lower()
            
            if continue_download == 's':
                try:
                    subprocess.run([r"C:\Python313\python.exe", "src/data_downloader.py"])
                except Exception as e:
                    print(f"❌ Erro: {e}")
        
        elif choice == "3":
            print("\n🚀 TREINAMENTO DEMO")
            print("-" * 20)
            
            if not check_datasets():
                print("❌ Datasets não encontrados! Execute opção 2 primeiro.")
                continue
            
            quick_train_demo()
        
        elif choice == "4":
            print("\n🔍 INTERFACE DE PREDIÇÕES")
            print("-" * 20)
            
            try:
                subprocess.run([r"C:\Python313\python.exe", "src/predict.py"])
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        elif choice == "5":
            print("\n📊 STATUS DO PROJETO")
            print("-" * 20)
            
            # Verificar estrutura
            directories = ["src", "datasets", "models", "results"]
            for dir_name in directories:
                if os.path.exists(dir_name):
                    files_count = len([f for f in os.listdir(dir_name) 
                                     if os.path.isfile(os.path.join(dir_name, f))])
                    print(f"✅ {dir_name}: {files_count} arquivos")
                else:
                    print(f"❌ {dir_name}: não encontrado")
            
            # Verificar modelos treinados
            if os.path.exists("models"):
                model_files = [f for f in os.listdir("models") if f.endswith('.h5')]
                if model_files:
                    print(f"🧠 Modelos treinados: {len(model_files)}")
                    for model in model_files:
                        print(f"   - {model}")
                else:
                    print("🧠 Nenhum modelo treinado encontrado")
        
        elif choice == "6":
            print("\n👋 Saindo do início rápido...")
            break
        
        else:
            print("❌ Opção inválida")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()