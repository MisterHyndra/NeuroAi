// Estado global da aplicação
const API_URL = 'http://localhost:5000/api';
let currentImage = null;
let threshold = 0.35;  // Mesmo threshold do desktop
let charts = {};
let currentUser = null;
let authToken = null;

// Aguarda modal.js carregar
function waitForModal(callback) {
    if (typeof showConfirmModal === 'function') {
        callback();
    } else {
        setTimeout(() => waitForModal(callback), 100);
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    initializeApp();
    setupEventListeners();
});

// Verifica se usuário está autenticado
function checkAuth() {
    authToken = localStorage.getItem('neuroai_token');
    const userStr = localStorage.getItem('neuroai_user');
    
    if (!authToken || !userStr) {
        window.location.href = 'login.html';
        return;
    }
    
    currentUser = JSON.parse(userStr);
    updateUserInfo();
    
    // Verifica se token ainda é válido (não bloqueante)
    fetch(`${API_URL}/auth/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: authToken })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.valid) {
            localStorage.removeItem('neuroai_token');
            localStorage.removeItem('neuroai_user');
            window.location.href = 'login.html';
        }
    })
    .catch(error => console.error('Erro ao verificar token:', error));
}

// Atualiza informações do usuário na interface
function updateUserInfo() {
    const header = document.querySelector('.header .status');
    if (header && currentUser) {
        header.innerHTML = `
            <span style="margin-right: 15px;">👤 ${currentUser.full_name || currentUser.username}</span>
            <button onclick="window.location.href='history.html'" style="background: #00d9ff; padding: 0.5rem 1rem; border: none; border-radius: 5px; color: #0a0e27; cursor: pointer; margin-right: 10px; font-weight: bold;">
                 Histórico
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
        headers: { 'Content-Type': 'application/json' },
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
    
    fetch(`${API_URL}/health`)
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok' && data.model_loaded) {
            updateStatus('Modelo carregado ✓ Pronto para análise', 'ready');
            
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
        } else {
            throw new Error('Modelo não carregado no servidor');
        }
    })
    .catch(error => {
        console.error('Erro ao conectar com servidor:', error);
        updateStatus('⚠️ Servidor não encontrado. Inicie com: python web/api_server.py', 'error');
    });
}

// Configura event listeners
function setupEventListeners() {
    const imageInput = document.getElementById('imageInput');
    const selectButton = document.getElementById('selectButton');
    const uploadArea = document.getElementById('uploadArea');
    const analyzeButton = document.getElementById('analyzeButton');
    const thresholdSlider = document.getElementById('thresholdSlider');
    const generateReport = document.getElementById('generateReport');
    
    selectButton.addEventListener('click', () => imageInput.click());
    uploadArea.addEventListener('click', () => imageInput.click());
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#00ffff';
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#00d9ff';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#00d9ff';
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            loadImage(file);
        }
    });
    
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            loadImage(file);
        }
    });
    
    analyzeButton.addEventListener('click', () => runAnalysis());
    
    thresholdSlider.addEventListener('input', (e) => {
        threshold = e.target.value / 100;
        document.getElementById('thresholdValue').textContent = threshold.toFixed(2);
        
        if (currentImage && currentImage.predictions) {
            updateResultDisplay(currentImage.predictions, threshold);
        }
    });
    
    generateReport.addEventListener('click', () => downloadReport());
    
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => switchTab(tab.dataset.tab));
    });
}

// Carrega imagem
function loadImage(file) {
    const reader = new FileReader();
    
    reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
            currentImage = { element: img, file: file, predictions: null };
            
            const preview = document.getElementById('imagePreview');
            preview.innerHTML = `<img src="${e.target.result}" alt="Imagem carregada">`;
            
            drawImageOnCanvas('originalCanvas', img);
            
            document.getElementById('analyzeButton').disabled = false;
            resetResults();
            
            // Auto-análise 500ms após carregar
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
    
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0);
}

