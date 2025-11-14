"""
Interface para fazer predições com modelos de diagnóstico de câncer
"""
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class CancerPredictor:
    def __init__(self, model_path=None):
        """
        Inicializa o preditor de câncer
        
        Args:
            model_path: Caminho para o modelo treinado
        """
        self.model = None
        self.model_path = model_path
        self.img_size = (224, 224)
        
        # Mapeamento de classes
        self.class_names = {
            0: 'Benigno',
            1: 'Maligno'
        }
        
        # Tipos de câncer suportados
        self.cancer_types = {
            'breast_cancer': 'Câncer de Mama',
            'skin_cancer': 'Câncer de Pele', 
            'lung_cancer': 'Câncer de Pulmão',
            'brain_cancer': 'Câncer Cerebral'
        }
        
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path):
        """Carrega modelo treinado"""
        try:
            self.model = load_model(model_path)
            self.model_path = model_path
            print(f"✅ Modelo carregado: {model_path}")
            return True
        except Exception as e:
            print(f"❌ Erro ao carregar modelo: {e}")
            return False
    
    def preprocess_image(self, image_path):
        """
        Pré-processa imagem para predição
        
        Args:
            image_path: Caminho para a imagem
            
        Returns:
            Imagem preprocessada
        """
        try:
            # Carregar imagem
            if isinstance(image_path, str):
                img = cv2.imread(image_path)
                if img is None:
                    raise ValueError(f"Não foi possível carregar a imagem: {image_path}")
            else:
                # Se já é um array numpy
                img = image_path
            
            # Converter BGR para RGB
            if len(img.shape) == 3 and img.shape[2] == 3:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Redimensionar
            img = cv2.resize(img, self.img_size)
            
            # Normalizar
            img = img.astype(np.float32) / 255.0
            
            # Expandir dimensões para batch
            img = np.expand_dims(img, axis=0)
            
            return img
            
        except Exception as e:
            print(f"❌ Erro ao preprocessar imagem: {e}")
            return None
    
    def predict_single_image(self, image_path, show_confidence=True):
        """
        Faz predição para uma única imagem
        
        Args:
            image_path: Caminho para a imagem
            show_confidence: Se deve mostrar a confiança da predição
            
        Returns:
            Dicionário com resultado da predição
        """
        if self.model is None:
            return {"error": "Modelo não carregado"}
        
        # Preprocessar imagem
        img = self.preprocess_image(image_path)
        if img is None:
            return {"error": "Erro ao processar imagem"}
        
        try:
            # Fazer predição
            prediction = self.model.predict(img, verbose=0)
            
            # Interpretar resultado
            if len(prediction.shape) == 1 or prediction.shape[1] == 1:
                # Classificação binária
                probability = float(prediction[0][0]) if len(prediction.shape) > 1 else float(prediction[0])
                predicted_class = 1 if probability > 0.5 else 0
                confidence = probability if probability > 0.5 else 1 - probability
            else:
                # Classificação multi-classe
                predicted_class = int(np.argmax(prediction[0]))
                confidence = float(np.max(prediction[0]))
                probability = float(prediction[0][predicted_class])
            
            # Preparar resultado
            result = {
                "predicted_class": predicted_class,
                "class_name": self.class_names.get(predicted_class, f"Classe {predicted_class}"),
                "confidence": confidence,
                "probability": probability,
                "raw_prediction": prediction[0].tolist()
            }
            
            if show_confidence:
                print(f"🔍 Predição: {result['class_name']}")
                print(f"📊 Confiança: {confidence:.2%}")
            
            return result
            
        except Exception as e:
            return {"error": f"Erro na predição: {str(e)}"}
    
    def predict_batch(self, image_paths, save_results=True):
        """
        Faz predição para múltiplas imagens
        
        Args:
            image_paths: Lista de caminhos para imagens
            save_results: Se deve salvar resultados em arquivo
            
        Returns:
            Lista com resultados das predições
        """
        if self.model is None:
            print("❌ Modelo não carregado")
            return []
        
        results = []
        print(f"🔄 Processando {len(image_paths)} imagens...")
        
        for i, img_path in enumerate(image_paths):
            print(f"   {i+1}/{len(image_paths)}: {os.path.basename(img_path)}")
            
            result = self.predict_single_image(img_path, show_confidence=False)
            result["image_path"] = img_path
            result["image_name"] = os.path.basename(img_path)
            results.append(result)
        
        if save_results:
            self.save_batch_results(results)
        
        return results
    
    def save_batch_results(self, results, filename="results/batch_predictions.csv"):
        """Salva resultados em arquivo CSV"""
        try:
            import pandas as pd
            
            # Preparar dados para DataFrame
            data = []
            for result in results:
                if "error" not in result:
                    data.append({
                        "image_name": result["image_name"],
                        "image_path": result["image_path"],
                        "predicted_class": result["predicted_class"],
                        "class_name": result["class_name"],
                        "confidence": result["confidence"],
                        "probability": result["probability"]
                    })
            
            # Criar DataFrame e salvar
            df = pd.DataFrame(data)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            df.to_csv(filename, index=False)
            print(f"💾 Resultados salvos em: {filename}")
            
        except Exception as e:
            print(f"❌ Erro ao salvar resultados: {e}")
    
    def visualize_prediction(self, image_path, result=None, save_path=None):
        """
        Visualiza imagem com resultado da predição
        
        Args:
            image_path: Caminho para a imagem
            result: Resultado da predição (opcional)
            save_path: Caminho para salvar visualização
        """
        if result is None:
            result = self.predict_single_image(image_path, show_confidence=False)
        
        if "error" in result:
            print(f"❌ {result['error']}")
            return
        
        # Carregar e exibir imagem
        try:
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            plt.figure(figsize=(10, 8))
            plt.imshow(img)
            
            # Adicionar título com resultado
            title = f"Predição: {result['class_name']}\n"
            title += f"Confiança: {result['confidence']:.1%}"
            
            # Cor baseada na predição
            color = 'red' if result['predicted_class'] == 1 else 'green'
            plt.title(title, fontsize=16, color=color, weight='bold')
            plt.axis('off')
            
            # Salvar se especificado
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"💾 Visualização salva: {save_path}")
            
            plt.show()
            
        except Exception as e:
            print(f"❌ Erro na visualização: {e}")
    
    def create_gui_interface(self):
        """Cria interface gráfica para predições"""
        
        class CancerPredictorGUI:
            def __init__(self, predictor):
                self.predictor = predictor
                self.root = tk.Tk()
                self.root.title("Diagnóstico de Câncer - IA")
                self.root.geometry("600x500")
                
                self.setup_gui()
            
            def setup_gui(self):
                """Configura interface gráfica"""
                
                # Título
                title_label = tk.Label(
                    self.root, 
                    text="🏥 Sistema de Diagnóstico de Câncer por IA",
                    font=("Arial", 16, "bold")
                )
                title_label.pack(pady=20)
                
                # Frame para seleção de modelo
                model_frame = ttk.LabelFrame(self.root, text="Modelo", padding=10)
                model_frame.pack(pady=10, padx=20, fill="x")
                
                # Lista de modelos
                self.model_var = tk.StringVar()
                self.model_combo = ttk.Combobox(model_frame, textvariable=self.model_var, width=50)
                self.update_model_list()
                self.model_combo.pack(pady=5)
                
                ttk.Button(model_frame, text="Carregar Modelo", command=self.load_selected_model).pack(pady=5)
                
                # Frame para imagem
                image_frame = ttk.LabelFrame(self.root, text="Imagem para Análise", padding=10)
                image_frame.pack(pady=10, padx=20, fill="x")
                
                ttk.Button(image_frame, text="Selecionar Imagem", command=self.select_image).pack(pady=5)
                
                self.image_label = tk.Label(image_frame, text="Nenhuma imagem selecionada", fg="gray")
                self.image_label.pack(pady=5)
                
                # Frame para predição
                predict_frame = ttk.LabelFrame(self.root, text="Diagnóstico", padding=10)
                predict_frame.pack(pady=10, padx=20, fill="both", expand=True)
                
                ttk.Button(predict_frame, text="🔍 Analisar Imagem", command=self.predict_image).pack(pady=10)
                
                # Área de resultados
                self.result_text = tk.Text(predict_frame, height=10, wrap=tk.WORD)
                self.result_text.pack(fill="both", expand=True, pady=5)
                
                # Scrollbar para texto
                scrollbar = ttk.Scrollbar(predict_frame, orient="vertical", command=self.result_text.yview)
                scrollbar.pack(side="right", fill="y")
                self.result_text.configure(yscrollcommand=scrollbar.set)
                
                # Variáveis
                self.selected_image = None
            
            def update_model_list(self):
                """Atualiza lista de modelos disponíveis"""
                models_dir = "models"
                if os.path.exists(models_dir):
                    model_files = [f for f in os.listdir(models_dir) if f.endswith('.h5')]
                    self.model_combo['values'] = model_files
                    if model_files:
                        self.model_combo.set(model_files[0])
            
            def load_selected_model(self):
                """Carrega modelo selecionado"""
                model_name = self.model_var.get()
                if not model_name:
                    messagebox.showerror("Erro", "Selecione um modelo")
                    return
                
                model_path = os.path.join("models", model_name)
                if self.predictor.load_model(model_path):
                    messagebox.showinfo("Sucesso", f"Modelo carregado: {model_name}")
                else:
                    messagebox.showerror("Erro", "Falha ao carregar modelo")
            
            def select_image(self):
                """Seleciona imagem para análise"""
                file_path = filedialog.askopenfilename(
                    title="Selecionar Imagem",
                    filetypes=[
                        ("Imagens", "*.jpg *.jpeg *.png *.bmp *.tiff"),
                        ("Todos os arquivos", "*.*")
                    ]
                )
                
                if file_path:
                    self.selected_image = file_path
                    self.image_label.config(text=f"Imagem: {os.path.basename(file_path)}", fg="black")
            
            def predict_image(self):
                """Faz predição da imagem selecionada"""
                if self.predictor.model is None:
                    messagebox.showerror("Erro", "Carregue um modelo primeiro")
                    return
                
                if self.selected_image is None:
                    messagebox.showerror("Erro", "Selecione uma imagem primeiro")
                    return
                
                # Fazer predição
                result = self.predictor.predict_single_image(self.selected_image, show_confidence=False)
                
                # Exibir resultado
                self.result_text.delete(1.0, tk.END)
                
                if "error" in result:
                    self.result_text.insert(tk.END, f"❌ Erro: {result['error']}")
                else:
                    output = f"🔍 RESULTADO DO DIAGNÓSTICO\n"
                    output += f"{'='*40}\n\n"
                    output += f"📄 Imagem: {os.path.basename(self.selected_image)}\n"
                    output += f"🎯 Diagnóstico: {result['class_name']}\n"
                    output += f"📊 Confiança: {result['confidence']:.1%}\n"
                    output += f"📈 Probabilidade: {result['probability']:.3f}\n\n"
                    
                    if result['predicted_class'] == 1:
                        output += "⚠️ ATENÇÃO: Possível caso maligno detectado!\n"
                        output += "Recomenda-se avaliação médica especializada.\n"
                    else:
                        output += "✅ Resultado sugere caso benigno.\n"
                        output += "Sempre consulte um médico para confirmação.\n"
                    
                    output += f"\n📋 AVISO IMPORTANTE:\n"
                    output += f"Este sistema é uma ferramenta de apoio e não substitui\n"
                    output += f"o diagnóstico médico profissional. Sempre consulte\n"
                    output += f"um médico especialista para avaliação definitiva."
                    
                    self.result_text.insert(tk.END, output)
            
            def run(self):
                """Executa interface gráfica"""
                self.root.mainloop()
        
        # Criar e executar GUI
        gui = CancerPredictorGUI(self)
        gui.run()

