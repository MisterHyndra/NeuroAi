# NeuroAI Web Dashboard

Versão web do sistema de diagnóstico cerebral, usando **seu modelo .h5 treinado diretamente** via API local Python.

## 🎯 Como Funciona (Igual ao Desktop)

1. **Usuário faz upload da imagem** → input file HTML
2. **Frontend envia para API Python** → Flask local (porta 5000)
3. **Servidor preprocessa e prediz** → usa TensorFlow/Keras com modelo .h5
4. **Interface mostra resultado** → tumor/normal, confiança, gráficos automaticamente

**Análise instantânea ao carregar imagem**, igual ao `visual_diagnosis_modern.py`!

---

## � Como Usar (3 Passos)

### **1. Instalar Dependências (primeira vez)**

```bash
pip install flask flask-cors
```

Ou instale tudo de uma vez:
```bash
pip install -r requirements.txt
```

---

### **2. Iniciar o Servidor**

**Opção A - Script automático (Windows):**
```bash
run_web_dashboard.bat
```

**Opção B - Manual:**
```bash
python web/api_server.py
```

Você verá:
```
🧠 NeuroAI - Servidor de Inferência Local
✅ Modelo carregado com sucesso!
🌐 Servidor rodando em: http://localhost:5000
```

---

### **3. Abrir a Interface Web**

Abra no navegador:
```
http://localhost:5000/web/index.html
```

**Pronto!** Arraste uma imagem e a análise roda automaticamente 🎉

---

## 💡 Arquitetura: Por Que Funciona Sem Back-end Externo?

### **Desktop (Python):**
- ✅ Modelo `.h5` carrega localmente
- ✅ TensorFlow/Keras faz inferência no computador
- ✅ Tkinter mostra interface

### **Web (Python + HTML):**
- ✅ Servidor Flask **local** (porta 5000)
- ✅ Mesmo modelo `.h5` treinado
- ✅ Frontend HTML envia imagem via API local
- ✅ Preprocessing e predição no servidor local

**Resultado:** Ambos rodam **100% local**, sem internet, sem servidor externo, sem cloud!

---

## ⚙️ Detalhes Técnicos

### **Por que não usa TensorFlow.js direto?**
- ✅ Evita conversão do modelo (usa `.h5` direto)
- ✅ Aproveita TensorFlow/Keras já instalado
- ✅ Mesmo código de preprocessing do desktop
- ✅ Performance melhor (servidor vs navegador)

### **Como funciona a comunicação?**
```
Navegador (HTML/JS)  →  Flask API (Python)  →  Modelo .h5
     Upload              Preprocessa             Predição
      ↓                      ↓                       ↓
   FormData           resize + normalize        model.predict()
      ↓                      ↓                       ↓
   Recebe ←          JSON Response  ←         [prob_normal, prob_tumor]
   Mostra gráficos
```

### **Auto-análise ao upload:**
Ao selecionar imagem, já executa automaticamente (igual ao desktop quando clica "Analisar").

---

## 🎯 Próximos Passos Opcionais

1. **Deploy em servidor real** (Flask em cloud + domínio)
2. **Autenticação** (login de médicos)
3. **Banco de dados** (histórico de análises)
4. **PACS/DICOM** (integração hospitalar)
5. **Ensemble** (múltiplos modelos)