// Atualiza mapa de ativação
function updateActivationMap(heatmapBase64) {
    const canvas = document.getElementById('activationCanvas');
    const ctx = canvas.getContext('2d');
    const originalImg = currentImage.element;
    
    const heatmapImg = new Image();
    heatmapImg.onload = () => {
        canvas.width = 600;
        canvas.height = 300;
        
        ctx.fillStyle = '#1a1f35';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        const size = 256;
        const offsetY = (canvas.height - size) / 2;
        ctx.drawImage(originalImg, 20, offsetY, size, size);
        
        ctx.fillStyle = '#00d4ff';
        ctx.font = 'bold 14px Segoe UI';
        ctx.fillText('Imagem Original', 20, offsetY - 10);
        
        const offsetX = 320;
        ctx.globalAlpha = 0.6;
        ctx.drawImage(originalImg, offsetX, offsetY, size, size);
        ctx.globalAlpha = 0.4;
        ctx.drawImage(heatmapImg, offsetX, offsetY, size, size);
        ctx.globalAlpha = 1.0;
        
        ctx.fillStyle = '#00d4ff';
        ctx.fillText('Mapa de Ativação', offsetX, offsetY - 10);
        
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
    
    const activationTab = document.getElementById('activationTab');
    const placeholder = activationTab.querySelector('p');
    if (placeholder) {
        placeholder.style.display = 'none';
    }
}

// Executa análise via API Python local
async function runAnalysis() {
    if (!currentImage) {
        showAlertModal(' Aviso', 'Carregue uma imagem primeiro.', { icon: '', buttonText: 'OK' });
        return;
    }
    
    try {
        updateStatus('Analisando imagem...', 'analyzing');
        
        const formData = new FormData();
        formData.append('image', currentImage.file);
        
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
        
        currentImage.predictions = {
            normal: result.predictions.normal,
            tumor: result.predictions.tumor,
            confidence: result.confidence,
            heatmap: result.heatmap || null,
            timestamp: new Date()
        };
        
        updateResultDisplay(currentImage.predictions, threshold);
        updateCharts(currentImage.predictions);
        
        if (result.heatmap) {
            updateActivationMap(result.heatmap);
        }
        
        await saveToHistory(currentImage.predictions, currentImage.file.name);
        
        switchTab('analysis');
        document.getElementById('generateReport').disabled = false;
        
        updateStatus('Análise concluída ✓', 'ready');
        
    } catch (error) {
        console.error('Erro na análise:', error);
        updateStatus('Erro na análise', 'error');
        showAlertModal(' Erro na Análise', 'Erro ao analisar imagem: ' + error.message + '\n\nVerifique se o servidor está rodando: python web/api_server.py', { icon: '❌' });
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
    
    updateReport(predictions, isTumor, threshold);
}

// Atualiza gráficos
function updateCharts(predictions) {
    const confidence = predictions.confidence * 100;
    const uncertainty = 100 - confidence;
    
    createBarChart('classificationChart', 
        ['Normal', 'Tumor'],
        [predictions.normal, predictions.tumor],
        ['#64ff64', '#ff6464']
    );
    
    document.getElementById('confidenceTitle').textContent = 
        `Nível de Confiança: ${confidence.toFixed(1)}%`;
    createPieChart('confidenceChart',
        ['Confiança', 'Incerteza'],
        [confidence, uncertainty],
        ['#00d9ff', '#666666']
    );
    
    createDistributionChart('distributionChart', predictions);
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
            plugins: { legend: { display: false } },
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
                    tension: 0.4,
                    pointRadius: 0
                },
                {
                    label: 'Tumor',
                    data: tumorCurve,
                    borderColor: '#ff6464',
                    backgroundColor: 'rgba(255, 100, 100, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    labels: { color: '#aaa' }
                }
            },
            scales: {
                y: {
                    ticks: { color: '#aaa' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                x: {
                    ticks: { color: '#aaa' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                }
            }
        }
    });
}

// Cria gráfico de risco
function createRiskChart(canvasId, tumorProb) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    if (charts[canvasId]) {
        charts[canvasId].destroy();
    }
    
    const riskLevel = tumorProb * 100;
    const riskColor = riskLevel < 25 ? '#64ff64' : riskLevel < 50 ? '#ffff00' : riskLevel < 75 ? '#ffaa00' : '#ff6464';
    
    charts[canvasId] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Risco de Tumor'],
            datasets: [{
                label: 'Nível de Risco (%)',
                data: [riskLevel],
                backgroundColor: riskColor,
                borderColor: riskColor,
                borderWidth: 2
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    ticks: { color: '#aaa' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                y: {
                    ticks: { color: '#aaa' },
                    grid: { display: false }
                }
            }
        }
    });
}

