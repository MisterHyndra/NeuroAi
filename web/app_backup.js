// Estado global da aplicação
const API_URL = 'http://localhost:5000/api';
let currentImage = null;
let threshold = 0.35;  // Mesmo threshold do desktop
let charts = {};
let currentUser = null;
let authToken = null;

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    // Verifica autenticação e inicializa app
    checkAuth();
    initializeApp();
    setupEventListeners();
    console.log('NeuroAI front-end inicializado.');
});

// Captura erros globais e mostra no status para facilitar debug
window.addEventListener('error', (event) => {
    console.error('Erro global capturado:', event.error || event.message);
    updateStatus('Erro de script: ' + (event.message || 'desconhecido'), 'error');
});

// Verifica se usuário está autenticado
function checkAuth() {
    authToken = localStorage.getItem('neuroai_token');
    const userStr = localStorage.getItem('neuroai_user');
    
    if (!authToken || !userStr) {
        // Redireciona para login
        window.location.href = 'login.html';
        return;
    }
    
    currentUser = JSON.parse(userStr);
    
    // Atualiza informações do usuário imediatamente
    updateUserInfo();
    
    // Verifica se token ainda é válido (não bloqueante)
    fetch(`${API_URL}/auth/verify`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ token: authToken })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.valid) {
            // Token inválido, redireciona
            localStorage.removeItem('neuroai_token');
            localStorage.removeItem('neuroai_user');
            window.location.href = 'login.html';
        }
    })
    .catch(error => {
        console.error('Erro ao verificar token:', error);
        // Continua mesmo com erro de verificação
    });
}

// Atualiza informações do usuário na interface
function updateUserInfo() {
    const header = document.querySelector('.header .status');
    if (header && currentUser) {
        header.innerHTML = `
            <span style="margin-right: 15px;">👤 ${currentUser.full_name || currentUser.username}</span>
            <button onclick="window.location.href='history.html'" style="background: #00d9ff; padding: 0.5rem 1rem; border: none; border-radius: 5px; color: #0a0e27; cursor: pointer; margin-right: 10px; font-weight: bold;">
                📊 Histórico
            </button>
            <button onclick="logout()" style="background: #ff4757; padding: 0.5rem 1rem; border: none; border-radius: 5px; color: white; cursor: pointer;">
                Sair
            </button>
        `;
    }
}

// Logout
function logout() {
    fetch(`${API_URL}/auth/logout`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ token: authToken })
    }).finally(() => {
        localStorage.removeItem('neuroai_token');
        localStorage.removeItem('neuroai_user');
        window.location.href = 'login.html';
    });
}

// Inicializa a aplicação e verifica conexão com API
function initializeApp() {
    updateStatus('Conectando ao servidor local...', 'loading');
    
    // Verifica se o servidor está rodando (não bloqueante)
    fetch(`${API_URL}/health`)
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok' && data.model_loaded) {
            updateStatus('Modelo carregado ✓ Pronto para análise', 'ready');
            
            // Busca informações do modelo
            fetch(`${API_URL}/model-info`)
            .then(infoResponse => infoResponse.json())
            .then(modelInfo => {
                const shape = modelInfo.input_shape;
                document.getElementById('modelInfo').textContent = 
                    `• Arquitetura: CNN (entrada ${shape[1]}x${shape[2]}x${shape[3]})`;
            })
            .catch(e => {
                document.getElementById('modelInfo').textContent = 
                    `• Arquitetura: CNN (modelo Python local)`;
            });
            
            console.log('Conectado ao servidor de inferência:', data);
        } else {
            throw new Error('Modelo não carregado no servidor');
        }
    })
    .catch(error => {
        console.error('Erro ao conectar com servidor:', error);
        updateStatus('⚠️ Servidor não encontrado. Inicie com: python web/api_server.py', 'error');
        showServerInstructions();
    });
}

function showServerInstructions() {
    const msg = `
Para usar o modelo .h5 treinado diretamente na web:

1. Instale Flask (se necessário):
   pip install flask flask-cors

2. Inicie o servidor de inferência:
   python web/api_server.py

3. Abra a interface web:
   http://localhost:5000/web/index.html

O servidor carrega seu modelo .h5 e responde via API local.
    `;
    console.info(msg);
}