def main():
    """Função principal para interface de predição"""
    
    print("🔮 Interface de Predição - Diagnóstico de Câncer")
    print("=" * 50)
    
    # Verificar se existem modelos
    models_dir = "models"
    if not os.path.exists(models_dir):
        print("❌ Diretório de modelos não encontrado!")
        print("Execute primeiro o treinamento: python src/train_model.py")
        return
    
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.h5')]
    
    if not model_files:
        print("❌ Nenhum modelo encontrado!")
        print("Execute primeiro o treinamento: python src/train_model.py")
        return
    
    # Criar preditor
    predictor = CancerPredictor()
    
    # Menu de opções
    while True:
        print("\n📋 OPÇÕES DISPONÍVEIS:")
        print("1. 🖥️  Interface Gráfica (GUI)")
        print("2. 📸 Predição de imagem única")
        print("3. 📁 Predição em lote (múltiplas imagens)")
        print("4. 📊 Listar modelos disponíveis")
        print("5. 🚪 Sair")
        
        choice = input("\nEscolha uma opção (1-5): ").strip()
        
        if choice == "1":
            print("🖥️ Abrindo interface gráfica...")
            predictor.create_gui_interface()
        
        elif choice == "2":
            # Carregar modelo se necessário
            if predictor.model is None:
                print("\n📁 Modelos disponíveis:")
                for i, model in enumerate(model_files):
                    print(f"   {i+1}. {model}")
                
                try:
                    model_idx = int(input("Escolha o modelo (número): ")) - 1
                    if 0 <= model_idx < len(model_files):
                        model_path = os.path.join(models_dir, model_files[model_idx])
                        if not predictor.load_model(model_path):
                            continue
                    else:
                        print("❌ Escolha inválida")
                        continue
                except ValueError:
                    print("❌ Digite um número válido")
                    continue
            
            # Selecionar imagem
            image_path = input("Digite o caminho da imagem: ").strip()
            if os.path.exists(image_path):
                result = predictor.predict_single_image(image_path)
                if "error" not in result:
                    predictor.visualize_prediction(image_path, result)
            else:
                print("❌ Arquivo não encontrado")
        
        elif choice == "3":
            # Predição em lote
            if predictor.model is None:
                print("❌ Carregue um modelo primeiro (opção 2)")
                continue
            
            folder_path = input("Digite o caminho da pasta com imagens: ").strip()
            if os.path.exists(folder_path):
                # Encontrar imagens na pasta
                image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
                image_paths = []
                
                for file in os.listdir(folder_path):
                    if any(file.lower().endswith(ext) for ext in image_extensions):
                        image_paths.append(os.path.join(folder_path, file))
                
                if image_paths:
                    results = predictor.predict_batch(image_paths)
                    print(f"✅ Processadas {len(results)} imagens")
                else:
                    print("❌ Nenhuma imagem encontrada na pasta")
            else:
                print("❌ Pasta não encontrada")
        
        elif choice == "4":
            print("\n📁 Modelos disponíveis:")
            for i, model in enumerate(model_files):
                print(f"   {i+1}. {model}")
        
        elif choice == "5":
            print("👋 Saindo...")
            break
        
        else:
            print("❌ Opção inválida")

if __name__ == "__main__":
    main()