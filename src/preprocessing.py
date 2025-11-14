"""
Módulo de pré-processamento de imagens para diagnóstico de câncer
"""
import os
import cv2
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
from tqdm import tqdm

class CancerImagePreprocessor:
    def __init__(self, img_size=(224, 224), batch_size=32):
        self.img_size = img_size
        self.batch_size = batch_size
        self.cancer_types = {
            'breast_cancer': 0,
            'skin_cancer': 1, 
            'lung_cancer': 2,
            'brain_cancer': 3
        }
        
    def load_and_preprocess_images(self, dataset_paths):
        """
        Carrega e pré-processa imagens de todos os tipos de câncer
        
        Args:
            dataset_paths: Dict com caminhos para cada tipo de câncer
            
        Returns:
            X: Array de imagens preprocessadas
            y: Array de labels
            class_names: Lista com nomes das classes
        """
        images = []
        labels = []
        class_names = []
        
        print("🔄 Carregando e preprocessando imagens...")
        
        for cancer_type, type_id in self.cancer_types.items():
            if cancer_type not in dataset_paths:
                print(f"⚠️ Dataset não encontrado para {cancer_type}")
                continue
                
            dataset_path = dataset_paths[cancer_type]
            if not os.path.exists(dataset_path):
                print(f"⚠️ Caminho não existe: {dataset_path}")
                continue
            
            print(f"📁 Processando {cancer_type}...")
            
            # Carregar imagens para este tipo de câncer
            cancer_images, cancer_labels = self._load_cancer_type_images(
                dataset_path, type_id, cancer_type
            )
            
            images.extend(cancer_images)
            labels.extend(cancer_labels)
            class_names.append(cancer_type)
        
        # Converter para arrays numpy
        X = np.array(images)
        y = np.array(labels)
        
        print(f"✅ Total de imagens carregadas: {len(X)}")
        print(f"📊 Distribuição por classe: {np.bincount(y)}")
        
        return X, y, class_names
    
    def _load_cancer_type_images(self, dataset_path, type_id, cancer_type):
        """Carrega imagens de um tipo específico de câncer"""
        images = []
        labels = []
        
        # Estratégias diferentes para cada tipo de dataset
        if cancer_type == "breast_cancer":
            images, labels = self._load_breast_cancer_images(dataset_path, type_id)
        elif cancer_type == "skin_cancer":
            images, labels = self._load_skin_cancer_images(dataset_path, type_id)
        elif cancer_type == "lung_cancer":
            images, labels = self._load_lung_cancer_images(dataset_path, type_id)
        elif cancer_type == "brain_cancer":
            images, labels = self._load_brain_cancer_images(dataset_path, type_id)
        
        return images, labels
    
    def _load_breast_cancer_images(self, dataset_path, type_id):
        """Carrega imagens de câncer de mama"""
        images = []
        labels = []
        
        # Procurar por subdiretórios (IDC_negative, IDC_positive, etc.)
        for root, dirs, files in os.walk(dataset_path):
            for file in files[:1000]:  # Limitar para exemplo
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(root, file)
                    img = self._load_and_resize_image(img_path)
                    if img is not None:
                        images.append(img)
                        
                        # Determinar label baseado no nome do arquivo ou diretório
                        if 'positive' in root.lower() or '1.png' in file:
                            labels.append(1)  # Maligno
                        else:
                            labels.append(0)  # Benigno
        
        return images, labels
    
    def _load_skin_cancer_images(self, dataset_path, type_id):
        """Carrega imagens de câncer de pele"""
        images = []
        labels = []
        
        for root, dirs, files in os.walk(dataset_path):
            for file in files[:1000]:  # Limitar para exemplo
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(root, file)
                    img = self._load_and_resize_image(img_path)
                    if img is not None:
                        images.append(img)
                        
                        # Determinar label baseado no diretório
                        if 'malignant' in root.lower():
                            labels.append(1)  # Maligno
                        else:
                            labels.append(0)  # Benigno
        
        return images, labels
    
    def _load_lung_cancer_images(self, dataset_path, type_id):
        """Carrega imagens de câncer de pulmão"""
        images = []
        labels = []
        
        for root, dirs, files in os.walk(dataset_path):
            for file in files[:1000]:  # Limitar para exemplo
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(root, file)
                    img = self._load_and_resize_image(img_path)
                    if img is not None:
                        images.append(img)
                        
                        # Determinar label baseado no diretório
                        if any(word in root.lower() for word in ['cancer', 'malignant', 'adenocarcinoma']):
                            labels.append(1)  # Maligno
                        else:
                            labels.append(0)  # Normal/Benigno
        
        return images, labels
    
    def _load_brain_cancer_images(self, dataset_path, type_id):
        """Carrega imagens de câncer cerebral"""
        images = []
        labels = []
        
        for root, dirs, files in os.walk(dataset_path):
            for file in files[:1000]:  # Limitar para exemplo
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(root, file)
                    img = self._load_and_resize_image(img_path)
                    if img is not None:
                        images.append(img)
                        
                        # Determinar label baseado no diretório
                        if any(word in root.lower() for word in ['tumor', 'glioma', 'meningioma']):
                            labels.append(1)  # Tumor
                        else:
                            labels.append(0)  # Normal
        
        return images, labels
    
    def _load_and_resize_image(self, img_path):
        """Carrega e redimensiona uma imagem"""
        try:
            # Carregar imagem
            img = cv2.imread(img_path)
            if img is None:
                return None
                
            # Converter de BGR para RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Redimensionar
            img = cv2.resize(img, self.img_size)
            
            # Normalizar para 0-1
            img = img.astype(np.float32) / 255.0
            
            return img
            
        except Exception as e:
            print(f"❌ Erro ao carregar imagem {img_path}: {e}")
            return None
    
    def create_data_generators(self, X_train, y_train, X_val, y_val):
        """Cria geradores de dados com data augmentation"""
        
        # Data augmentation para treino
        train_datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )
        
        # Apenas normalização para validação
        val_datagen = ImageDataGenerator()
        
        # Criar geradores
        train_generator = train_datagen.flow(
            X_train, y_train,
            batch_size=self.batch_size,
            shuffle=True
        )
        
        val_generator = val_datagen.flow(
            X_val, y_val,
            batch_size=self.batch_size,
            shuffle=False
        )
        
        return train_generator, val_generator
    
    def split_data(self, X, y, test_size=0.2, val_size=0.2):
        """Divide dados em treino, validação e teste"""
        
        # Primeiro split: treino+val vs teste
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Segundo split: treino vs validação
        val_ratio = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_ratio, random_state=42, stratify=y_temp
        )
        
        print(f"📊 Divisão dos dados:")
        print(f"   Treino: {len(X_train)} amostras")
        print(f"   Validação: {len(X_val)} amostras") 
        print(f"   Teste: {len(X_test)} amostras")
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def visualize_samples(self, X, y, class_names, num_samples=12):
        """Visualiza amostras das imagens"""
        fig, axes = plt.subplots(3, 4, figsize=(15, 12))
        axes = axes.ravel()
        
        # Selecionar amostras aleatórias
        indices = np.random.choice(len(X), num_samples, replace=False)
        
        for i, idx in enumerate(indices):
            axes[i].imshow(X[idx])
            
            # Determinar tipo de câncer e label
            cancer_type = "Unknown"
            label_text = "Benigno" if y[idx] == 0 else "Maligno"
            
            axes[i].set_title(f"{cancer_type} - {label_text}")
            axes[i].axis('off')
        
        plt.tight_layout()
        plt.savefig('results/sample_images.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Visualização salva em 'results/sample_images.png'")

def main():
    """Função principal para teste do preprocessamento"""
    
    # Paths dos datasets (ajuste conforme necessário)
    dataset_paths = {
        'breast_cancer': 'datasets/breast_cancer',
        'skin_cancer': 'datasets/skin_cancer',
        'lung_cancer': 'datasets/lung_cancer', 
        'brain_cancer': 'datasets/brain_cancer'
    }
    
    # Criar preprocessador
    preprocessor = CancerImagePreprocessor(img_size=(224, 224))
    
    # Carregar e preprocessar dados
    X, y, class_names = preprocessor.load_and_preprocess_images(dataset_paths)
    
    if len(X) > 0:
        # Dividir dados
        X_train, X_val, X_test, y_train, y_val, y_test = preprocessor.split_data(X, y)
        
        # Visualizar amostras
        preprocessor.visualize_samples(X, y, class_names)
        
        # Salvar dados preprocessados
        np.save('datasets/X_preprocessed.npy', X)
        np.save('datasets/y_preprocessed.npy', y)
        
        print("✅ Dados preprocessados salvos!")
    else:
        print("❌ Nenhuma imagem foi carregada. Verifique os caminhos dos datasets.")

if __name__ == "__main__":
    main()