// Configura event listeners
function setupEventListeners() {
    console.log('Configurando event listeners...');
    // Upload de imagem
    const imageInput = document.getElementById('imageInput');
    const selectButton = document.getElementById('selectButton');
    const uploadArea = document.getElementById('uploadArea');
    const analyzeButton = document.getElementById('analyzeButton');
    const thresholdSlider = document.getElementById('thresholdSlider');
    const generateReport = document.getElementById('generateReport');
    
    // Garante que o input não está desabilitado
    try { imageInput.disabled = false; } catch {}
    
    const openFileDialog = async () => {
        console.log('Abrindo seletor de arquivos...');
        try {
            // Primeiro tenta via input
            imageInput.click();
        } catch (e1) {
            console.warn('Falha ao usar input.click():', e1);
            // Fallback moderno
            if (window.showOpenFilePicker) {
                try {
                    const [handle] = await window.showOpenFilePicker({
                        types: [{
                            description: 'Imagens',
                            accept: { 'image/*': ['.png', '.jpg', '.jpeg', '.bmp', '.webp'] }
                        }]
                    });
                    const file = await handle.getFile();
                    if (file) {
                        console.log('Arquivo selecionado via FilePicker:', file.name);
                        loadImage(file);
                    }
                } catch (e2) {
                    console.error('FilePicker falhou:', e2);
                    alert('Não foi possível abrir o seletor de arquivos. Verifique permissões do navegador.');
                }
            } else {
                alert('Seu navegador bloqueou o seletor de arquivos. Tente outro navegador ou verifique permissões.');
            }
        }
    };
    
    selectButton.addEventListener('click', () => { console.log('Clique em Selecionar Imagem'); openFileDialog(); });
    uploadArea.addEventListener('click', () => { console.log('Clique na área de upload'); openFileDialog(); });
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#00ffff';
        console.log('Dragover na área de upload');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#00d9ff';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#00d9ff';
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            console.log('Arquivo solto:', file.name);
            loadImage(file);
        }
    });
    
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            console.log('Arquivo selecionado:', file.name);
            loadImage(file);
        }
    });
    
    // Análise
    analyzeButton.addEventListener('click', () => { console.log('Clique em INICIAR DIAGNÓSTICO'); runAnalysis(); });
    
    // Threshold
    thresholdSlider.addEventListener('input', (e) => {
        threshold = e.target.value / 100;
        console.log('Threshold alterado para', threshold);
        document.getElementById('thresholdValue').textContent = threshold.toFixed(2);
        
        // Re-analisa se já tem resultado
        if (currentImage) {
            updateResultDisplay(currentImage.predictions, threshold);
        }
    });
    
    // Relatório
    generateReport.addEventListener('click', () => { console.log('Clique em RELATÓRIO'); downloadReport(); });
    
    // Tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => { console.log('Clique na aba', tab.dataset.tab); switchTab(tab.dataset.tab); });
    });
    console.log('Event listeners configurados.');
}

// Carrega imagem
function loadImage(file) {
    const reader = new FileReader();
    
    reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
            currentImage = { element: img, file: file, predictions: null };
            
            // Mostra preview
            const preview = document.getElementById('imagePreview');
            preview.innerHTML = `<img src="${e.target.result}" alt="Imagem carregada">`;
            
            // Desenha no canvas
            drawImageOnCanvas('originalCanvas', img);
            
            // Habilita botão de análise
            document.getElementById('analyzeButton').disabled = false;
            
            // Limpa resultados anteriores
            resetResults();
            
            // 🔥 AUTO-ANÁLISE: Roda automaticamente ao carregar
            setTimeout(() => runAnalysis(), 500);
        };
        img.src = e.target.result;
    };
    
    reader.readAsDataURL(file);
}

// Desenha imagem no canvas
function drawImageOnCanvas(canvasId, img) {
    const canvas = document.getElementById(canvasId);
    const ctx = canvas.getContext('2d');
    
    // Define tamanho do canvas
    canvas.width = img.width;
    canvas.height = img.height;
    
    // Desenha a imagem
    ctx.drawImage(img, 0, 0);
}

