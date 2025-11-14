"""
Script para baixar e organizar datasets de câncer de diferentes tipos
"""
import os
import zipfile
import requests
from tqdm import tqdm
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi

class CancerDatasetDownloader:
    def __init__(self, base_path="datasets"):
        self.base_path = base_path
        self.datasets = {
            "breast_cancer": {
                "kaggle_dataset": "paultimothymooney/breast-histopathology-images",
                "local_path": "datasets/breast_cancer",
                "description": "Breast Histopathology Images"
            },
            "skin_cancer": {
                "kaggle_dataset": "fanconic/skin-cancer-malignant-vs-benign",
                "local_path": "datasets/skin_cancer", 
                "description": "Skin Cancer Malignant vs Benign"
            },
            "lung_cancer": {
                "kaggle_dataset": "mohamedhanyyy/chest-ctscan-images",
                "local_path": "datasets/lung_cancer",
                "description": "Chest CT-Scan Images"
            },
            "brain_cancer": {
                "kaggle_dataset": "masoudnickparvar/brain-tumor-mri-dataset",
                "local_path": "datasets/brain_cancer",
                "description": "Brain Tumor MRI Dataset"
            }
        }
    
    def setup_kaggle_api(self):
        """
        Configura a API do Kaggle
        Você precisa ter o arquivo kaggle.json no diretório ~/.kaggle/
        """
        try:
            api = KaggleApi()
            api.authenticate()
            return api
        except Exception as e:
            print(f"❌ Erro ao configurar API do Kaggle: {e}")
            print("📝 Instruções:")
            print("1. Acesse https://www.kaggle.com/account")
            print("2. Clique em 'Create API Token'")
            print("3. Salve o arquivo kaggle.json em ~/.kaggle/")
            print("4. No Windows: C:\\Users\\{username}\\.kaggle\\kaggle.json")
            return None
    
    def download_dataset(self, cancer_type):
        """Baixa um dataset específico do Kaggle"""
        if cancer_type not in self.datasets:
            print(f"❌ Tipo de câncer não suportado: {cancer_type}")
            return False
        
        dataset_info = self.datasets[cancer_type]
        
        print(f"📥 Baixando {dataset_info['description']}...")
        
        api = self.setup_kaggle_api()
        if not api:
            return False
        
        try:
            # Criar diretório se não existir
            os.makedirs(dataset_info['local_path'], exist_ok=True)
            
            # Baixar dataset
            api.dataset_download_files(
                dataset_info['kaggle_dataset'],
                path=dataset_info['local_path'],
                unzip=True
            )
            
            print(f"✅ Dataset {cancer_type} baixado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao baixar dataset {cancer_type}: {e}")
            return False
    
    def download_all_datasets(self):
        """Baixa todos os datasets"""
        print("🚀 Iniciando download de todos os datasets...")
        
        success_count = 0
        for cancer_type in self.datasets.keys():
            if self.download_dataset(cancer_type):
                success_count += 1
        
        print(f"\n📊 Resumo: {success_count}/{len(self.datasets)} datasets baixados com sucesso")
        return success_count == len(self.datasets)
    
    def verify_datasets(self):
        """Verifica se os datasets foram baixados corretamente"""
        print("\n🔍 Verificando datasets...")
        
        for cancer_type, info in self.datasets.items():
            path = info['local_path']
            if os.path.exists(path) and os.listdir(path):
                files_count = sum([len(files) for r, d, files in os.walk(path)])
                print(f"✅ {cancer_type}: {files_count} arquivos encontrados")
            else:
                print(f"❌ {cancer_type}: Dataset não encontrado")

def main():
    """Função principal"""
    downloader = CancerDatasetDownloader()
    
    print("🎯 Cancer Dataset Downloader")
    print("=" * 50)
    
    choice = input("""
Escolha uma opção:
1. Baixar todos os datasets
2. Baixar dataset específico
3. Verificar datasets existentes
4. Sair

Digite sua escolha (1-4): """)
    
    if choice == "1":
        downloader.download_all_datasets()
    elif choice == "2":
        print("\nTipos disponíveis:")
        for i, cancer_type in enumerate(downloader.datasets.keys(), 1):
            print(f"{i}. {cancer_type}")
        
        try:
            selection = int(input("\nEscolha o número do tipo: ")) - 1
            cancer_types = list(downloader.datasets.keys())
            if 0 <= selection < len(cancer_types):
                downloader.download_dataset(cancer_types[selection])
            else:
                print("❌ Seleção inválida")
        except ValueError:
            print("❌ Por favor, digite um número válido")
    elif choice == "3":
        downloader.verify_datasets()
    elif choice == "4":
        print("👋 Saindo...")
        return
    else:
        print("❌ Opção inválida")
    
    downloader.verify_datasets()

if __name__ == "__main__":
    main()