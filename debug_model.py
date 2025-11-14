"""
Script de diagnóstico para investigar falsos positivos
"""
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

def load_and_test_model():
    """Carrega modelo e testa com imagem problemática"""
    
    model_path = "models/brain_cancer_corrected.h5"
    
    if not os.path.exists(model_path):
        print("❌ Modelo não encontrado!")
        return
    
    print("🔍 DIAGNÓSTICO DO MODELO")
    print("=" * 50)
    
    # Carregar modelo
    try:
        model = load_model(model_path)
        print(f"✅ Modelo carregado: {model_path}")
        print(f"📊 Arquitetura do modelo:")
        model.summary()
    except Exception as e:
        print(f"❌ Erro ao carregar modelo: {e}")
        return
    
    # Testar com imagem normal (se disponível)
    test_image_path = "deep.jpg"  # Imagem que você mencionou
    
    if os.path.exists(test_image_path):
        print(f"\n🧪 TESTANDO COM IMAGEM: {test_image_path}")
        
        # Carregar imagem
        img = cv2.imread(test_image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        print(f"📐 Dimensões originais: {img.shape}")
        
        # Testar diferentes pré-processamentos
        test_preprocessing_methods(img, model)
    else:
        print(f"⚠️ Imagem de teste não encontrada: {test_image_path}")
        
        # Testar com imagem aleatória
        print("\n🧪 TESTANDO COM IMAGEM ALEATÓRIA")
        random_img = np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8)
        test_preprocessing_methods(random_img, model)

def test_preprocessing_methods(img, model):
    """Testa diferentes métodos de pré-processamento"""
    
    print("\n📋 TESTANDO DIFERENTES PRÉ-PROCESSAMENTOS:")
    
    # Método 1: Original (simples)
    img1 = cv2.resize(img, (128, 128))
    img1 = img1.astype(np.float32) / 255.0
    img1 = np.expand_dims(img1, axis=0)
    
    pred1 = model.predict(img1, verbose=0)[0][0]
    print(f"1. Método original: {pred1:.4f} ({pred1*100:.1f}%)")
    
    # Método 2: Com corte de bordas
    h, w = img.shape[:2]
    margin_h = int(h * 0.10)
    margin_w = int(w * 0.10)
    cropped = img[margin_h:h-margin_h, margin_w:w-margin_w]
    
    img2 = cv2.resize(cropped, (128, 128))
    img2 = img2.astype(np.float32) / 255.0
    img2 = np.expand_dims(img2, axis=0)
    
    pred2 = model.predict(img2, verbose=0)[0][0]
    print(f"2. Com corte de bordas: {pred2:.4f} ({pred2*100:.1f}%)")
    
    # Método 3: Escala de cinza + CLAHE
    if len(cropped.shape) == 3:
        gray = cv2.cvtColor(cropped, cv2.COLOR_RGB2GRAY)
    else:
        gray = cropped
    
    try:
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
    except:
        gray = cv2.equalizeHist(gray)
    
    gray = gray.astype(np.float32) / 255.0
    img3 = np.stack([gray, gray, gray], axis=-1)
    img3 = cv2.resize(img3, (128, 128))
    img3 = np.expand_dims(img3, axis=0)
    
    pred3 = model.predict(img3, verbose=0)[0][0]
    print(f"3. Escala cinza + CLAHE: {pred3:.4f} ({pred3*100:.1f}%)")
    
    # Método 4: Normalização robusta
    img4 = cv2.resize(cropped, (128, 128))
    img4 = img4.astype(np.float32)
    
    # Normalização por canal
    for i in range(3):
        channel = img4[:, :, i]
        mean = np.mean(channel)
        std = np.std(channel)
        if std > 0:
            img4[:, :, i] = (channel - mean) / std
    
    # Normalizar para 0-1
    img4 = (img4 - img4.min()) / (img4.max() - img4.min())
    img4 = np.expand_dims(img4, axis=0)
    
    pred4 = model.predict(img4, verbose=0)[0][0]
    print(f"4. Normalização robusta: {pred4:.4f} ({pred4*100:.1f}%)")
    
    # Método 5: Imagem completamente normalizada (ruído)
    noise_img = np.random.normal(0.5, 0.1, (1, 128, 128, 3))
    noise_img = np.clip(noise_img, 0, 1)
    
    pred5 = model.predict(noise_img, verbose=0)[0][0]
    print(f"5. Imagem de ruído: {pred5:.4f} ({pred5*100:.1f}%)")
    
    print(f"\n🎯 ANÁLISE:")
    print(f"   - Se todos os métodos dão alta probabilidade, o modelo está com viés")
    print(f"   - Se apenas alguns dão alta, o problema é no pré-processamento")
    print(f"   - Imagem de ruído deve dar ~50% (modelo neutro)")

def check_model_bias():
    """Verifica se o modelo tem viés"""
    print("\n🔍 VERIFICANDO VIÉS DO MODELO:")
    
    # Testar com imagens completamente aleatórias
    model_path = "models/brain_cancer_corrected.h5"
    
    if not os.path.exists(model_path):
        print("❌ Modelo não encontrado!")
        return
    
    model = load_model(model_path)
    
    predictions = []
    
    # Testar 10 imagens aleatórias
    for i in range(10):
        random_img = np.random.randint(0, 255, (1, 128, 128, 3), dtype=np.float32) / 255.0
        pred = model.predict(random_img, verbose=0)[0][0]
        predictions.append(pred)
        print(f"   Imagem {i+1}: {pred:.4f} ({pred*100:.1f}%)")
    
    avg_pred = np.mean(predictions)
    print(f"\n📊 Média das predições aleatórias: {avg_pred:.4f} ({avg_pred*100:.1f}%)")
    
    if avg_pred > 0.7:
        print("🚨 PROBLEMA: Modelo tem viés forte para 'tumor'!")
        print("   - Possível overfitting")
        print("   - Dados de treino desbalanceados")
        print("   - Modelo não generaliza bem")
    elif avg_pred < 0.3:
        print("🚨 PROBLEMA: Modelo tem viés forte para 'normal'!")
    else:
        print("✅ Modelo parece neutro para imagens aleatórias")

def suggest_fixes():
    """Sugere correções para o problema"""
    print("\n💡 SUGESTÕES DE CORREÇÃO:")
    print("=" * 50)
    
    print("1. 🎯 AJUSTE DE LIMIAR:")
    print("   - Use limiar mais alto (0.8-0.9) para ser mais conservador")
    print("   - Ou use limiar adaptativo baseado na confiança")
    
    print("\n2. 🔧 RETREINAMENTO:")
    print("   - Verificar se dados de treino estão balanceados")
    print("   - Usar validação cruzada")
    print("   - Adicionar regularização (dropout, weight decay)")
    
    print("\n3. 📊 PRÉ-PROCESSAMENTO:")
    print("   - Implementar detecção de artefatos")
    print("   - Usar normalização mais robusta")
    print("   - Adicionar validação de qualidade da imagem")
    
    print("\n4. 🧪 VALIDAÇÃO:")
    print("   - Testar com dataset independente")
    print("   - Calcular métricas de precisão/recall")
    print("   - Analisar matriz de confusão")

if __name__ == "__main__":
    load_and_test_model()
    check_model_bias()
    suggest_fixes()