// Atualiza mapa de ativação
function updateActivationMap(heatmapBase64) {
    const canvas = document.getElementById('activationCanvas');
    const ctx = canvas.getContext('2d');
    
    // Imagem original
    const originalImg = currentImage.element;
    
    // Carrega heatmap
    const heatmapImg = new Image();
    heatmapImg.onload = () => {
        // Define tamanho
        canvas.width = 600;
        canvas.height = 300;
        
        // Limpa canvas
        ctx.fillStyle = '#1a1f35';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Desenha original (esquerda)
        const size = 256;
        const offsetY = (canvas.height - size) / 2;
        ctx.drawImage(originalImg, 20, offsetY, size, size);
        
        // Texto "Original"
        ctx.fillStyle = '#00d4ff';
        ctx.font = 'bold 14px Segoe UI';
        ctx.fillText('Imagem Original', 20, offsetY - 10);
        
        // Desenha original com heatmap sobreposto (direita)
        const offsetX = 320;
        ctx.globalAlpha = 0.6;
        ctx.drawImage(originalImg, offsetX, offsetY, size, size);
        ctx.globalAlpha = 0.4;
        ctx.drawImage(heatmapImg, offsetX, offsetY, size, size);
        ctx.globalAlpha = 1.0;
        
        // Texto "Mapa de Ativação"
        ctx.fillStyle = '#00d4ff';
        ctx.fillText('Mapa de Ativação', offsetX, offsetY - 10);
        
        // Legenda
        ctx.fillStyle = '#ffffff';
        ctx.font = '11px Segoe UI';
        const legend = [
            '🔴 VERMELHO: Regiões suspeitas',
            '🟡 AMARELO: Interesse moderado',
            '🔵 AZUL: Regiões normais'
        ];
        legend.forEach((text, i) => {
            ctx.fillText(text, 20, canvas.height - 50 + i * 18);
        });
    };
    heatmapImg.src = 'data:image/png;base64,' + heatmapBase64;
    
    // Remove mensagem de "aguardando"
    const activationTab = document.getElementById('activationTab');
    const placeholder = activationTab.querySelector('p');
    if (placeholder) {
        placeholder.style.display = 'none';
    }
}

// Não precisa mais de preprocessamento no frontend
// O servidor Python faz tudo isso

// Executa análise via API Python local
async function runAnalysis() {
    if (!currentImage) {
        alert('Carregue uma imagem primeiro.');
        return;
    }
    
    try {
        updateStatus('Analisando imagem...', 'analyzing');
        
        // Prepara FormData com a imagem
        const formData = new FormData();
        formData.append('image', currentImage.file);
        
        // Chama API Python
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Erro na API: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.error || 'Erro desconhecido');
        }
        
        // Salva resultados
        currentImage.predictions = {
            normal: result.predictions.normal,
            tumor: result.predictions.tumor,
            confidence: result.confidence,
            heatmap: result.heatmap || null,
            timestamp: new Date()
        };
        
        console.log('Resultados:', currentImage.predictions);
        
        // Atualiza interface
        updateResultDisplay(currentImage.predictions, threshold);
        updateCharts(currentImage.predictions);
        
        // Atualiza mapa de ativação
        if (result.heatmap) {
            updateActivationMap(result.heatmap);
        }
        
        // Salva no histórico
        await saveToHistory(currentImage.predictions, currentImage.file.name);
        
        // Muda para aba de análise
        switchTab('analysis');
        
        // Habilita relatório
        document.getElementById('generateReport').disabled = false;
        
        updateStatus('Análise concluída ✓', 'ready');
        
    } catch (error) {
        console.error('Erro na análise:', error);
        updateStatus('Erro na análise', 'error');
        alert('Erro ao analisar imagem: ' + error.message + '\n\nVerifique se o servidor está rodando: python web/api_server.py');
    }
}

// Atualiza display de resultado
function updateResultDisplay(predictions, threshold) {
    const resultDisplay = document.getElementById('resultDisplay');
    const isTumor = predictions.tumor > threshold;
    const confidence = (predictions.confidence * 100).toFixed(1);
    
    if (isTumor) {
        resultDisplay.className = 'result-detected';
        resultDisplay.innerHTML = `
            <div class="icon-placeholder">
                <svg width="80" height="80" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="35" fill="none" stroke="#ff6464" stroke-width="3"/>
                    <path d="M50 30 L50 55 M50 65 L50 70" stroke="#ff6464" stroke-width="4" stroke-linecap="round"/>
                </svg>
            </div>
            <h3>TUMOR DETECTADO</h3>
            <p>Confiança: ${confidence}%</p>
        `;
    } else {
        resultDisplay.className = 'result-normal';
        resultDisplay.innerHTML = `
            <div class="icon-placeholder">
                <svg width="80" height="80" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="35" fill="none" stroke="#64ff64" stroke-width="3"/>
                    <path d="M35 50 L45 60 L65 40" stroke="#64ff64" stroke-width="4" stroke-linecap="round" fill="none"/>
                </svg>
            </div>
            <h3>NORMAL</h3>
            <p>Confiança: ${confidence}%</p>
        `;
    }
    
    // Atualiza relatório
    updateReport(predictions, isTumor, threshold);
}

