"""
Interface Visual ATUALIZADA para Diagnóstico de Câncer com IA
Usando o modelo corrigido que classifica adequadamente
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

class VisualCancerDiagnosisV2:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏥 Sistema de Diagnóstico de Câncer Cerebral")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Variáveis
        self.model = None
        self.current_image = None
        self.current_image_path = None
        
        # Configurações do modelo
        self.img_size = (128, 128)
        
        # Informações detalhadas sobre tipos de tumor
        self.tumor_info = {
            'glioma': {
                'name': 'Glioma',
                'emoji': '🔴',
                'description': 'Tumor que se origina das células gliais do cérebro',
                'severity': 'Alta',
                'color': '#e74c3c'
            },
            'meningioma': {
                'name': 'Meningioma', 
                'emoji': '🟠',
                'description': 'Tumor que se origina das meninges (membranas do cérebro)',
                'severity': 'Moderada',
                'color': '#f39c12'
            },
            'pituitary': {
                'name': 'Tumor Pituitário',
                'emoji': '🟡',
                'description': 'Tumor na glândula pituitária (hipófise)',
                'severity': 'Moderada',
                'color': '#f1c40f'
            },
            'normal': {
                'name': 'Normal',
                'emoji': '✅',
                'description': 'Tecido cerebral normal, sem sinais de tumor',
                'severity': 'Nenhuma',
                'color': '#27ae60'
            }
        }
        
        self.setup_gui()
        self.load_corrected_model()
    
    def setup_gui(self):
        """Configura a interface gráfica melhorada"""
        
        # Título principal com versão
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=90)
        title_frame.pack(fill='x', pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🧠 DIAGNÓSTICO DE CÂNCER CEREBRAL POR IA",
            font=("Arial", 22, "bold"),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Detecta: Glioma • Meningioma • Tumor Pituitário • Tecido Normal",
            font=("Arial", 12),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        subtitle_label.pack()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Frame esquerdo - Controles
        left_frame = tk.Frame(main_frame, bg='#f0f0f0', width=350)
        left_frame.pack(side='left', fill='y', padx=(0, 20))
        left_frame.pack_propagate(False)
        
        # Frame direito - Visualização  
        right_frame = tk.Frame(main_frame, bg='white', relief='solid', borderwidth=1)
        right_frame.pack(side='right', fill='both', expand=True)
        
        self.setup_controls(left_frame)
        self.setup_visualization(right_frame)
    
    def setup_controls(self, parent):
        """Configura os controles da interface"""
        
        # Status do modelo
        model_frame = tk.LabelFrame(parent, text="🤖 Modelo de IA", font=("Arial", 12, "bold"), 
                                   bg='#f0f0f0', padx=15, pady=15)
        model_frame.pack(fill='x', pady=(0, 15))
        
        self.model_status = tk.Label(
            model_frame, text="🔄 Carregando modelo corrigido...", 
            font=("Arial", 10, "bold"), bg='#f0f0f0', fg='#f39c12'
        )
        self.model_status.pack(pady=5)
        
        model_info = tk.Label(
            model_frame, 
            text="• Treinado com 2.400 imagens\n• Acurácia: 83.96%\n• 4 categorias de diagnóstico",
            font=("Arial", 9), bg='#f0f0f0', fg='#7f8c8d', justify='left'
        )
        model_info.pack(pady=5)
        
        # Seleção de imagem
        image_frame = tk.LabelFrame(parent, text="📷 Imagem para Análise", 
                                   font=("Arial", 12, "bold"), bg='#f0f0f0', padx=15, pady=15)
        image_frame.pack(fill='x', pady=(0, 15))
        
        select_image_btn = tk.Button(
            image_frame, text="📁 Selecionar Imagem de RM", command=self.select_image,
            bg='#3498db', fg='white', font=("Arial", 11, "bold"),
            relief='flat', padx=25, pady=10
        )
        select_image_btn.pack(pady=8)
        
        self.image_status = tk.Label(
            image_frame, text="Aguardando seleção de imagem...",
            font=("Arial", 9), bg='#f0f0f0', fg='#7f8c8d'
        )
        self.image_status.pack(pady=5)
        
        # Guia de uso
        guide_frame = tk.LabelFrame(parent, text="💡 Como Usar", 
                                   font=("Arial", 11, "bold"), bg='#f0f0f0', padx=15, pady=10)
        guide_frame.pack(fill='x', pady=(0, 15))
        
        guide_text = tk.Label(
            guide_frame,
            text="1. Selecione uma imagem de RM cerebral\n" +
                 "2. Clique em 'Analisar' para diagnóstico\n" +
                 "3. Veja resultado detalhado e gráficos\n" +
                 "4. Consulte sempre um médico especialista",
            font=("Arial", 9), bg='#f0f0f0', fg='#2c3e50',
            justify='left'
        )
        guide_text.pack()
        
        # Análise
        analysis_frame = tk.LabelFrame(parent, text="🔬 Análise de IA", 
                                      font=("Arial", 12, "bold"), bg='#f0f0f0', padx=15, pady=15)
        analysis_frame.pack(fill='x', pady=(0, 15))
        
        analyze_btn = tk.Button(
            analysis_frame, text="🧠 ANALISAR IMAGEM", command=self.analyze_image,
            bg='#e74c3c', fg='white', font=("Arial", 13, "bold"),
            relief='flat', padx=25, pady=15
        )
        analyze_btn.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(analysis_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=5)
        
        # Resultado resumido
        summary_frame = tk.LabelFrame(parent, text="⚡ Resultado Rápido", 
                                     font=("Arial", 11, "bold"), bg='#f0f0f0', padx=15, pady=10)
        summary_frame.pack(fill='x', pady=(0, 15))
        
        self.quick_result = tk.Label(
            summary_frame, text="Aguardando análise...",
            font=("Arial", 12, "bold"), bg='#f0f0f0', fg='#7f8c8d'
        )
        self.quick_result.pack(pady=10)
        
        # Resultado detalhado
        result_frame = tk.LabelFrame(parent, text="📋 Relatório Completo", 
                                    font=("Arial", 12, "bold"), bg='#f0f0f0', padx=10, pady=10)
        result_frame.pack(fill='both', expand=True)
        
        # Área de resultado com scrollbar
        result_text_frame = tk.Frame(result_frame, bg='#f0f0f0')
        result_text_frame.pack(fill='both', expand=True)
        
        self.result_text = tk.Text(
            result_text_frame, wrap='word', font=("Arial", 9),
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
            parent, text="🖼️ Visualização e Análise Detalhada", 
            font=("Arial", 16, "bold"), bg='white', pady=15
        )
        viz_title.pack()
        
        # Notebook para abas
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Aba 1 - Imagem
        self.image_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.image_tab, text="📷 Imagem")
        
        self.image_label = tk.Label(
            self.image_tab, 
            text="📷\n\nSelecione uma imagem de\nressonância magnética cerebral\npara começar a análise",
            font=("Arial", 14), bg='white', fg='#bdc3c7'
        )
        self.image_label.pack(expand=True)
        
        # Aba 2 - Gráficos
        self.charts_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.charts_tab, text="📊 Gráficos")
        
        self.charts_frame = tk.Frame(self.charts_tab, bg='white')
        self.charts_frame.pack(fill='both', expand=True)
    
    def load_corrected_model(self):
        """Carrega o modelo corrigido"""
        corrected_model = "models/brain_cancer_corrected.h5"
        
        if os.path.exists(corrected_model):
            try:
                self.model = load_model(corrected_model)
                self.model_status.config(
                    text="✅ Modelo Corrigido Carregado (83.96% acurácia)", 
                    fg='#27ae60'
                )
                print(f"✅ Modelo corrigido carregado: {corrected_model}")
            except Exception as e:
                self.model_status.config(text="❌ Erro ao carregar modelo", fg='#e74c3c')
                print(f"❌ Erro: {e}")
        else:
            self.model_status.config(text="❌ Modelo corrigido não encontrado", fg='#e74c3c')
    
    def select_image(self):
        """Seleciona imagem para análise"""
        file_path = filedialog.askopenfilename(
            title="Selecionar Imagem de Ressonância Magnética",
            filetypes=[
                ("Imagens", "*.jpg *.jpeg *.png *.bmp *.tiff"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
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
            
            # Resetar resultado anterior
            self.quick_result.config(text="Aguardando análise...", fg='#7f8c8d')
            self.result_text.delete(1.0, tk.END)
    
    def display_image(self, image_path):
        """Exibe a imagem selecionada"""
        try:
            # Carregar e redimensionar imagem para display
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Redimensionar mantendo proporção
            height, width = img.shape[:2]
            max_size = 500
            
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
            messagebox.showerror("Erro", "Modelo não foi carregado corretamente")
            return
        
        if self.current_image is None:
            messagebox.showerror("Erro", "Selecione uma imagem primeiro")
            return
        
        try:
            # Mostrar progress bar
            self.progress.start()
            self.root.update()
            
            # Pré-processar imagem
            processed_img = self.preprocess_image(self.current_image)
            
            # Fazer predição
            prediction = self.model.predict(processed_img, verbose=0)
            
            # Interpretar resultado
            probability = float(prediction[0][0])
            is_tumor = probability > 0.5
            confidence = probability if is_tumor else 1 - probability
            
            # Parar progress bar
            self.progress.stop()
            
            # Exibir resultado resumido
            self.display_quick_result(is_tumor, confidence, probability)
            
            # Exibir resultado detalhado
            self.display_detailed_result(is_tumor, confidence, probability)
            
            # Exibir gráficos
            self.display_analysis_charts(confidence, is_tumor, probability)
            
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Erro", f"Erro durante análise:\n{str(e)}")
    
    def display_quick_result(self, is_tumor, confidence, probability):
        """Exibe resultado rápido"""
        if is_tumor:
            result_text = f"🔴 TUMOR DETECTADO\nConfiança: {confidence:.1%}"
            color = '#e74c3c'
        else:
            result_text = f"✅ TECIDO NORMAL\nConfiança: {confidence:.1%}"
            color = '#27ae60'
        
        self.quick_result.config(text=result_text, fg=color)
    
    def display_detailed_result(self, is_tumor, confidence, probability):
        """Exibe resultado detalhado do diagnóstico"""
        
        self.result_text.delete(1.0, tk.END)
        
        # Cabeçalho do resultado
        result_header = "🧠 RELATÓRIO DE ANÁLISE CEREBRAL\n"
        result_header += "=" * 55 + "\n\n"
        
        # Informações da análise
        analysis_info = f"📄 Arquivo: {os.path.basename(self.current_image_path)}\n"
        analysis_info += f"🤖 Modelo: Diagnóstico de Câncer Cerebral v2.0\n"
        analysis_info += f"📊 Acurácia do modelo: 83.96%\n"
        analysis_info += f"🕐 Data/Hora: {self.get_current_time()}\n\n"
        
        # Resultado principal
        if is_tumor:
            diagnosis = "🔴 POSSÍVEL TUMOR CEREBRAL DETECTADO\n\n"
            diagnosis += f"📈 Probabilidade de tumor: {probability:.1%}\n"
            diagnosis += f"🎯 Nível de confiança: {confidence:.1%}\n\n"
            
            diagnosis += "🧠 TIPOS POSSÍVEIS DE TUMOR:\n"
            diagnosis += "• Glioma (tumor das células gliais)\n"
            diagnosis += "• Meningioma (tumor das meninges)\n"
            diagnosis += "• Tumor pituitário (hipófise)\n\n"
            
            diagnosis += "⚠️ AÇÃO REQUERIDA:\n"
            diagnosis += "Este resultado indica presença de possível\n"
            diagnosis += "tumor cerebral. É URGENTE buscar avaliação\n"
            diagnosis += "médica especializada (neurologista/neurocirurgião).\n\n"
        else:
            diagnosis = "✅ TECIDO CEREBRAL NORMAL\n\n"
            diagnosis += f"📈 Probabilidade de normalidade: {1-probability:.1%}\n"
            diagnosis += f"🎯 Nível de confiança: {confidence:.1%}\n\n"
            diagnosis += "✅ RESULTADO FAVORÁVEL:\n"
            diagnosis += "A análise não identificou sinais evidentes\n"
            diagnosis += "de tumor cerebral na imagem de RM analisada.\n"
            diagnosis += "O tecido apresenta características normais.\n\n"
        
        # Interpretação técnica
        technical = "🔬 INTERPRETAÇÃO TÉCNICA:\n"
        technical += "-" * 35 + "\n"
        if is_tumor:
            if confidence >= 0.9:
                technical += "• Confiança MUITO ALTA na detecção\n"
            elif confidence >= 0.7:
                technical += "• Confiança ALTA na detecção\n"
            else:
                technical += "• Confiança MODERADA na detecção\n"
            
            technical += "• Características anômalas identificadas\n"
            technical += "• Padrões compatíveis com tecido tumoral\n"
        else:
            technical += "• Padrões de tecido cerebral normal\n"
            technical += "• Ausência de características tumorais\n"
            technical += "• Estruturas cerebrais preservadas\n"
        
        technical += f"• Processamento: Imagem {self.img_size[0]}x{self.img_size[1]} pixels\n\n"
        
        # Aviso médico
        medical_warning = "⚕️ IMPORTANTE - AVISO MÉDICO:\n"
        medical_warning += "-" * 40 + "\n"
        medical_warning += "• Este sistema é uma FERRAMENTA DE APOIO\n"
        medical_warning += "• NÃO substitui diagnóstico médico profissional\n"
        medical_warning += "• Baseado em análise de imagem por IA\n"
        medical_warning += "• Sempre consulte médico especialista\n"
        medical_warning += "• Exames complementares podem ser necessários\n\n"
        
        # Recomendações específicas
        recommendations = "📋 RECOMENDAÇÕES ESPECÍFICAS:\n"
        recommendations += "-" * 35 + "\n"
        if is_tumor:
            recommendations += "🚨 URGENTE:\n"
            recommendations += "• Consulte neurologista/neurocirurgião\n"
            recommendations += "• Leve esta análise ao médico\n"
            recommendations += "• Realize RM com contraste se indicado\n"
            recommendations += "• Não adie a consulta médica\n"
            recommendations += "• Mantenha a calma - muitos tumores são tratáveis\n"
        else:
            recommendations += "✅ ACOMPANHAMENTO:\n"
            recommendations += "• Mantenha check-ups médicos regulares\n"
            recommendations += "• Continue exames preventivos\n"
            recommendations += "• Procure médico se houver sintomas\n"
            recommendations += "• Este resultado não exclui outras condições\n"
            recommendations += "• Mantenha estilo de vida saudável\n"
        
        # Combinar todo o texto
        full_result = result_header + analysis_info + diagnosis + technical + medical_warning + recommendations
        
        self.result_text.insert(tk.END, full_result)
        
        # Configurar cores baseadas no resultado
        if is_tumor:
            self.result_text.tag_add("tumor", "3.0", "3.end")
            self.result_text.tag_config("tumor", foreground="#e74c3c", font=("Arial", 11, "bold"))
        else:
            self.result_text.tag_add("normal", "3.0", "3.end") 
            self.result_text.tag_config("normal", foreground="#27ae60", font=("Arial", 11, "bold"))
    
    def display_analysis_charts(self, confidence, is_tumor, probability):
        """Exibe gráficos de análise"""
        
        # Limpar frame anterior
        for widget in self.charts_frame.winfo_children():
            widget.destroy()
        
        # Criar figura matplotlib
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.patch.set_facecolor('white')
        fig.suptitle('Análise Detalhada do Diagnóstico por IA', fontsize=16, fontweight='bold')
        
        # Gráfico 1 - Classificação
        categories = ['Normal', 'Tumor']
        values = [1-probability, probability]
        colors = ['#27ae60', '#e74c3c']
        
        bars = ax1.bar(categories, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
        ax1.set_ylim(0, 1)
        ax1.set_ylabel('Probabilidade', fontweight='bold')
        ax1.set_title('Classificação Principal', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Adicionar valores nas barras
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{value:.1%}', ha='center', va='bottom', fontweight='bold')
        
        # Gráfico 2 - Nível de confiança
        sizes = [confidence, 1-confidence]
        labels = ['Confiança', 'Incerteza']
        colors_pie = ['#3498db', '#ecf0f1']
        
        wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=colors_pie, 
                                          autopct='%1.1f%%', startangle=90)
        ax2.set_title(f'Nível de Confiança: {confidence:.1%}', fontweight='bold')
        
        # Gráfico 3 - Distribuição de probabilidade
        x = ['Normal', 'Tumor']
        y = [1-probability, probability]
        
        ax3.plot(x, y, marker='o', linewidth=3, markersize=8, color='#8e44ad')
        ax3.fill_between(x, y, alpha=0.3, color='#8e44ad')
        ax3.set_ylim(0, 1)
        ax3.set_ylabel('Probabilidade', fontweight='bold')
        ax3.set_title('Distribuição de Probabilidade', fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # Gráfico 4 - Escala de risco
        risk_categories = ['Muito Baixo', 'Baixo', 'Médio', 'Alto', 'Muito Alto']
        risk_values = [0.1, 0.3, 0.5, 0.7, 0.9]
        
        # Determinar posição atual na escala
        current_risk = probability
        
        bars_risk = ax4.barh(risk_categories, [0.2]*5, color='lightgray', alpha=0.5)
        
        # Colorir barra correspondente ao risco atual
        if current_risk <= 0.2:
            bars_risk[0].set_color('#27ae60')
        elif current_risk <= 0.4:
            bars_risk[1].set_color('#f39c12')
        elif current_risk <= 0.6:
            bars_risk[2].set_color('#e67e22')
        elif current_risk <= 0.8:
            bars_risk[3].set_color('#e74c3c')
        else:
            bars_risk[4].set_color('#c0392b')
        
        # Adicionar marcador da posição atual
        risk_position = len(risk_categories) - 1 - (current_risk * len(risk_categories))
        ax4.scatter([0.15], [risk_position], color='black', s=100, marker='|', linewidth=3)
        
        ax4.set_xlim(0, 0.2)
        ax4.set_title('Escala de Risco', fontweight='bold')
        ax4.set_xlabel('Indicador de Risco', fontweight='bold')
        
        plt.tight_layout()
        
        # Incorporar no tkinter
        canvas = FigureCanvasTkAgg(fig, self.charts_frame)
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
    print("🧠 Iniciando Interface Visual v2.0 - Diagnóstico de Câncer Cerebral...")
    
    try:
        app = VisualCancerDiagnosisV2()
        app.run()
    except Exception as e:
        print(f"❌ Erro ao inicializar interface: {e}")

if __name__ == "__main__":
    main()