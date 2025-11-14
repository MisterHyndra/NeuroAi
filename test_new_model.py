"""
Teste rápido do novo modelo balanceado
"""
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

def test_model_with_image(image_path):
    """Testa modelo com uma imagem específica"""
    
    model_path = "models/brain_cancer_balanced.h5"
    
    if not os.path.exists(model_path):
        print("❌ Modelo balanceado não encontrado!")
        return
    
    if not os.path.exists(image_path):
        print(f"❌ Imagem não encontrada: {image_path}")
        return
    
    print(f"🧪 TESTANDO NOVO MODELO BALANCEADO")
    print("=" * 50)
    
    # Carregar modelo
    model = load_model(model_path)
    print(f"✅ Modelo carregado: {model_path}")
    
    # Carregar imagem
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print(f"📐 Dimensões da imagem: {img.shape}")
    
    # Pré-processar (método melhorado)
    h, w = img.shape[:2]
    margin_h = int(h * 0.10)
    margin_w = int(w * 0.10)
    cropped = img[margin_h:h-margin_h, margin_w:w-margin_w]
    
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
    img_rgb = np.stack([gray, gray, gray], axis=-1)
    img_resized = cv2.resize(img_rgb, (128, 128))
    img_processed = np.expand_dims(img_resized, axis=0)
    
    # Fazer predição
    prediction = model.predict(img_processed, verbose=0)[0][0]
    
    print(f"\n📊 RESULTADO:")
    print(f"   Probabilidade de tumor: {prediction:.4f} ({prediction*100:.1f}%)")
    
    # Testar diferentes limiares
    thresholds = [0.5, 0.6, 0.7, 0.75, 0.8, 0.9]
    print(f"\n🎯 TESTE DE LIMIARES:")
    for threshold in thresholds:
        is_tumor = prediction > threshold
        result = "TUMOR" if is_tumor else "NORMAL"
        confidence = prediction if is_tumor else 1 - prediction
        print(f"   Limiar {threshold:.2f}: {result} (confiança: {confidence:.1%})")
    
    # Recomendação
    print(f"\n💡 RECOMENDAÇÃO:")
    if prediction < 0.3:
        print("   ✅ Imagem provavelmente NORMAL")
        print("   📋 Use limiar 0.5-0.6 para ser mais sensível")
    elif prediction > 0.7:
        print("   ⚠️ Imagem suspeita de TUMOR")
        print("   📋 Use limiar 0.7-0.8 para confirmar")
    else:
        print("   ❓ Resultado incerto")
        print("   📋 Use limiar 0.75+ para ser conservador")
    
    # Testar com ruído para verificar viés
    print(f"\n🔍 TESTE DE VIÉS:")
    noise_img = np.random.random((1, 128, 128, 3))
    noise_pred = model.predict(noise_img, verbose=0)[0][0]
    print(f"   Ruído aleatório: {noise_pred:.4f} ({noise_pred*100:.1f}%)")
    
    if noise_pred < 0.1:
        print("   ✅ Modelo neutro (sem viés)")
    else:
        print("   ⚠️ Modelo ainda tem algum viés")

if __name__ == "__main__":
    # Testar com a imagem que estava dando problema
    test_image = "deep.jpg"
    
    if os.path.exists(test_image):
        test_model_with_image(test_image)
    else:
        print(f"❌ Imagem de teste não encontrada: {test_image}")
        print("📝 Coloque uma imagem de teste no diretório atual")


