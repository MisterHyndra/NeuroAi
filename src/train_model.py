"""
Script principal para treinamento dos modelos de diagnóstico de câncer
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight
import tensorflow as tf
from tensorflow.keras.utils import to_categorical

# Imports locais
from preprocessing import CancerImagePreprocessor
from model_architecture import CancerCNNModels

class CancerModelTrainer:
    def __init__(self, config=None):
        """
        Inicializa o treinador de modelos
        
        Args:
            config: Dicionário com configurações de treinamento
        """
        self.config = config or self._get_default_config()
        self.preprocessor = CancerImagePreprocessor(
            img_size=self.config['img_size'],
            batch_size=self.config['batch_size']
        )
        self.models = CancerCNNModels(
            input_shape=(*self.config['img_size'], 3),
            num_classes=self.config['num_classes']
        )
        
        # Criar diretórios necessários
        os.makedirs('models', exist_ok=True)
        os.makedirs('results', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
    
    def _get_default_config(self):
        """Configurações padrão para treinamento"""
        return {
            'img_size': (224, 224),
            'batch_size': 32,
            'num_classes': 2,  # Binário por padrão (benigno/maligno)
            'epochs': 50,
            'learning_rate': 0.001,
            'validation_split': 0.2,
            'test_split': 0.2,
            'model_type': 'advanced_cnn',  # 'basic_cnn', 'advanced_cnn', 'transfer_learning'
            'transfer_base': 'vgg16'  # Para transfer learning
        }
    
    def load_data(self, dataset_paths):
        """
        Carrega e prepara os dados para treinamento
        
        Args:
            dataset_paths: Dict com caminhos para datasets de cada tipo de câncer
        """
        print("📊 Carregando dados...")
        
        # Carregar e preprocessar imagens
        X, y, class_names = self.preprocessor.load_and_preprocess_images(dataset_paths)
        
        if len(X) == 0:
            raise ValueError("Nenhuma imagem foi carregada. Verifique os caminhos dos datasets.")
        
        # Dividir dados
        X_train, X_val, X_test, y_train, y_val, y_test = self.preprocessor.split_data(
            X, y, 
            test_size=self.config['test_split'],
            val_size=self.config['validation_split']
        )
        
        # Converter labels para categorical se necessário
        if self.config['num_classes'] > 2:
            y_train = to_categorical(y_train, self.config['num_classes'])
            y_val = to_categorical(y_val, self.config['num_classes'])
            y_test = to_categorical(y_test, self.config['num_classes'])
        
        return (X_train, X_val, X_test, y_train, y_val, y_test), class_names
    
    def create_model(self):
        """Cria o modelo baseado na configuração"""
        print(f"🏗️ Criando modelo: {self.config['model_type']}")
        
        if self.config['model_type'] == 'basic_cnn':
            model = self.models.create_basic_cnn()
        elif self.config['model_type'] == 'advanced_cnn':
            model = self.models.create_advanced_cnn()
        elif self.config['model_type'] == 'transfer_learning':
            model = self.models.create_transfer_learning_model(
                base_model_name=self.config['transfer_base'],
                trainable_layers=5
            )
        else:
            raise ValueError(f"Tipo de modelo não suportado: {self.config['model_type']}")
        
        # Compilar modelo
        model = self.models.compile_model(model, learning_rate=self.config['learning_rate'])
        
        print(f"✅ Modelo criado com {model.count_params():,} parâmetros")
        return model
    
    def calculate_class_weights(self, y_train):
        """Calcula pesos das classes para lidar com desbalanceamento"""
        if self.config['num_classes'] == 2:
            # Para classificação binária
            class_weights = compute_class_weight(
                'balanced',
                classes=np.unique(y_train),
                y=y_train
            )
            return dict(enumerate(class_weights))
        else:
            # Para classificação multi-classe
            y_train_labels = np.argmax(y_train, axis=1) if len(y_train.shape) > 1 else y_train
            class_weights = compute_class_weight(
                'balanced',
                classes=np.unique(y_train_labels),
                y=y_train_labels
            )
            return dict(enumerate(class_weights))
    
    def train_model(self, model, X_train, y_train, X_val, y_val):
        """
        Treina o modelo
        
        Args:
            model: Modelo compilado
            X_train, y_train: Dados de treinamento
            X_val, y_val: Dados de validação
        """
        print("🚀 Iniciando treinamento...")
        
        # Calcular pesos das classes
        class_weights = self.calculate_class_weights(y_train)
        print(f"⚖️ Pesos das classes: {class_weights}")
        
        # Criar callbacks
        callbacks = self.models.get_callbacks(
            model_name=f"{self.config['model_type']}_cancer_model"
        )
        
        # Criar geradores de dados com augmentation
        train_generator, val_generator = self.preprocessor.create_data_generators(
            X_train, y_train, X_val, y_val
        )
        
        # Treinar modelo
        history = model.fit(
            train_generator,
            epochs=self.config['epochs'],
            validation_data=val_generator,
            class_weight=class_weights,
            callbacks=callbacks,
            verbose=1
        )
        
        print("✅ Treinamento concluído!")
        return history, model
    
    def evaluate_model(self, model, X_test, y_test, class_names=None):
        """
        Avalia o modelo nos dados de teste
        
        Args:
            model: Modelo treinado
            X_test, y_test: Dados de teste
            class_names: Nomes das classes
        """
        print("📈 Avaliando modelo...")
        
        # Fazer predições
        y_pred = model.predict(X_test)
        
        # Converter predições para classes
        if self.config['num_classes'] == 2:
            y_pred_classes = (y_pred > 0.5).astype(int).flatten()
            y_test_classes = y_test.astype(int)
        else:
            y_pred_classes = np.argmax(y_pred, axis=1)
            y_test_classes = np.argmax(y_test, axis=1) if len(y_test.shape) > 1 else y_test
        
        # Calcular métricas
        test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
        
        print(f"📊 Resultados do teste:")
        print(f"   Loss: {test_loss:.4f}")
        print(f"   Accuracy: {test_accuracy:.4f}")
        
        # Relatório de classificação
        target_names = class_names if class_names else [f"Classe {i}" for i in range(self.config['num_classes'])]
        if self.config['num_classes'] == 2:
            target_names = ['Benigno', 'Maligno']
        
        report = classification_report(y_test_classes, y_pred_classes, target_names=target_names)
        print(f"\n📋 Relatório de classificação:\n{report}")
        
        # Matriz de confusão
        cm = confusion_matrix(y_test_classes, y_pred_classes)
        
        return {
            'test_loss': test_loss,
            'test_accuracy': test_accuracy,
            'classification_report': report,
            'confusion_matrix': cm,
            'predictions': y_pred,
            'true_labels': y_test_classes,
            'pred_labels': y_pred_classes
        }
    
    def plot_training_history(self, history, save_path='results/training_history.png'):
        """Plota histórico de treinamento"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Accuracy
        ax1.plot(history.history['accuracy'], label='Treino')
        ax1.plot(history.history['val_accuracy'], label='Validação')
        ax1.set_title('Acurácia do Modelo')
        ax1.set_xlabel('Época')
        ax1.set_ylabel('Acurácia')
        ax1.legend()
        ax1.grid(True)
        
        # Loss
        ax2.plot(history.history['loss'], label='Treino')
        ax2.plot(history.history['val_loss'], label='Validação')
        ax2.set_title('Loss do Modelo')
        ax2.set_xlabel('Época')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✅ Histórico de treinamento salvo em '{save_path}'")
    
    def plot_confusion_matrix(self, cm, class_names=None, save_path='results/confusion_matrix.png'):
        """Plota matriz de confusão"""
        plt.figure(figsize=(10, 8))
        
        if class_names is None:
            if self.config['num_classes'] == 2:
                class_names = ['Benigno', 'Maligno']
            else:
                class_names = [f'Classe {i}' for i in range(self.config['num_classes'])]
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=class_names, yticklabels=class_names)
        plt.title('Matriz de Confusão')
        plt.xlabel('Predição')
        plt.ylabel('Verdadeiro')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✅ Matriz de confusão salva em '{save_path}'")
    
    def save_model_and_results(self, model, history, evaluation_results, model_name=None):
        """Salva modelo e resultados"""
        if model_name is None:
            model_name = f"{self.config['model_type']}_cancer_model"
        
        # Salvar modelo
        model_path = f"models/{model_name}.h5"
        model.save(model_path)
        print(f"💾 Modelo salvo em '{model_path}'")
        
        # Salvar configuração
        config_path = f"models/{model_name}_config.txt"
        with open(config_path, 'w') as f:
            f.write("CONFIGURAÇÃO DO MODELO\n")
            f.write("=" * 30 + "\n")
            for key, value in self.config.items():
                f.write(f"{key}: {value}\n")
        
        # Salvar resultados
        results_path = f"results/{model_name}_results.txt"
        with open(results_path, 'w') as f:
            f.write("RESULTADOS DA AVALIAÇÃO\n")
            f.write("=" * 30 + "\n")
            f.write(f"Test Loss: {evaluation_results['test_loss']:.4f}\n")
            f.write(f"Test Accuracy: {evaluation_results['test_accuracy']:.4f}\n\n")
            f.write("RELATÓRIO DE CLASSIFICAÇÃO:\n")
            f.write(evaluation_results['classification_report'])
        
        print(f"📄 Resultados salvos em '{results_path}'")

