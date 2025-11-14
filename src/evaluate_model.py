"""
Script para avaliação detalhada dos modelos de diagnóstico de câncer
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_curve, auc,
    precision_recall_curve, average_precision_score
)
import tensorflow as tf
from tensorflow.keras.models import load_model

class CancerModelEvaluator:
    def __init__(self, model_path):
        """
        Inicializa o avaliador de modelos
        
        Args:
            model_path: Caminho para o modelo salvo
        """
        self.model_path = model_path
        self.model = self.load_model()
        
    def load_model(self):
        """Carrega o modelo salvo"""
        try:
            model = load_model(self.model_path)
            print(f"✅ Modelo carregado de: {self.model_path}")
            return model
        except Exception as e:
            print(f"❌ Erro ao carregar modelo: {e}")
            return None
    
    def evaluate_comprehensive(self, X_test, y_test, class_names=None):
        """
        Realiza avaliação abrangente do modelo
        
        Args:
            X_test: Dados de teste
            y_test: Labels verdadeiros
            class_names: Nomes das classes
        """
        if self.model is None:
            print("❌ Modelo não carregado")
            return None
        
        print("🔍 Iniciando avaliação abrangente...")
        
        # Fazer predições
        y_pred_proba = self.model.predict(X_test)
        
        # Determinar se é classificação binária ou multi-classe
        is_binary = len(y_pred_proba.shape) == 1 or y_pred_proba.shape[1] == 1
        
        if is_binary:
            y_pred_classes = (y_pred_proba > 0.5).astype(int).flatten()
            y_test_classes = y_test.astype(int) if len(y_test.shape) == 1 else y_test.flatten()
        else:
            y_pred_classes = np.argmax(y_pred_proba, axis=1)
            y_test_classes = np.argmax(y_test, axis=1) if len(y_test.shape) > 1 else y_test
        
        # Métricas básicas
        test_loss, test_accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        
        # Relatório de classificação
        if class_names is None:
            if is_binary:
                class_names = ['Benigno', 'Maligno']
            else:
                class_names = [f'Classe {i}' for i in range(y_pred_proba.shape[1])]
        
        report = classification_report(
            y_test_classes, y_pred_classes, 
            target_names=class_names, 
            output_dict=True
        )
        
        # Matriz de confusão
        cm = confusion_matrix(y_test_classes, y_pred_classes)
        
        # Compilar resultados
        results = {
            'test_loss': test_loss,
            'test_accuracy': test_accuracy,
            'classification_report': report,
            'confusion_matrix': cm,
            'y_true': y_test_classes,
            'y_pred': y_pred_classes,
            'y_pred_proba': y_pred_proba,
            'class_names': class_names,
            'is_binary': is_binary
        }
        
        print(f"📊 Acurácia: {test_accuracy:.4f}")
        print(f"📊 Loss: {test_loss:.4f}")
        
        return results
    
    def plot_confusion_matrix(self, results, save_path='results/detailed_confusion_matrix.png'):
        """Plota matriz de confusão detalhada"""
        cm = results['confusion_matrix']
        class_names = results['class_names']
        
        plt.figure(figsize=(10, 8))
        
        # Calcular percentuais
        cm_percent = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
        
        # Criar anotações
        annotations = []
        for i in range(cm.shape[0]):
            row = []
            for j in range(cm.shape[1]):
                row.append(f'{cm[i,j]}\n({cm_percent[i,j]:.1f}%)')
            annotations.append(row)
        
        sns.heatmap(cm, annot=annotations, fmt='', cmap='Blues',
                   xticklabels=class_names, yticklabels=class_names)
        
        plt.title('Matriz de Confusão Detalhada')
        plt.xlabel('Predição')
        plt.ylabel('Verdadeiro')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✅ Matriz de confusão salva em: {save_path}")
    
    def plot_roc_curves(self, results, save_path='results/roc_curves.png'):
        """Plota curvas ROC"""
        if not results['is_binary']:
            print("⚠️ Curvas ROC implementadas apenas para classificação binária")
            return
        
        y_true = results['y_true']
        y_scores = results['y_pred_proba'].flatten()
        
        # Calcular ROC
        fpr, tpr, _ = roc_curve(y_true, y_scores)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(10, 8))
        plt.plot(fpr, tpr, color='darkorange', lw=2, 
                label=f'ROC curve (AUC = {roc_auc:.3f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Taxa de Falsos Positivos')
        plt.ylabel('Taxa de Verdadeiros Positivos')
        plt.title('Curva ROC - Diagnóstico de Câncer')
        plt.legend(loc="lower right")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✅ Curva ROC salva em: {save_path}")
        print(f"📊 AUC Score: {roc_auc:.3f}")
        
        return roc_auc
    
    def plot_precision_recall_curve(self, results, save_path='results/precision_recall_curve.png'):
        """Plota curva Precision-Recall"""
        if not results['is_binary']:
            print("⚠️ Curva PR implementada apenas para classificação binária")
            return
        
        y_true = results['y_true']
        y_scores = results['y_pred_proba'].flatten()
        
        # Calcular Precision-Recall
        precision, recall, _ = precision_recall_curve(y_true, y_scores)
        avg_precision = average_precision_score(y_true, y_scores)
        
        plt.figure(figsize=(10, 8))
        plt.plot(recall, precision, color='blue', lw=2,
                label=f'PR curve (AP = {avg_precision:.3f})')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Curva Precision-Recall - Diagnóstico de Câncer')
        plt.legend(loc="lower left")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✅ Curva PR salva em: {save_path}")
        print(f"📊 Average Precision: {avg_precision:.3f}")
        
        return avg_precision
    
    def analyze_errors(self, results, X_test, num_examples=8):
        """Analisa erros de classificação"""
        y_true = results['y_true']
        y_pred = results['y_pred']
        y_pred_proba = results['y_pred_proba']
        
        # Encontrar erros
        error_indices = np.where(y_true != y_pred)[0]
        
        if len(error_indices) == 0:
            print("🎉 Nenhum erro encontrado!")
            return
        
        print(f"❌ Total de erros: {len(error_indices)} de {len(y_true)} ({len(error_indices)/len(y_true)*100:.1f}%)")
        
        # Selecionar alguns exemplos para visualização
        num_examples = min(num_examples, len(error_indices))
        selected_errors = np.random.choice(error_indices, num_examples, replace=False)
        
        # Plotar erros
        fig, axes = plt.subplots(2, 4, figsize=(20, 10))
        axes = axes.ravel()
        
        for i, idx in enumerate(selected_errors):
            if i >= len(axes):
                break
                
            axes[i].imshow(X_test[idx])
            
            true_label = results['class_names'][y_true[idx]]
            pred_label = results['class_names'][y_pred[idx]]
            
            if results['is_binary']:
                confidence = y_pred_proba[idx][0] if y_pred_proba[idx][0] > 0.5 else 1 - y_pred_proba[idx][0]
            else:
                confidence = np.max(y_pred_proba[idx])
            
            axes[i].set_title(f'Verdadeiro: {true_label}\nPredito: {pred_label}\nConfiança: {confidence:.2f}')
            axes[i].axis('off')
        
        plt.tight_layout()
        plt.savefig('results/error_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Análise de erros salva em: results/error_analysis.png")
    
    def generate_detailed_report(self, results, save_path='results/detailed_evaluation_report.txt'):
        """Gera relatório detalhado da avaliação"""
        
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DETALHADO DE AVALIAÇÃO\n")
            f.write("=" * 50 + "\n\n")
            
            # Métricas gerais
            f.write("MÉTRICAS GERAIS\n")
            f.write("-" * 20 + "\n")
            f.write(f"Acurácia: {results['test_accuracy']:.4f}\n")
            f.write(f"Loss: {results['test_loss']:.4f}\n\n")
            
            # Relatório de classificação
            f.write("RELATÓRIO DE CLASSIFICAÇÃO\n")
            f.write("-" * 30 + "\n")
            
            report = results['classification_report']
            for class_name in results['class_names']:
                if class_name in report:
                    metrics = report[class_name]
                    f.write(f"\n{class_name.upper()}:\n")
                    f.write(f"  Precision: {metrics['precision']:.3f}\n")
                    f.write(f"  Recall: {metrics['recall']:.3f}\n")
                    f.write(f"  F1-Score: {metrics['f1-score']:.3f}\n")
                    f.write(f"  Support: {metrics['support']}\n")
            
            # Métricas macro e weighted
            f.write(f"\nMÉTRICAS AGREGADAS:\n")
            if 'macro avg' in report:
                macro = report['macro avg']
                f.write(f"Macro Avg - Precision: {macro['precision']:.3f}, Recall: {macro['recall']:.3f}, F1: {macro['f1-score']:.3f}\n")
            if 'weighted avg' in report:
                weighted = report['weighted avg']
                f.write(f"Weighted Avg - Precision: {weighted['precision']:.3f}, Recall: {weighted['recall']:.3f}, F1: {weighted['f1-score']:.3f}\n")
            
            # Matriz de confusão
            f.write(f"\nMATRIZ DE CONFUSÃO\n")
            f.write("-" * 20 + "\n")
            cm = results['confusion_matrix']
            f.write(f"Classes: {results['class_names']}\n")
            f.write(f"{cm}\n")
        
        print(f"📄 Relatório detalhado salvo em: {save_path}")

def main():
    """Função principal para avaliação"""
    
    print("📊 Avaliação Detalhada do Modelo de Diagnóstico de Câncer")
    print("=" * 60)
    
    # Verificar se existem modelos salvos
    model_dir = "models"
    if not os.path.exists(model_dir):
        print("❌ Diretório de modelos não encontrado!")
        print("Execute primeiro o treinamento: python src/train_model.py")
        return
    
    # Listar modelos disponíveis
    model_files = [f for f in os.listdir(model_dir) if f.endswith('.h5')]
    
    if not model_files:
        print("❌ Nenhum modelo encontrado!")
        print("Execute primeiro o treinamento: python src/train_model.py")
        return
    
    print("📁 Modelos disponíveis:")
    for i, model_file in enumerate(model_files):
        print(f"   {i+1}. {model_file}")
    
    # Selecionar modelo
    try:
        choice = int(input("\nEscolha o modelo para avaliar (número): ")) - 1
        if 0 <= choice < len(model_files):
            selected_model = model_files[choice]
        else:
            print("❌ Escolha inválida")
            return
    except ValueError:
        print("❌ Por favor digite um número válido")
        return
    
    model_path = os.path.join(model_dir, selected_model)
    print(f"🔍 Avaliando modelo: {selected_model}")
    
    # Carregar dados de teste (você precisa implementar isso)
    # Por enquanto, vamos usar dados sintéticos para demonstração
    print("⚠️ Usando dados sintéticos para demonstração")
    print("   Para usar dados reais, carregue seus dados de teste aqui")
    
    # Dados sintéticos para demonstração
    X_test = np.random.rand(100, 224, 224, 3)
    y_test = np.random.randint(0, 2, 100)
    
    try:
        # Criar avaliador
        evaluator = CancerModelEvaluator(model_path)
        
        # Realizar avaliação abrangente
        results = evaluator.evaluate_comprehensive(X_test, y_test)
        
        if results:
            # Plotar visualizações
            evaluator.plot_confusion_matrix(results)
            
            if results['is_binary']:
                evaluator.plot_roc_curves(results)
                evaluator.plot_precision_recall_curve(results)
            
            # Analisar erros
            evaluator.analyze_errors(results, X_test)
            
            # Gerar relatório detalhado
            evaluator.generate_detailed_report(results)
            
            print("\n🎉 Avaliação concluída!")
            print(f"📊 Resumo: Acurácia = {results['test_accuracy']:.2%}")
    
    except Exception as e:
        print(f"❌ Erro durante avaliação: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()