// Atualiza gráficos
function updateCharts(predictions) {
    const confidence = predictions.confidence * 100;
    const uncertainty = 100 - confidence;
    
    // Gráfico de classificação
    createBarChart('classificationChart', 
        ['Normal', 'Tumor'],
        [predictions.normal, predictions.tumor],
        ['#64ff64', '#ff6464']
    );
    
    // Gráfico de confiança
    document.getElementById('confidenceTitle').textContent = 
        `Nível de Confiança: ${confidence.toFixed(1)}%`;
    createPieChart('confidenceChart',
        ['Confiança', 'Incerteza'],
        [confidence, uncertainty],
        ['#00d9ff', '#666666']
    );
    
    // Distribuição de probabilidade
    createDistributionChart('distributionChart', predictions);
    
    // Escala de risco
    createRiskChart('riskChart', predictions.tumor);
}

// Cria gráfico de barras
function createBarChart(canvasId, labels, data, colors) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    if (charts[canvasId]) {
        charts[canvasId].destroy();
    }
    
    charts[canvasId] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Probabilidade',
                data: data,
                backgroundColor: colors,
                borderColor: colors,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    ticks: { color: '#aaa' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                x: {
                    ticks: { color: '#aaa' },
                    grid: { display: false }
                }
            }
        }
    });
}

// Cria gráfico de pizza
function createPieChart(canvasId, labels, data, colors) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    if (charts[canvasId]) {
        charts[canvasId].destroy();
    }
    
    charts[canvasId] = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderColor: '#0a0e27',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: '#aaa' }
                }
            }
        }
    });
}

// Cria gráfico de distribuição
function createDistributionChart(canvasId, predictions) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    if (charts[canvasId]) {
        charts[canvasId].destroy();
    }
    
    // Simula curvas gaussianas
    const points = 100;
    const x = Array.from({length: points}, (_, i) => i / points);
    
    const normalCurve = x.map(xi => 
        predictions.normal * Math.exp(-Math.pow((xi - 0.3) / 0.15, 2))
    );
    
    const tumorCurve = x.map(xi => 
        predictions.tumor * Math.exp(-Math.pow((xi - 0.7) / 0.15, 2))
    );
    
    charts[canvasId] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: x.map(xi => xi.toFixed(2)),
            datasets: [
                {
                    label: 'Normal',
                    data: normalCurve,
                    borderColor: '#64ff64',
                    backgroundColor: 'rgba(100, 255, 100, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Tumor',
                    data: tumorCurve,
                    borderColor: '#ff6464',
                    backgroundColor: 'rgba(255, 100, 100, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: { color: '#aaa' }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: '#aaa', display: false },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                x: {
                    ticks: { color: '#aaa', display: false },
                    grid: { display: false }
                }
            }
        }
    });
}

// Cria escala de risco
function createRiskChart(canvasId, tumorProb) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    if (charts[canvasId]) {
        charts[canvasId].destroy();
    }
    
    const riskLevels = ['Muito Baixo', 'Baixo', 'Médio', 'Alto', 'Muito Alto'];
    const riskValues = [0.1, 0.2, 0.3, 0.2, 0.2]; // Apenas exemplo
    const riskColors = ['#64ff64', '#88ff88', '#ffdd44', '#ff9944', '#ff6464'];
    
    charts[canvasId] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: riskLevels,
            datasets: [{
                label: 'Indicador',
                data: riskValues,
                backgroundColor: riskColors,
                borderWidth: 0
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    display: false,
                    max: 0.3
                },
                y: {
                    ticks: { color: '#aaa', font: { size: 10 } },
                    grid: { display: false }
                }
            }
        }
    });
}

// Atualiza relatório
function updateReport(predictions, isTumor, threshold) {
    const confidence = (predictions.confidence * 100).toFixed(1);
    const timestamp = predictions.timestamp.toLocaleString('pt-BR');
    
    document.getElementById('reportDetails').innerHTML = `
        • Arquivo: ${currentImage.file.name}<br>
        • Data: ${timestamp}<br>
        • Modelo: brain_cancer_final (Balanceado)<br>
        • Resolução: 128x128 pixels<br>
        • Limiar usado: ${threshold.toFixed(2)}
    `;
    
    document.getElementById('reportResult').innerHTML = `
        • Classificação: <strong>${isTumor ? 'TUMOR DETECTADO' : 'NORMAL'}</strong><br>
        • Confiança: ${confidence}%<br>
        • Probabilidade Normal: ${(predictions.normal * 100).toFixed(1)}%<br>
        • Probabilidade Tumor: ${(predictions.tumor * 100).toFixed(1)}%
    `;
    
    const interpretation = isTumor ? 
        `Possível presença de tumor cerebral detectada. Confiança: ${confidence}%.<br>
        ⚠️ <strong>ATENÇÃO MÉDICA NECESSÁRIA</strong><br>
        • Consulte neurologista imediatamente<br>
        • Realize exames complementares (RM, TC)<br>
        • Não é diagnóstico definitivo` :
        `Nenhuma anomalia significativa detectada. Confiança: ${confidence}%.<br>
        ✓ Resultado compatível com normalidade<br>
        • Mantenha acompanhamento de rotina<br>
        • Consulte médico se houver sintomas`;
    
    document.getElementById('reportInterpretation').innerHTML = interpretation;
}