def main():
    """Função principal para treinamento"""
    
    print("🎯 Iniciando treinamento do modelo de diagnóstico de câncer")
    print("=" * 60)
    
    # Configuração
    config = {
        'img_size': (224, 224),
        'batch_size': 16,  # Reduzido para economizar memória
        'num_classes': 2,
        'epochs': 20,  # Reduzido para teste
        'learning_rate': 0.001,
        'validation_split': 0.2,
        'test_split': 0.2,
        'model_type': 'advanced_cnn',  # Pode alterar para 'basic_cnn' ou 'transfer_learning'
        'transfer_base': 'vgg16'
    }
    
    # Paths dos datasets
    dataset_paths = {
        'breast_cancer': 'datasets/breast_cancer',
        'skin_cancer': 'datasets/skin_cancer',
        'lung_cancer': 'datasets/lung_cancer',
        'brain_cancer': 'datasets/brain_cancer'
    }
    
    # Verificar se pelo menos um dataset existe
    existing_datasets = {k: v for k, v in dataset_paths.items() if os.path.exists(v)}
    
    if not existing_datasets:
        print("❌ Nenhum dataset encontrado!")
        print("📝 Execute primeiro o script de download de dados:")
        print("   python src/data_downloader.py")
        return
    
    print(f"📁 Datasets encontrados: {list(existing_datasets.keys())}")
    
    try:
        # Criar trainer
        trainer = CancerModelTrainer(config)
        
        # Carregar dados
        (X_train, X_val, X_test, y_train, y_val, y_test), class_names = trainer.load_data(existing_datasets)
        
        # Criar modelo
        model = trainer.create_model()
        
        # Treinar modelo
        history, trained_model = trainer.train_model(model, X_train, y_train, X_val, y_val)
        
        # Avaliar modelo
        evaluation_results = trainer.evaluate_model(trained_model, X_test, y_test, class_names)
        
        # Plotar resultados
        trainer.plot_training_history(history)
        trainer.plot_confusion_matrix(evaluation_results['confusion_matrix'], class_names)
        
        # Salvar modelo e resultados
        trainer.save_model_and_results(trained_model, history, evaluation_results)
        
        print("\n🎉 Treinamento concluído com sucesso!")
        print(f"🎯 Acurácia final: {evaluation_results['test_accuracy']:.2%}")
        
    except Exception as e:
        print(f"❌ Erro durante o treinamento: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()