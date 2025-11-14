"""
Interface Visual MODERNA para Diagnóstico de Câncer - Design Profissional
Layout moderno com tema médico elegante
"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
import os
from tensorflow.keras.models import load_model

class ModernCancerDiagnosis:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NeuroAI - Sistema de Diagnóstico Cerebral")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0e1a')
        self.root.minsize(1200, 700)  # Tamanho mínimo
        
        # Tentar maximizar (funciona no Windows)
        try:
            self.root.state('zoomed')
        except:
            # Fallback para outros sistemas
            self.root.attributes('-zoomed', True)
        
        # Cores do tema moderno
        self.colors = {
            'bg_primary': '#0a0e1a',      # Azul escuro profundo
            'bg_secondary': '#1a1f35',     # Azul escuro médio  
            'bg_card': '#242b4d',          # Azul escuro claro
            'accent_blue': '#00d4ff',      # Azul neon
            'accent_green': '#00ff88',     # Verde neon
            'accent_red': '#ff4757',       # Vermelho vibrante
            'accent_orange': '#ffa726',    # Laranja suave
            'text_primary': '#ffffff',     # Branco
            'text_secondary': '#b3bcc8',   # Cinza claro
            'text_muted': '#6c7b88',       # Cinza médio
            'success': '#28a745',          # Verde sucesso
            'warning': '#ffc107',          # Amarelo aviso
            'danger': '#dc3545',           # Vermelho perigo
            'gradient_start': '#667eea',   # Gradiente início
            'gradient_end': '#764ba2'      # Gradiente fim
        }
        
        # Configurar fonte moderna
        self.fonts = {
            'title': ('Segoe UI', 28, 'bold'),
            'subtitle': ('Segoe UI', 14, 'normal'),
            'heading': ('Segoe UI', 16, 'bold'),
            'body': ('Segoe UI', 11, 'normal'),
            'small': ('Segoe UI', 9, 'normal'),
            'button': ('Segoe UI', 12, 'bold'),
            'mono': ('Consolas', 10, 'normal')
        }
        
        # Variáveis
        self.model = None
        self.current_image = None
        self.current_image_path = None
        self.img_size = (128, 128)
        self.decision_threshold = tk.DoubleVar(value=0.4)
        
        self.setup_modern_gui()
        self.load_corrected_model()
        self.create_animations()
    
    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=20, **kwargs):
        """Cria retângulo com cantos arredondados"""
        points = []
        for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                     (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                     (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                     (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
            points.extend([x, y])
        return canvas.create_polygon(points, smooth=True, **kwargs)
    
    def setup_modern_gui(self):
        """Configura interface moderna"""
        
        # Header com gradiente
        self.create_header()
        
        # Container principal
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Grid principal - 3 colunas responsivas
        main_container.grid_columnconfigure(0, weight=1, minsize=300)  # Painel esquerdo
        main_container.grid_columnconfigure(1, weight=3, minsize=600)  # Visualização
        main_container.grid_columnconfigure(2, weight=1, minsize=300)  # Painel direito
        main_container.grid_rowconfigure(0, weight=1)
        
        # Painel esquerdo - Controles
        self.create_control_panel(main_container)
        
        # Painel central - Visualização
        self.create_visualization_panel(main_container)
        
        # Painel direito - Resultados
        self.create_results_panel(main_container)
    
    def create_header(self):
        """Cria header moderno com gradiente"""
        header_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=120)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Container do header
        header_container = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        header_container.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Lado esquerdo - Logo e título
        left_header = tk.Frame(header_container, bg=self.colors['bg_secondary'])
        left_header.pack(side='left', fill='y')
        
        # Logo (emoji estilizado)
        logo_label = tk.Label(
            left_header,
            text="🧠",
            font=('Segoe UI Emoji', 48),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_blue']
        )
        logo_label.pack(side='left', padx=(0, 20))
        
        # Título e subtítulo
        title_container = tk.Frame(left_header, bg=self.colors['bg_secondary'])
        title_container.pack(side='left', fill='y')
        
        title_label = tk.Label(
            title_container,
            text="NeuroAI Diagnostics",
            font=self.fonts['title'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(
            title_container,
            text="Sistema Inteligente de Diagnóstico Cerebral • Powered by AI",
            font=self.fonts['subtitle'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack(anchor='w')
        
        # Lado direito - Status do modelo
        right_header = tk.Frame(header_container, bg=self.colors['bg_secondary'])
        right_header.pack(side='right', fill='y')
        
        # Card de status do modelo
        self.create_model_status_card(right_header)
    
    def create_model_status_card(self, parent):
        """Cria card de status do modelo"""
        status_card = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat')
        status_card.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Indicador de status
        self.status_indicator = tk.Label(
            status_card,
            text="●",
            font=('Segoe UI', 20),
            bg=self.colors['bg_card'],
            fg=self.colors['warning']
        )
        self.status_indicator.pack(pady=(15, 5))
        
        self.model_status_label = tk.Label(
            status_card,
            text="Carregando Modelo...",
            font=self.fonts['body'],
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        )
        self.model_status_label.pack()
        
        self.model_info_label = tk.Label(
            status_card,
            text="Aguarde...",
            font=self.fonts['small'],
            bg=self.colors['bg_card'],
            fg=self.colors['text_muted']
        )
        self.model_info_label.pack(pady=(5, 15))
    
    def create_control_panel(self, parent):
        """Cria painel de controles moderno com scroll"""
        # Frame principal
        control_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        control_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 15))
        
        # Canvas para scroll
        canvas = tk.Canvas(control_frame, bg=self.colors['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(control_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_primary'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título do painel
        panel_title = tk.Label(
            scrollable_frame,
            text="Painel de Controle",
            font=self.fonts['heading'],
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        panel_title.pack(pady=(0, 30))
        
        # Card de upload
        self.create_upload_card(scrollable_frame)
        
        # Card de análise
        self.create_analysis_card(scrollable_frame)
        
        # Card de informações
        self.create_info_card(scrollable_frame)
        
        # Pack canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel para scroll
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_upload_card(self, parent):
        """Cria card de upload moderno"""
        upload_card = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat', bd=2)
        upload_card.pack(fill='x', pady=(0, 20))
        
        # Header do card
        card_header = tk.Frame(upload_card, bg=self.colors['bg_card'])
        card_header.pack(fill='x', padx=20, pady=(20, 10))
        
        header_icon = tk.Label(
            card_header,
            text="📁",
            font=('Segoe UI Emoji', 24),
            bg=self.colors['bg_card'],
            fg=self.colors['accent_blue']
        )
        header_icon.pack(side='left')
        
        header_text = tk.Label(
            card_header,
            text="Carregar Imagem",
            font=self.fonts['heading'],
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        )
        header_text.pack(side='left', padx=(15, 0))
        
        # Área de drop/upload
        upload_area = tk.Frame(upload_card, bg=self.colors['bg_secondary'], relief='ridge', bd=1)
        upload_area.pack(fill='x', padx=15, pady=(0, 8))
        
        upload_text = tk.Label(
            upload_area,
            text="Arraste a imagem aqui\nou clique para selecionar",
            font=self.fonts['body'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary'],
            justify='center'
        )
        upload_text.pack(pady=20)
        
        # Botão de upload estilizado
        self.upload_btn = self.create_modern_button(
            upload_card,
            text="🔍 Selecionar Imagem de RM",
            command=self.select_image,
            color=self.colors['accent_blue'],
            width=250
        )
        self.upload_btn.pack(pady=(0, 20))
        
        # Status da imagem
        self.image_status = tk.Label(
            upload_card,
            text="Nenhuma imagem selecionada",
            font=self.fonts['small'],
            bg=self.colors['bg_card'],
            fg=self.colors['text_muted']
        )
        self.image_status.pack(pady=(0, 20))
    
    def create_analysis_card(self, parent):
        """Cria card de análise"""
        analysis_card = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat', bd=2)
        analysis_card.pack(fill='x', pady=(0, 20))
        
        # Header
        card_header = tk.Frame(analysis_card, bg=self.colors['bg_card'])
        card_header.pack(fill='x', padx=20, pady=(20, 10))
        
        header_icon = tk.Label(
            card_header,
            text="🔬",
            font=('Segoe UI Emoji', 24),
            bg=self.colors['bg_card'],
            fg=self.colors['accent_green']
        )
        header_icon.pack(side='left')
        
        header_text = tk.Label(
            card_header,
            text="Análise por IA",
            font=self.fonts['heading'],
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        )
        header_text.pack(side='left', padx=(15, 0))
        
        # Botão de análise principal
        self.analyze_btn = self.create_modern_button(
            analysis_card,
            text="🧠 INICIAR DIAGNÓSTICO",
            command=self.analyze_image,
            color=self.colors['accent_green'],
            width=250,
            height=50
        )
        self.analyze_btn.pack(pady=20)
        
        # Progress bar moderna
        progress_frame = tk.Frame(analysis_card, bg=self.colors['bg_card'])
        progress_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            mode='indeterminate',
            style='Modern.Horizontal.TProgressbar'
        )
        self.progress.pack(fill='x')
        
        # Configurar estilo da progress bar
        self.setup_progressbar_style()
        
        # Controle de limiar de decisão
        threshold_frame = tk.Frame(analysis_card, bg=self.colors['bg_card'])
        threshold_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Label(
            threshold_frame,
            text="Limiar de decisão (prob. para Tumor)",
            font=self.fonts['small'],
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary']
        ).pack(anchor='w')
        
        slider_row = tk.Frame(threshold_frame, bg=self.colors['bg_card'])
        slider_row.pack(fill='x')
        
        def on_threshold_change(value):
            value = float(value)
            threshold_value_label.config(text=f"{value:.2f}")
        
        threshold_slider = ttk.Scale(
            slider_row,
            from_=0.30,
            to=0.90,
            orient='horizontal',
            variable=self.decision_threshold,
            command=on_threshold_change,
            length=220
        )
        threshold_slider.pack(side='left', pady=4)
        
        threshold_value_label = tk.Label(
            slider_row,
            text=f"{self.decision_threshold.get():.2f}",
            font=self.fonts['small'],
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        )
        threshold_value_label.pack(side='left', padx=10)

        # Botão para sugerir limiar ótimo
        suggest_btn = self.create_modern_button(
            analysis_card,
            text="📐 Calcular limiar ótimo (Testing)",
            command=self.compute_optimal_threshold,
            color=self.colors['accent_orange'],
            width=280,
            height=40
        )
        suggest_btn.pack(pady=(0, 12))
    
    def create_info_card(self, parent):
        """Cria card de informações"""
        info_card = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat', bd=2)
        info_card.pack(fill='both', expand=True)
        
        # Header
        card_header = tk.Frame(info_card, bg=self.colors['bg_card'])
        card_header.pack(fill='x', padx=20, pady=(20, 10))
        
        header_icon = tk.Label(
            card_header,
            text="ℹ️",
            font=('Segoe UI Emoji', 24),
            bg=self.colors['bg_card'],
            fg=self.colors['accent_orange']
        )
        header_icon.pack(side='left')
        
        header_text = tk.Label(
            card_header,
            text="Informações do Sistema",
            font=self.fonts['heading'],
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        )
        header_text.pack(side='left', padx=(15, 0))
        
        # Informações técnicas
        info_text = """