// Muda aba
function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    document.getElementById(tabName + 'Tab').classList.add('active');
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
}

// Atualiza status
function updateStatus(message, status) {
    const statusEl = document.getElementById('modelStatus');
    if (statusEl) {
        statusEl.textContent = message;
        statusEl.style.color = status === 'error' ? '#ff6464' : status === 'ready' ? '#64ff64' : '#00d9ff';
    }
}

// Reseta resultados
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
}

// Atualiza relatório
function updateReport(predictions, isTumor, threshold) {
    const timestamp = new Date().toLocaleString('pt-BR');
    
    document.getElementById('reportDetails').innerHTML = `
        <strong>Timestamp:</strong> ${timestamp}<br>
        <strong>Probabilidade Normal:</strong> ${(predictions.normal * 100).toFixed(2)}%<br>
        <strong>Probabilidade Tumor:</strong> ${(predictions.tumor * 100).toFixed(2)}%<br>
        <strong>Confiança:</strong> ${(predictions.confidence * 100).toFixed(2)}%<br>
        <strong>Limiar Aplicado:</strong> ${threshold.toFixed(2)}
    `;
    
    if (isTumor) {
        document.getElementById('reportResult').innerHTML = `
            <span style="color: #ff6464; font-weight: bold;">⚠️ TUMOR DETECTADO</span><br>
            A IA identificou padrões consistentes com presença de tumor cerebral.<br>
            Confiança: ${(predictions.confidence * 100).toFixed(2)}%
        `;
        document.getElementById('reportInterpretation').innerHTML = `
            <strong>Interpretação:</strong> O modelo detectou características suspeitas.<br>
            <strong>Ação Recomendada:</strong> Encaminhe para revisão médica urgente.
        `;
    } else {
        document.getElementById('reportResult').innerHTML = `
            <span style="color: #64ff64; font-weight: bold;">✓ TECIDO NORMAL</span><br>
            Nenhum padrão suspeito foi identificado nesta análise.<br>
            Confiança: ${(predictions.confidence * 100).toFixed(2)}%
        `;
        document.getElementById('reportInterpretation').innerHTML = `
            <strong>Interpretação:</strong> Não foram encontradas anomalias significativas.<br>
            <strong>Ação Recomendada:</strong> Manutenção de acompanhamento regular.
        `;
    }
}

// Salva análise no histórico
async function saveToHistory(predictions, imageName) {
    try {
        const response = await fetch(`${API_URL}/history`, {
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
                result: predictions.tumor > threshold ? 'Tumor' : 'Normal'
            })
        });
        
        if (response.ok) {
            console.log('Análise salva no histórico');
        }
    } catch (error) {
        console.error('Erro ao salvar no histórico:', error);
    }
}

// Download relatório
function downloadReport() {
    if (!currentImage || !currentImage.predictions) {
        showAlertModal('⚠️ Aviso', 'Realize uma análise primeiro.', { icon: '📊', buttonText: 'OK' });
        return;
    }
    
    const isTumor = currentImage.predictions.tumor > threshold;
    const resultado = isTumor ? 'TUMOR DETECTADO' : 'NORMAL';
    
    const content = `
NeuroAI - Relatório de Diagnóstico Cerebral
============================================
Data: ${new Date().toLocaleString('pt-BR')}
Usuário: ${currentUser.username}

RESULTADO PRINCIPAL
${resultado}
Confiança: ${(currentImage.predictions.confidence * 100).toFixed(2)}%

ANÁLISE DETALHADA
Probabilidade Normal: ${(currentImage.predictions.normal * 100).toFixed(2)}%
Probabilidade Tumor: ${(currentImage.predictions.tumor * 100).toFixed(2)}%
Limiar de Decisão: ${threshold.toFixed(2)}

RECOMENDAÇÕES
${isTumor 
    ? '• Encaminhe para revisão médica urgente\n• Realize exames complementares\n• Mantenha contato com especialista' 
    : '• Manutenção de acompanhamento regular\n• Próxima revisão conforme protocolo\n• Contato preventivo com especialista'}

Este relatório é fornecido apenas para fins informativos e não substitui avaliação médica profissional.
    `;
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `NeuroAI_Relatorio_${new Date().getTime()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}