// Baixa relatório
function downloadReport() {
    if (!currentImage || !currentImage.predictions) {
        alert('Execute uma análise primeiro.');
        return;
    }
    
    const predictions = currentImage.predictions;
    const isTumor = predictions.tumor > threshold;
    const confidence = (predictions.confidence * 100).toFixed(1);
    
    const report = `
=================================================
        NEUROAI DIAGNOSTICS - RELATÓRIO
=================================================

INFORMAÇÕES DA ANÁLISE
----------------------
Arquivo: ${currentImage.file.name}
Data: ${predictions.timestamp.toLocaleString('pt-BR')}
Modelo: brain_cancer_final (Balanceado)
Resolução: 128x128 pixels
Limiar: ${threshold.toFixed(2)}

RESULTADO PRINCIPAL
-------------------
Classificação: ${isTumor ? 'TUMOR DETECTADO' : 'NORMAL'}
Confiança: ${confidence}%
Probabilidade Normal: ${(predictions.normal * 100).toFixed(1)}%
Probabilidade Tumor: ${(predictions.tumor * 100).toFixed(1)}%

INTERPRETAÇÃO
-------------
${isTumor ? 
    'Possível presença de tumor cerebral detectada.\n⚠️ ATENÇÃO MÉDICA NECESSÁRIA\n• Consulte neurologista imediatamente\n• Realize exames complementares' :
    'Nenhuma anomalia significativa detectada.\n✓ Resultado compatível com normalidade\n• Mantenha acompanhamento de rotina'
}

=================================================
Este relatório foi gerado automaticamente por IA
e NÃO substitui avaliação médica profissional.
=================================================
    `;
    
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `neuroai_relatorio_${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
}

// Utilitários
function updateStatus(message, type) {
    const status = document.getElementById('modelStatus');
    status.textContent = message;
    
    const colors = {
        loading: '#ffaa00',
        ready: '#00ff88',
        analyzing: '#00d9ff',
        error: '#ff6464'
    };
    
    status.style.color = colors[type] || '#00d9ff';
}

function switchTab(tabName) {
    // Remove active de todas as tabs
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    
    // Adiciona active na tab selecionada
    document.querySelector(`.tab[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(`${tabName}Tab`).classList.add('active');
}

function resetResults() {
    document.getElementById('resultDisplay').className = 'result-waiting';
    document.getElementById('resultDisplay').innerHTML = `
        <div class="icon-placeholder">
            <svg width="80" height="80" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" fill="none" stroke="#666" stroke-width="2"/>
                <text x="50" y="58" font-size="30" text-anchor="middle" fill="#666">?</text>
            </svg>
        </div>
        <p>Aguardando análise</p>
    `;
    
    document.getElementById('reportDetails').textContent = 'Nenhuma análise realizada ainda.';
    document.getElementById('reportResult').textContent = 'Aguardando diagnóstico...';
    document.getElementById('reportInterpretation').textContent = 'Execute a análise primeiro.';
    document.getElementById('generateReport').disabled = true;
    
    // Limpa gráficos
    Object.values(charts).forEach(chart => chart.destroy());
    charts = {};
    
    // Limpa mapa de ativação
    const canvas = document.getElementById('activationCanvas');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    const activationTab = document.getElementById('activationTab');
    const placeholder = activationTab.querySelector('p');
    if (placeholder) {
        placeholder.style.display = 'block';
    }
}

// Salva análise no histórico
async function saveToHistory(predictions, imageName) {
    if (!authToken) return;
    
    try {
        const isTumor = predictions.tumor > threshold;
        
        await fetch(`${API_URL}/history`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                image_name: imageName,
                prediction_normal: predictions.normal,
                prediction_tumor: predictions.tumor,
                confidence: predictions.confidence,
                threshold_used: threshold,
                result: isTumor ? 'tumor' : 'normal'
            })
        });
        
        console.log('✅ Análise salva no histórico');
    } catch (error) {
        console.error('Erro ao salvar histórico:', error);
    }
}