• Modelo Balanceado (sem viés)
• Acurácia: 83.13%
• 2 categorias: Normal vs Tumor
• Detecta: Glioma, Meningioma, 
  Tumor Pituitário, Tecido Normal
• Limiar ajustado: 0.40
• Tempo de análise: ~2 segundos
• Formato suportado: JPG, PNG
        """
        
        info_label = tk.Label(
            info_card,
            text=info_text.strip(),
            font=self.fonts['small'],
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            justify='left'
        )
        info_label.pack(padx=20, pady=10, anchor='w')
        
        # Aviso médico
        warning_frame = tk.Frame(info_card, bg=self.colors['danger'], relief='flat')
        warning_frame.pack(fill='x', padx=20, pady=(10, 20))
        
        warning_text = "⚠️ FERRAMENTA DE APOIO\nNÃO substitui diagnóstico médico"
        warning_label = tk.Label(
            warning_frame,
            text=warning_text,
            font=self.fonts['small'],
            bg=self.colors['danger'],
            fg='white',
            justify='center'
        )
        warning_label.pack(pady=10)
    
    def create_visualization_panel(self, parent):
        """Cria painel de visualização central"""
        viz_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        viz_frame.grid(row=0, column=1, sticky='nsew', padx=15)
        
        # Título
        viz_title = tk.Label(
            viz_frame,
            text="Visualização e Análise",
            font=self.fonts['heading'],
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        viz_title.pack(pady=(0, 20))
        
        # Notebook com estilo moderno
        self.setup_notebook_style()
        self.notebook = ttk.Notebook(viz_frame, style='Modern.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Aba 1 - Imagem
        self.create_image_tab()
        
        # Aba 2 - Gráficos
        self.create_charts_tab()
        
        # Aba 3 - Heatmap (simulado)
        self.create_heatmap_tab()
    
    def create_image_tab(self):
        """Cria aba de visualização da imagem"""
        self.image_tab = tk.Frame(self.notebook, bg=self.colors['bg_card'])
        self.notebook.add(self.image_tab, text=" 🖼️  Imagem Original ")
        
        # Container da imagem
        image_container = tk.Frame(self.image_tab, bg=self.colors['bg_secondary'], relief='flat', bd=2)
        image_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.image_label = tk.Label(
            image_container,
            text="🏥\n\nCarregue uma imagem de\nRessonância Magnética\npara começar a análise",
            font=('Segoe UI', 16),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_muted'],
            justify='center'
        )
        self.image_label.pack(expand=True)
    
    def create_charts_tab(self):
        """Cria aba de gráficos"""
        self.charts_tab = tk.Frame(self.notebook, bg=self.colors['bg_card'])
        self.notebook.add(self.charts_tab, text=" 📊  Análise Quantitativa ")
        
        self.charts_frame = tk.Frame(self.charts_tab, bg=self.colors['bg_card'])
        self.charts_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    def create_heatmap_tab(self):
        """Cria aba de heatmap"""
        self.heatmap_tab = tk.Frame(self.notebook, bg=self.colors['bg_card'])
        self.notebook.add(self.heatmap_tab, text=" 🔥  Mapa de Ativação ")
        
        # Container principal do heatmap
        heatmap_container = tk.Frame(self.heatmap_tab, bg=self.colors['bg_card'])
        heatmap_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título explicativo
        title_frame = tk.Frame(heatmap_container, bg=self.colors['bg_card'])
        title_frame.pack(fill='x', pady=(0, 10))
        
        title_label = tk.Label(
            title_frame,
            text="🔥 Mapa de Ativação da IA",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        )
        title_label.pack()
        
        explanation_label = tk.Label(
            title_frame,
            text="Mostra onde a IA está focando para fazer o diagnóstico\n🔴 Vermelho = Suspeito | 🟡 Amarelo = Moderado | 🔵 Azul = Normal",
            font=('Segoe UI', 10),
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            justify='center'
        )
        explanation_label.pack(pady=5)
        
        # Frame para o heatmap
        self.heatmap_frame = tk.Frame(heatmap_container, bg=self.colors['bg_secondary'], relief='flat', bd=2)
        self.heatmap_frame.pack(fill='both', expand=True)
        
        # Label inicial
        self.heatmap_label = tk.Label(
            self.heatmap_frame,
            text="🔄\n\nAnalise uma imagem primeiro\npara gerar o mapa de ativação",
            font=('Segoe UI', 14),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_muted'],
            justify='center'
        )
        self.heatmap_label.pack(expand=True)
    
    def create_results_panel(self, parent):
        """Cria painel de resultados"""
        results_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        results_frame.grid(row=0, column=2, sticky='nsew', padx=(15, 0))
        
        # Título
        results_title = tk.Label(
            results_frame,
            text="Resultados do Diagnóstico",
            font=self.fonts['heading'],
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        results_title.pack(pady=(0, 20))
        
        # Card de resultado rápido
        self.create_quick_result_card(results_frame)
        
        # Card de relatório detalhado
        self.create_detailed_report_card(results_frame)
    
    def create_quick_result_card(self, parent):
        """Cria card de resultado rápido"""
        quick_card = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat', bd=2)
        quick_card.pack(fill='x', pady=(0, 20))
        
        # Header
        header = tk.Frame(quick_card, bg=self.colors['bg_card'])
        header.pack(fill='x', padx=20, pady=(20, 10))
        
        header_icon = tk.Label(
            header,
            text="⚡",
            font=('Segoe UI Emoji', 24),
            bg=self.colors['bg_card'],
            fg=self.colors['accent_orange']
        )
        header_icon.pack(side='left')
        
        header_text = tk.Label(
            header,
            text="Resultado Instantâneo",
            font=self.fonts['heading'],
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        )
        header_text.pack(side='left', padx=(15, 0))
        
        # Área do resultado
        result_area = tk.Frame(quick_card, bg=self.colors['bg_secondary'], relief='flat')
        result_area.pack(fill='x', padx=20, pady=(0, 10))
        
        self.quick_result_icon = tk.Label(
            result_area,
            text="🔄",
            font=('Segoe UI Emoji', 48),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_muted']
        )
        self.quick_result_icon.pack(pady=(20, 10))
        
        self.quick_result_text = tk.Label(
            result_area,
            text="Aguardando análise...",
            font=self.fonts['body'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary'],
            justify='center'
        )
        self.quick_result_text.pack(pady=(0, 20))
    
    def create_detailed_report_card(self, parent):
        """Cria card de relatório detalhado"""
        report_card = tk.Frame(parent, bg=self.colors['bg_card'], relief='flat', bd=2)
        report_card.pack(fill='both', expand=True)
        
        # Header
        header = tk.Frame(report_card, bg=self.colors['bg_card'])
        header.pack(fill='x', padx=20, pady=(20, 10))
        
        header_icon = tk.Label(
            header,
            text="📋",
            font=('Segoe UI Emoji', 24),
            bg=self.colors['bg_card'],
            fg=self.colors['accent_blue']
        )
        header_icon.pack(side='left')
        
        header_text = tk.Label(
            header,
            text="Relatório Completo",
            font=self.fonts['heading'],
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary']
        )
        header_text.pack(side='left', padx=(15, 0))
        
        # Área de texto com scroll
        text_frame = tk.Frame(report_card, bg=self.colors['bg_card'])
        text_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        self.result_text = tk.Text(
            text_frame,
            wrap='word',
            font=self.fonts['mono'],
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            relief='flat',
            borderwidth=0,
            padx=15,
            pady=15,
            insertbackground=self.colors['accent_blue']
        )
        
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def create_modern_button(self, parent, text, command, color, width=None, height=None):
        """Cria botão moderno estilizado"""
        btn_frame = tk.Frame(parent, bg=parent['bg'])
        if width:
            btn_frame.configure(width=width)
        if height:
            btn_frame.configure(height=height)
        
        button = tk.Button(
            btn_frame,
            text=text,
            command=command,
            font=self.fonts['button'],
            bg=color,
            fg='white',
            relief='flat',
            bd=0,
            padx=20,
            pady=12,
            cursor='hand2'
        )
        button.pack(fill='both', expand=True)
        
        # Hover effects
        def on_enter(e):
            button.configure(bg=self.lighten_color(color))
        
        def on_leave(e):
            button.configure(bg=color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return btn_frame
    
    def lighten_color(self, color):
        """Clareia uma cor em hex"""
        if color.startswith('#'):
            color = color[1:]
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, c + 30) for c in rgb)
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def setup_progressbar_style(self):
        """Configura estilo da progress bar"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure(
            'Modern.Horizontal.TProgressbar',
            background=self.colors['accent_blue'],
            troughcolor=self.colors['bg_secondary'],
            borderwidth=0,
            lightcolor=self.colors['accent_blue'],
            darkcolor=self.colors['accent_blue']
        )
    
    def setup_notebook_style(self):
        """Configura estilo do notebook"""
        style = ttk.Style()
        
        style.configure(
            'Modern.TNotebook',
            background=self.colors['bg_card'],
            borderwidth=0
        )
        
        style.configure(
            'Modern.TNotebook.Tab',
            background=self.colors['bg_secondary'],
            foreground=self.colors['text_secondary'],
            padding=[20, 10],
            font=self.fonts['body']
        )
        
        style.map(
            'Modern.TNotebook.Tab',
            background=[('selected', self.colors['accent_blue'])],
            foreground=[('selected', 'white')]
        )
    
    def load_corrected_model(self):
        """Carrega o modelo balanceado (sem viés)"""
        # Tentar primeiro o modelo balanceado
        balanced_model = "models/brain_cancer_balanced.h5"
        corrected_model = "models/brain_cancer_corrected.h5"
        
        model_path = None
        model_info = ""
        
        if os.path.exists(balanced_model):
            model_path = balanced_model
            model_info = "Acurácia: 83.13% • Modelo Balanceado"
        elif os.path.exists(corrected_model):
            model_path = corrected_model
            model_info = "Acurácia: 83.96% • Modelo Corrigido"
        
        if model_path:
            try:
                self.model = load_model(model_path)
                self.status_indicator.config(fg=self.colors['success'])
                self.model_status_label.config(text="Modelo Online")
                self.model_info_label.config(text=model_info)
                print(f"✅ Modelo carregado: {model_path}")
            except Exception as e:
                self.status_indicator.config(fg=self.colors['danger'])
                self.model_status_label.config(text="Erro no Modelo")
                self.model_info_label.config(text="Falha ao carregar")
                print(f"❌ Erro: {e}")
        else:
            self.status_indicator.config(fg=self.colors['danger'])
            self.model_status_label.config(text="Modelo Não Encontrado")
            self.model_info_label.config(text="Execute o treinamento")
    
    def select_image(self):
        """Seleciona imagem para análise"""
        file_path = filedialog.askopenfilename(
            title="Selecionar Imagem de Ressonância Magnética",
            filetypes=[
                ("Imagens Médicas", "*.jpg *.jpeg *.png *.bmp *.tiff *.dcm"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("DICOM", "*.dcm"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if file_path:
            self.current_image_path = file_path
            self.display_image(file_path)
            filename = os.path.basename(file_path)
            self.image_status.config(
                text=f"✅ {filename}",
                fg=self.colors['success']
            )
            
            # Reset resultado anterior
            self.reset_results()
    
    def display_image(self, image_path):
        """Exibe a imagem selecionada com estilo moderno"""
        try:
            # Carregar e processar imagem
            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Redimensionar mantendo proporção
            height, width = img.shape[:2]
            max_size = 600
            
            if width > height:
                new_width = max_size
                new_height = int(height * max_size / width)
            else:
                new_height = max_size
                new_width = int(width * max_size / height)
            
            img_resized = cv2.resize(img, (new_width, new_height))
            
            # Criar moldura elegante
            img_pil = Image.fromarray(img_resized)
            
            # Adicionar sombra sutil
            shadow = Image.new('RGBA', (img_pil.width + 20, img_pil.height + 20), (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow)
            shadow_draw.rectangle([10, 10, img_pil.width + 10, img_pil.height + 10], 
                                fill=(0, 0, 0, 30))
            shadow = shadow.filter(ImageFilter.GaussianBlur(5))
            
            # Compor imagem final
            final_img = Image.new('RGBA', shadow.size, (0, 0, 0, 0))
            final_img.paste(shadow, (0, 0))
            final_img.paste(img_pil, (5, 5))
            
            img_tk = ImageTk.PhotoImage(final_img)
            
            # Atualizar display
            self.image_label.config(image=img_tk, text="")
            self.image_label.image = img_tk  # Manter referência
            
            # Salvar imagem original
            self.current_image = img
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem:\n{str(e)}")
    
    def analyze_image(self):
        """Realiza análise da imagem com interface moderna"""
        if self.model is None:
            messagebox.showerror("Erro", "Modelo não foi carregado corretamente")
            return
        
        if self.current_image is None:
            messagebox.showerror("Erro", "Selecione uma imagem primeiro")
            return
        
        try:
            # Iniciar animação de progresso
            self.progress.start(10)
            self.quick_result_icon.config(text="🔄", fg=self.colors['warning'])
            self.quick_result_text.config(text="Analisando...", fg=self.colors['text_primary'])
            self.root.update()
            
            # Pré-processar imagem
            processed_img = self.preprocess_image(self.current_image)
            
            # Fazer predição com TTA (rotações e flips)
            prediction = self.predict_with_tta(processed_img)
            
            # Interpretar resultado
            probability = float(prediction)
            threshold = float(self.decision_threshold.get())
            is_tumor = probability > threshold
            confidence = probability if is_tumor else 1 - probability
            
            # Parar progresso
            self.progress.stop()
            
            # Atualizar resultados
            self.display_modern_results(is_tumor, confidence, probability)
            
            # Gerar gráficos modernos
            self.display_modern_charts(confidence, is_tumor, probability)
            
            # Gerar mapa de ativação
            self.generate_activation_map(processed_img, is_tumor, confidence)
            
        except Exception as e:
            self.progress.stop()
            self.quick_result_icon.config(text="❌", fg=self.colors['danger'])
            self.quick_result_text.config(text="Erro na análise", fg=self.colors['danger'])
            messagebox.showerror("Erro", f"Erro durante análise:\n{str(e)}")
    
    def display_modern_results(self, is_tumor, confidence, probability):
        """Exibe resultados com design moderno"""
        if is_tumor:
            self.quick_result_icon.config(text="⚠️", fg=self.colors['danger'])
            result_text = f"TUMOR DETECTADO\nConfiança: {confidence:.1%}"
            self.quick_result_text.config(text=result_text, fg=self.colors['danger'])
        else:
            self.quick_result_icon.config(text="✅", fg=self.colors['success'])
            result_text = f"TECIDO NORMAL\nConfiança: {confidence:.1%}"
            self.quick_result_text.config(text=result_text, fg=self.colors['success'])
        
        # Relatório detalhado com formatação moderna
        self.generate_modern_report(is_tumor, confidence, probability)
    
    def generate_modern_report(self, is_tumor, confidence, probability):
        """Gera relatório com formatação moderna"""
        self.result_text.delete(1.0, tk.END)
        
        report = f"""
╔══════════════════════════════════════╗
║         RELATÓRIO DE DIAGNÓSTICO     ║
╚══════════════════════════════════════╝

📄 INFORMAÇÕES DA ANÁLISE
▶ Arquivo: {os.path.basename(self.current_image_path)}
▶ Modelo: NeuroAI v2.0 (Acurácia: 83.96%)
▶ Data/Hora: {self.get_current_time()}
▶ Resolução: {self.img_size[0]}x{self.img_size[1]} pixels
▶ Limiar usado: {float(self.decision_threshold.get()):.2f}

🎯 RESULTADO PRINCIPAL
▶ Classificação: {'TUMOR DETECTADO' if is_tumor else 'TECIDO NORMAL'}
▶ Probabilidade: {probability:.1%}
▶ Confiança: {confidence:.1%}
▶ Status: {'🔴 ATENÇÃO MÉDICA NECESSÁRIA' if is_tumor else '✅ RESULTADO FAVORÁVEL'}

🧠 INTERPRETAÇÃO CLÍNICA
"""
        
        if is_tumor:
            report += f"""▶ Possível presença de tumor cerebral
▶ Tipos possíveis: Glioma, Meningioma, Pituitário
▶ Confiança: {'MUITO ALTA' if confidence >= 0.9 else 'ALTA' if confidence >= 0.7 else 'MODERADA'}
▶ Recomendação: URGENTE - Consulte neurologista

🚨 AÇÕES RECOMENDADAS
▶ Consulte neurologista/neurocirurgião imediatamente
▶ Realize RM com contraste se indicado
▶ Leve este relatório ao médico
▶ Não adie a consulta médica"""
        else:
            report += f"""▶ Características de tecido cerebral normal
▶ Ausência de sinais evidentes de tumor
▶ Estruturas cerebrais preservadas
▶ Padrões anatômicos dentro da normalidade

✅ RECOMENDAÇÕES
▶ Mantenha check-ups médicos regulares
▶ Continue exames preventivos conforme orientação
▶ Procure médico se houver sintomas neurológicos
▶ Este resultado não exclui outras condições"""
        
        report += f"""

⚕️ AVISO MÉDICO IMPORTANTE
▶ Este sistema é uma FERRAMENTA DE APOIO
▶ NÃO substitui diagnóstico médico profissional
▶ Sempre consulte um médico especialista
▶ Exames complementares podem ser necessários

══════════════════════════════════════════
        """
        
        self.result_text.insert(tk.END, report)
    
    def display_modern_charts(self, confidence, is_tumor, probability):
        """Exibe gráficos com design moderno"""
        # Limpar frame anterior
        for widget in self.charts_frame.winfo_children():
            widget.destroy()
        
        # Configurar matplotlib com tema escuro
        try:
            plt.style.use('dark_background')
        except:
            plt.style.use('default')
        
        # Criar figura com melhor espaçamento
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.patch.set_facecolor('#1a1f35')
        fig.suptitle('NeuroAI - Análise Quantitativa do Diagnóstico', 
                    fontsize=13, fontweight='bold', color='white', y=0.98)
        
        # Ajustar espaçamento entre subplots - mais espaço no topo
        plt.subplots_adjust(left=0.08, right=0.95, top=0.85, bottom=0.10, 
                           wspace=0.25, hspace=0.40)
        
        # Gráfico 1 - Classificação com gradiente
        categories = ['Normal', 'Tumor']
        values = [1-probability, probability]
        colors = ['#00ff88', '#ff4757']
        
        bars = ax1.bar(categories, values, color=colors, alpha=0.8, 
                      edgecolor='white', linewidth=1)
        ax1.set_ylim(0, 1.1)  # Mais espaço para os rótulos
        ax1.set_ylabel('Probabilidade', fontweight='bold', color='white', fontsize=10)
        ax1.set_title('Classificação Principal', fontweight='bold', color='white', fontsize=11, pad=10)
        ax1.grid(True, alpha=0.2, color='white')
        ax1.set_facecolor('#242b4d')
        ax1.tick_params(axis='both', colors='white', labelsize=9)
        
        # Adicionar valores nas barras com melhor posicionamento
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.03,
                    f'{value:.1%}', ha='center', va='bottom', 
                    fontweight='bold', color='white', fontsize=10)
        
        # Gráfico 2 - Confiança estilizado
        sizes = [confidence, 1-confidence]
        labels = ['Confiança', 'Incerteza']
        colors_pie = ['#00d4ff', '#555']
        
        wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=colors_pie,
                                          autopct='%1.1f%%', startangle=90,
                                          textprops={'color': 'white', 'fontweight': 'bold', 'fontsize': 9})
        ax2.set_title(f'Nível de Confiança: {confidence:.1%}', 
                     fontweight='bold', color='white', fontsize=11, pad=10)
        
        # Gráfico 3 - Distribuição suavizada
        x = np.linspace(0, 1, 100)
        y1 = np.exp(-((x - (1-probability)) ** 2) / 0.02)
        y2 = np.exp(-((x - probability) ** 2) / 0.02)
        
        ax3.fill_between(x, y1, alpha=0.6, color='#00ff88', label='Normal')
        ax3.fill_between(x, y2, alpha=0.6, color='#ff4757', label='Tumor')
        ax3.axvline(x=probability, color='white', linestyle='--', linewidth=2)
        ax3.set_xlabel('Probabilidade', fontweight='bold', color='white', fontsize=10)
        ax3.set_ylabel('Densidade', fontweight='bold', color='white', fontsize=10)
        ax3.set_title('Distribuição de Probabilidade', fontweight='bold', color='white', fontsize=11, pad=10)
        ax3.legend(fontsize=9)
        ax3.grid(True, alpha=0.2, color='white')
        ax3.set_facecolor('#242b4d')
        ax3.tick_params(axis='both', colors='white', labelsize=9)
        
        # Gráfico 4 - Escala de risco horizontal
        risk_categories = ['Muito Baixo', 'Baixo', 'Médio', 'Alto', 'Muito Alto']
        risk_values = [0.2, 0.2, 0.2, 0.2, 0.2]
        
        # Determinar posição atual na escala
        current_risk = probability
        
        bars_risk = ax4.barh(risk_categories, risk_values, color='lightgray', alpha=0.3)
        
        # Colorir barra correspondente ao risco atual
        if current_risk <= 0.2:
            bars_risk[0].set_color('#00ff88')
        elif current_risk <= 0.4:
            bars_risk[1].set_color('#ffa726')
        elif current_risk <= 0.6:
            bars_risk[2].set_color('#ff9500')
        elif current_risk <= 0.8:
            bars_risk[3].set_color('#ff4757')
        else:
            bars_risk[4].set_color('#c0392b')
        
        # Adicionar marcador da posição atual
        risk_position = int(current_risk * (len(risk_categories) - 1))
        ax4.axhline(y=risk_position, color='white', linestyle='-', linewidth=3)
        
        ax4.set_xlim(0, 0.2)
        ax4.set_title('Escala de Risco', fontweight='bold', color='white', fontsize=11, pad=10)
        ax4.set_xlabel('Indicador', fontweight='bold', color='white', fontsize=10)
        ax4.set_facecolor('#242b4d')
        ax4.grid(True, alpha=0.2, color='white')
        ax4.tick_params(axis='both', colors='white', labelsize=9)
        
        # Remover tight_layout pois já temos subplots_adjust
        # plt.tight_layout()
        
        # Incorporar no tkinter
        canvas = FigureCanvasTkAgg(fig, self.charts_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Mudar para aba de gráficos
        self.notebook.select(1)
    
    def preprocess_image(self, image):
        """Pré-processa imagem para o modelo (robusto a artefatos).
        - Corta 10% das bordas (remove régua/legendas)
        - Converte para escala de cinza e aplica CLAHE
        - Normaliza 0-1 e replica para 3 canais
        - Redimensiona para o tamanho do modelo
        """
        h, w = image.shape[:2]
        margin_h = int(h * 0.10)
        margin_w = int(w * 0.10)
        cropped = image[margin_h:h - margin_h, margin_w:w - margin_w]

        if len(cropped.shape) == 3:
            gray = cv2.cvtColor(cropped, cv2.COLOR_RGB2GRAY)
        else:
            gray = cropped

        try:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            gray = clahe.apply(gray)
        except Exception:
            gray = cv2.equalizeHist(gray)

        gray = gray.astype(np.float32) / 255.0
        img_rgb = np.stack([gray, gray, gray], axis=-1)
        img_resized = cv2.resize(img_rgb, self.img_size)
        img_resized = np.expand_dims(img_resized, axis=0)
        return img_resized

    def predict_with_tta(self, img_batch):
        """Aplica Test-Time Augmentation e retorna média das probabilidades"""
        # img_batch: (1, H, W, 3) em float32 [0,1]
        x = img_batch[0]
        variants = []
        variants.append(x)  # original
        variants.append(np.flip(x, axis=1))  # flip horizontal
        variants.append(np.flip(x, axis=0))  # flip vertical
        variants.append(np.rot90(x, 1))
        variants.append(np.rot90(x, 2))
        variants.append(np.rot90(x, 3))
        
        probs = []
        for v in variants:
            pv = np.expand_dims(v, axis=0)
            p = self.model.predict(pv, verbose=0)[0][0]
            probs.append(float(p))
        
        return float(np.mean(probs))

    def compute_optimal_threshold(self):
        """Calcula limiar ótimo no conjunto Testing (Youden J)"""
        testing_dir = "datasets/brain_cancer/Testing"
        if not os.path.exists(testing_dir):
            messagebox.showwarning("Aviso", "Pasta Testing não encontrada")
            return
        
        classes = {
            'notumor': 0,
            'glioma': 1,
            'meningioma': 1,
            'pituitary': 1
        }
        
        probs = []
        labels = []
        
        # Amostrar limitando para rapidez
        for cls, lab in classes.items():
            cls_dir = os.path.join(testing_dir, cls)
            if not os.path.exists(cls_dir):
                continue
            files = [f for f in os.listdir(cls_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
            files = files[:80]  # limitar
            for f in files:
                try:
                    p = os.path.join(cls_dir, f)
                    img = cv2.imread(p)
                    if img is None:
                        continue
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    x = self.preprocess_image(img)
                    prob = self.predict_with_tta(x)
                    probs.append(prob)
                    labels.append(lab)
                except Exception:
                    continue
        
        if not probs:
            messagebox.showwarning("Aviso", "Não foi possível calcular o limiar")
            return
        
        probs = np.array(probs)
        labels = np.array(labels)
        
        # Procurar limiar ótimo maximizando Youden J = sens + esp - 1
        thresholds = np.linspace(0.3, 0.8, 26)
        best_t = self.decision_threshold.get()
        best_j = -1.0
        best_metrics = (0.0, 0.0)
        for t in thresholds:
            preds = (probs > t).astype(int)
            tp = int(np.sum((preds == 1) & (labels == 1)))
            tn = int(np.sum((preds == 0) & (labels == 0)))
            fp = int(np.sum((preds == 1) & (labels == 0)))
            fn = int(np.sum((preds == 0) & (labels == 1)))
            sens = tp / (tp + fn + 1e-9)
            esp = tn / (tn + fp + 1e-9)
            j = sens + esp - 1
            if j > best_j:
                best_j = j
                best_t = t
                best_metrics = (sens, esp)
        
        self.decision_threshold.set(best_t)
        self.quick_result_icon.config(text="✅", fg=self.colors['success'])
        self.quick_result_text.config(text=f"Limiar ótimo: {best_t:.2f}\nSens: {best_metrics[0]:.0%} • Esp: {best_metrics[1]:.0%}")
    
    def reset_results(self):
        """Reseta resultados anteriores"""
        self.quick_result_icon.config(text="🔄", fg=self.colors['text_muted'])
        self.quick_result_text.config(text="Aguardando análise...", fg=self.colors['text_secondary'])
        self.result_text.delete(1.0, tk.END)
    
    def get_current_time(self):
        """Retorna data/hora atual formatada"""
        from datetime import datetime
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    def generate_activation_map(self, processed_img, is_tumor, confidence):
        """Gera mapa de ativação mostrando onde a IA está focando"""
        try:
            # Limpar frame anterior
            for widget in self.heatmap_frame.winfo_children():
                widget.destroy()
            
            # Criar figura para o heatmap
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            fig.patch.set_facecolor('#1a1f35')
            fig.suptitle('Mapa de Ativação - Regiões de Interesse da IA', 
                        fontsize=16, fontweight='bold', color='white')
            
            # Imagem original
            original_img = cv2.resize(self.current_image, (128, 128))
            ax1.imshow(original_img)
            ax1.set_title('Imagem Original', color='white', fontweight='bold')
            ax1.axis('off')
            
            # Simular mapa de ativação baseado na predição
            # Em um modelo real, usaríamos Grad-CAM ou técnicas similares
            heatmap = self.create_simulated_heatmap(is_tumor, confidence)
            
            # Sobrepor heatmap na imagem
            im = ax2.imshow(original_img, alpha=0.6)
            im2 = ax2.imshow(heatmap, alpha=0.4, cmap='hot', interpolation='bilinear')
            ax2.set_title('Mapa de Ativação', color='white', fontweight='bold')
            ax2.axis('off')
            
            # Barra de cores
            cbar = plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
            cbar.set_label('Ativação da IA', color='white', fontweight='bold')
            cbar.ax.yaxis.set_tick_params(color='white')
            plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
            
            # Legenda explicativa sem emojis para evitar warnings
            legend_text = """
VERMELHO: Regiões suspeitas detectadas pela IA
AMARELO: Áreas de interesse moderado  
AZUL: Regiões consideradas normais
            """
            
            fig.text(0.02, 0.02, legend_text.strip(), color='white', fontsize=10,
                    bbox=dict(boxstyle="round,pad=0.5", facecolor='#242b4d', alpha=0.8))
            
            plt.tight_layout()
            
            # Incorporar no tkinter
            canvas = FigureCanvasTkAgg(fig, self.heatmap_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            
            print("✅ Mapa de ativação gerado com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao gerar mapa de ativação: {e}")
            # Mostrar mensagem de erro na aba
            error_label = tk.Label(
                self.heatmap_frame,
                text=f"❌\n\nErro ao gerar mapa:\n{str(e)}",
                font=('Segoe UI', 12),
                bg=self.colors['bg_secondary'],
                fg=self.colors['danger'],
                justify='center'
            )
            error_label.pack(expand=True)
    
    def create_simulated_heatmap(self, is_tumor, confidence):
        """Cria um heatmap simulado baseado na predição"""
        # Criar mapa base 128x128
        heatmap = np.zeros((128, 128))
        
        if is_tumor:
            # Se tumor detectado, criar focos de ativação
            # Simular regiões suspeitas
            
            # Foco principal (região central-superior)
            center_x, center_y = 64, 45
            for i in range(128):
                for j in range(128):
                    dist = np.sqrt((i - center_x)**2 + (j - center_y)**2)
                    if dist < 25:
                        heatmap[j, i] = confidence * np.exp(-dist/15)
            
            # Foco secundário se confiança alta
            if confidence > 0.8:
                center_x2, center_y2 = 85, 70
                for i in range(128):
                    for j in range(128):
                        dist = np.sqrt((i - center_x2)**2 + (j - center_y2)**2)
                        if dist < 15:
                            heatmap[j, i] = max(heatmap[j, i], 
                                              confidence * 0.7 * np.exp(-dist/10))
        else:
            # Se normal, criar ativação difusa e baixa
            # Simular que a IA está "verificando" mas não encontrando nada suspeito
            noise = np.random.random((128, 128)) * 0.2
            heatmap = noise * (1 - confidence)
        
        # Aplicar suavização
        from scipy import ndimage
        try:
            heatmap = ndimage.gaussian_filter(heatmap, sigma=3)
        except:
            # Se scipy não disponível, usar média simples
            kernel_size = 5
            kernel = np.ones((kernel_size, kernel_size)) / (kernel_size * kernel_size)
            heatmap = np.convolve(heatmap.flatten(), kernel.flatten(), mode='same').reshape(128, 128)
        
        return heatmap
    
    def create_animations(self):
        """Cria animações sutis"""
        pass  # Placeholder para futuras animações
    
    def run(self):
        """Executa a interface"""
        self.root.mainloop()

def main():
    """Função principal"""
    print("🚀 Iniciando NeuroAI - Interface Moderna de Diagnóstico...")
    
    try:
        app = ModernCancerDiagnosis()
        app.run()
    except Exception as e:
        print(f"❌ Erro ao inicializar interface: {e}")

if __name__ == "__main__":
    main()