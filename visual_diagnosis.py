"""
Interface Visual para Diagnóstico de Câncer com IA
Mostra imagem e resultado completo do diagnóstico
"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from tensorflow.keras.models import load_model

class VisualCancerDiagnosis:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏥 Sistema de Diagnóstico de Câncer por IA")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Variáveis
        self.model = None
        self.current_image = None
        self.current_image_path = None
        
        # Configurações do modelo
        self.img_size = (128, 128)
        
        # Mapeamento de tipos de câncer
        self.cancer_info = {
            'brain_cancer': {
                'name': 'Câncer Cerebral',
                'emoji': '🧠',
                'description': 'Tumor cerebral detectado em imagem de ressonância magnética',
                'color_positive': '#ff6b6b',
                'color_negative': '#51cf66'
            }
        }
        
        self.setup_gui()
        self.load_default_model()
    
    def setup_gui(self):
        """Configura a interface gráfica"""
        
        # Título principal
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🏥 SISTEMA DE DIAGNÓSTICO DE CÂNCER POR IA",
            font=("Arial", 20, "bold"),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Frame esquerdo - Controles
        left_frame = tk.Frame(main_frame, bg='#f0f0f0', width=300)
        left_frame.pack(side='left', fill='y', padx=(0, 20))
        left_frame.pack_propagate(False)
        
        # Frame direito - Visualização
        right_frame = tk.Frame(main_frame, bg='white', relief='solid', borderwidth=1)
        right_frame.pack(side='right', fill='both', expand=True)
        
        self.setup_controls(left_frame)
        self.setup_visualization(right_frame)
    
    def setup_controls(self, parent):
        """Configura os controles da interface"""
        
        # Seleção de modelo
        model_frame = tk.LabelFrame(parent, text="🤖 Modelo", font=("Arial", 12, "bold"), 
                                   bg='#f0f0f0', padx=10, pady=10)
        model_frame.pack(fill='x', pady=(0, 15))
        
        self.model_var = tk.StringVar()
        self.model_combo = ttk.Combobox(model_frame, textvariable=self.model_var, width=35)
        self.update_model_list()
        self.model_combo.pack(pady=5)
        
        load_model_btn = tk.Button(
            model_frame, text="Carregar Modelo", command=self.load_selected_model,
            bg='#3498db', fg='white', font=("Arial", 10, "bold"),
            relief='flat', padx=20, pady=5
        )
        load_model_btn.pack(pady=5)
        
        # Status do modelo
        self.model_status = tk.Label(
            model_frame, text="❌ Nenhum modelo carregado", 
            font=("Arial", 9), bg='#f0f0f0', fg='#e74c3c'
        )
        self.model_status.pack(pady=5)
        
        # Seleção de imagem
        image_frame = tk.LabelFrame(parent, text="📷 Imagem para Análise", 
                                   font=("Arial", 12, "bold"), bg='#f0f0f0', padx=10, pady=10)
        image_frame.pack(fill='x', pady=(0, 15))
        
        select_image_btn = tk.Button(
            image_frame, text="📁 Selecionar Imagem", command=self.select_image,
            bg='#2ecc71', fg='white', font=("Arial", 11, "bold"),
            relief='flat', padx=20, pady=8
        )
        select_image_btn.pack(pady=5)
        
        self.image_status = tk.Label(
            image_frame, text="Nenhuma imagem selecionada",
            font=("Arial", 9), bg='#f0f0f0', fg='#7f8c8d'
        )
        self.image_status.pack(pady=5)
        
        # Análise
        analysis_frame = tk.LabelFrame(parent, text="🔍 Análise", 
                                      font=("Arial", 12, "bold"), bg='#f0f0f0', padx=10, pady=10)
        analysis_frame.pack(fill='x', pady=(0, 15))
        
        analyze_btn = tk.Button(
            analysis_frame, text="🔬 ANALISAR IMAGEM", command=self.analyze_image,
            bg='#e74c3c', fg='white', font=("Arial", 12, "bold"),
            relief='flat', padx=20, pady=12
        )
        analyze_btn.pack(pady=10)
        
        # Resultado
        result_frame = tk.LabelFrame(parent, text="📋 Resultado do Diagnóstico", 
                                    font=("Arial", 12, "bold"), bg='#f0f0f0', padx=10, pady=10)
        result_frame.pack(fill='both', expand=True)
        
        # Área de resultado com scrollbar
        result_text_frame = tk.Frame(result_frame, bg='#f0f0f0')
        result_text_frame.pack(fill='both', expand=True)
        
        self.result_text = tk.Text(
            result_text_frame, wrap='word', font=("Arial", 10),
            bg='#ffffff', relief='flat', borderwidth=0, padx=10, pady=10
        )
        
        scrollbar = tk.Scrollbar(result_text_frame, orient='vertical', command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def setup_visualization(self, parent):
        """Configura a área de visualização"""
        
        # Título da visualização
        viz_title = tk.Label(
            parent, text="🖼️ Visualização da Análise", 
            font=("Arial", 16, "bold"), bg='white', pady=15
        )
        viz_title.pack()
        
        # Frame para a imagem
        self.image_frame = tk.Frame(parent, bg='white')
        self.image_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Label para exibir a imagem
        self.image_label = tk.Label(
            self.image_frame, 
            text="📷\n\nSelecione uma imagem\npara começar a análise",
            font=("Arial", 14), bg='white', fg='#bdc3c7'
        )
        self.image_label.pack(expand=True)
        
        # Frame para gráficos de confiança
        self.confidence_frame = tk.Frame(parent, bg='white')
        self.confidence_frame.pack(fill='x', padx=20, pady=(0, 20))
    
    def update_model_list(self):
        """Atualiza lista de modelos disponíveis"""
        models_dir = "models"
        if os.path.exists(models_dir):
            model_files = [f for f in os.listdir(models_dir) if f.endswith(('.h5', '.keras'))]
            self.model_combo['values'] = model_files
            if model_files:
                self.model_combo.set(model_files[0])
    
    def load_default_model(self):
        """Carrega modelo padrão se disponível"""
        demo_model = "models/demo_brain_cancer_model.h5"
        if os.path.exists(demo_model):
            self.load_model(demo_model)
    
    def load_selected_model(self):
        """Carrega modelo selecionado"""
        model_name = self.model_var.get()
        if not model_name:
            messagebox.showerror("Erro", "Selecione um modelo")
            return
        
        model_path = os.path.join("models", model_name)
        self.load_model(model_path)
    
    def load_model(self, model_path):
        """Carrega um modelo específico"""
        try:
            self.model = load_model(model_path)
            self.model_status.config(
                text=f"✅ Modelo carregado: {os.path.basename(model_path)}", 
                fg='#27ae60'
            )
            print(f"✅ Modelo carregado: {model_path}")
        except Exception as e:
            self.model_status.config(text="❌ Erro ao carregar modelo", fg='#e74c3c')
            messagebox.showerror("Erro", f"Falha ao carregar modelo:\n{str(e)}")
    
    def select_image(self):
        """Seleciona imagem para análise"""
        file_path = filedialog.askopenfilename(
            title="Selecionar Imagem Médica",
            filetypes=[
                ("Imagens", "*.jpg *.jpeg *.png *.bmp *.tiff *.dcm"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("DICOM", "*.dcm"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if file_path:
            self.current_image_path = file_path
            self.display_image(file_path)
            self.image_status.config(
                text=f"📁 {os.path.basename(file_path)}", 
                fg='#2c3e50'
            )
    
    def display_image(self, image_path):
        """Exibe a imagem selecionada"""
        try:
            # Carregar e redimensionar imagem para display
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Redimensionar mantendo proporção
            height, width = img.shape[:2]
            max_size = 400
            
            if width > height:
                new_width = max_size
                new_height = int(height * max_size / width)
            else:
                new_height = max_size
                new_width = int(width * max_size / height)
            
            img_resized = cv2.resize(img, (new_width, new_height))
            
            # Converter para formato do tkinter
            img_pil = Image.fromarray(img_resized)
            img_tk = ImageTk.PhotoImage(img_pil)
            
            # Atualizar label da imagem
            self.image_label.config(image=img_tk, text="")
            self.image_label.image = img_tk  # Manter referência
            
            # Salvar imagem original para processamento
            self.current_image = img
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem:\n{str(e)}")
    
    def preprocess_image(self, image):
        """Pré-processa imagem para o modelo"""
        try:
            # Redimensionar para o tamanho esperado pelo modelo
            img = cv2.resize(image, self.img_size)
            
            # Normalizar
            img = img.astype(np.float32) / 255.0
            
            # Expandir dimensões
            img = np.expand_dims(img, axis=0)
            
            return img
        except Exception as e:
            raise Exception(f"Erro no pré-processamento: {str(e)}")
    
    def analyze_image(self):
        """Realiza análise da imagem"""
        if self.model is None:
            messagebox.showerror("Erro", "Carregue um modelo primeiro")
            return
        
        if self.current_image is None:
            messagebox.showerror("Erro", "Selecione uma imagem primeiro")
            return
        
        try:
            # Pré-processar imagem
            processed_img = self.preprocess_image(self.current_image)
            
            # Fazer predição
            prediction = self.model.predict(processed_img, verbose=0)
            
            # Interpretar resultado
            probability = float(prediction[0][0])
            is_positive = probability > 0.5
            confidence = probability if is_positive else 1 - probability
            
            # Exibir resultado detalhado
            self.display_result(is_positive, confidence, probability)
            
            # Exibir gráfico de confiança
            self.display_confidence_chart(confidence, is_positive)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro durante análise:\n{str(e)}")
    
    def display_result(self, is_positive, confidence, probability):
        """Exibe resultado detalhado do diagnóstico"""
        
        self.result_text.delete(1.0, tk.END)
        
        # Cabeçalho do resultado
        result_header = "🔬 RESULTADO DO DIAGNÓSTICO\n"
        result_header += "=" * 50 + "\n\n"
        
        # Informações da imagem
        image_info = f"📄 Arquivo: {os.path.basename(self.current_image_path)}\n"
        image_info += f"📊 Modelo: Diagnóstico de Câncer Cerebral\n"
        image_info += f"🕐 Data/Hora: {self.get_current_time()}\n\n"
        
        # Resultado principal
        if is_positive:
            diagnosis = "🔴 POSSÍVEL TUMOR DETECTADO\n\n"
            diagnosis += f"🧠 Tipo: Câncer Cerebral\n"
            diagnosis += f"📈 Probabilidade: {probability:.1%}\n"
            diagnosis += f"🎯 Confiança: {confidence:.1%}\n\n"
            diagnosis += "⚠️ ATENÇÃO MÉDICA NECESSÁRIA\n"
            diagnosis += "Este resultado sugere a presença de um possível\n"
            diagnosis += "tumor cerebral. É FUNDAMENTAL buscar avaliação\n"
            diagnosis += "médica especializada imediatamente.\n\n"
        else:
            diagnosis = "✅ RESULTADO NORMAL\n\n"
            diagnosis += f"🧠 Tipo: Câncer Cerebral\n"
            diagnosis += f"📈 Probabilidade de normalidade: {1-probability:.1%}\n"
            diagnosis += f"🎯 Confiança: {confidence:.1%}\n\n"
            diagnosis += "✅ RESULTADO FAVORÁVEL\n"
            diagnosis += "A análise não detectou sinais evidentes de\n"
            diagnosis += "tumor cerebral na imagem fornecida.\n\n"
        
        # Aviso médico
        medical_warning = "⚕️ AVISO MÉDICO IMPORTANTE:\n"
        medical_warning += "-" * 40 + "\n"
        medical_warning += "• Este sistema é uma FERRAMENTA DE APOIO\n"
        medical_warning += "• NÃO substitui diagnóstico médico profissional\n"
        medical_warning += "• Sempre consulte um médico especialista\n"
        medical_warning += "• Use apenas como triagem inicial\n\n"
        
        # Recomendações
        recommendations = "📋 RECOMENDAÇÕES:\n"
        recommendations += "-" * 20 + "\n"
        if is_positive:
            recommendations += "• Procure um neurologista ou neurocirurgião\n"
            recommendations += "• Realize exames complementares\n"
            recommendations += "• Não ignore este resultado\n"
            recommendations += "• Mantenha a calma e busque ajuda médica\n"
        else:
            recommendations += "• Mantenha acompanhamento médico regular\n"
            recommendations += "• Continue exames preventivos\n"
            recommendations += "• Consulte médico se houver sintomas\n"
            recommendations += "• Este resultado não exclui outras condições\n"
        
        # Combinar todo o texto
        full_result = result_header + image_info + diagnosis + medical_warning + recommendations
        
        self.result_text.insert(tk.END, full_result)
        
        # Configurar cores baseadas no resultado
        if is_positive:
            self.result_text.tag_add("positive", "3.0", "3.end")
            self.result_text.tag_config("positive", foreground="#e74c3c", font=("Arial", 12, "bold"))
        else:
            self.result_text.tag_add("negative", "3.0", "3.end") 
            self.result_text.tag_config("negative", foreground="#27ae60", font=("Arial", 12, "bold"))
    
    def display_confidence_chart(self, confidence, is_positive):
        """Exibe gráfico de confiança"""
        
        # Limpar frame anterior
        for widget in self.confidence_frame.winfo_children():
            widget.destroy()
        
        # Criar figura matplotlib
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3))
        fig.patch.set_facecolor('white')
        
        # Gráfico de barras - confiança
        categories = ['Normal', 'Tumor']
        values = [1-confidence if is_positive else confidence, 
                 confidence if is_positive else 1-confidence]
        colors = ['#27ae60' if not is_positive else '#e74c3c', 
                 '#e74c3c' if is_positive else '#27ae60']
        
        bars = ax1.bar(categories, values, color=colors, alpha=0.7)
        ax1.set_ylim(0, 1)
        ax1.set_ylabel('Probabilidade')
        ax1.set_title('Classificação')
        ax1.grid(True, alpha=0.3)
        
        # Adicionar valores nas barras
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{value:.1%}', ha='center', va='bottom', fontweight='bold')
        
        # Gráfico de pizza - confiança
        sizes = [confidence, 1-confidence]
        labels = ['Predição', 'Incerteza']
        colors_pie = ['#3498db', '#ecf0f1']
        
        wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=colors_pie, 
                                          autopct='%1.1f%%', startangle=90)
        ax2.set_title(f'Nível de Confiança: {confidence:.1%}')
        
        plt.tight_layout()
        
        # Incorporar no tkinter
        canvas = FigureCanvasTkAgg(fig, self.confidence_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def get_current_time(self):
        """Retorna data/hora atual formatada"""
        from datetime import datetime
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def run(self):
        """Executa a interface"""
        self.root.mainloop()

def main():
    """Função principal"""
    print("🏥 Iniciando Interface Visual de Diagnóstico de Câncer...")
    
    try:
        app = VisualCancerDiagnosis()
        app.run()
    except Exception as e:
        print(f"❌ Erro ao inicializar interface: {e}")

if __name__ == "__main__":
    main()