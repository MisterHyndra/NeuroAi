"""
Teste do modelo balanceado com limiar ajustado
"""
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import random

def preprocess_image(img):
    """Pré-processa imagem igual ao modelo"""
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
    return img_processed

def test_category(model, category_path, category_name, expected_label, threshold=0.4, num_samples=5):
    """Testa uma categoria específica"""
    print(f"\n🧪 TESTANDO {category_name.upper()} (limiar {threshold}):")
    print("=" * 50)
    
    if not os.path.exists(category_path):
        print(f"❌ Caminho não encontrado: {category_path}")
        return
    
    # Listar arquivos
    files = [f for f in os.listdir(category_path) 
             if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if len(files) == 0:
        print(f"❌ Nenhuma imagem encontrada em {category_path}")
        return
    
    # Selecionar amostras aleatórias
    sample_files = random.sample(files, min(num_samples, len(files)))
    
    predictions = []
    correct_predictions = 0
    
    for i, filename in enumerate(sample_files):
        img_path = os.path.join(category_path, filename)
        
        try:
            # Carregar imagem
            img = cv2.imread(img_path)
            if img is None:
                continue
                
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Pré-processar
            img_processed = preprocess_image(img)
            
            # Fazer predição
            prediction = model.predict(img_processed, verbose=0)[0][0]
            predictions.append(prediction)
            
            # Classificar com limiar ajustado
            is_tumor = prediction > threshold
            predicted_label = 1 if is_tumor else 0
            
            # Verificar se está correto
            is_correct = predicted_label == expected_label
            if is_correct:
                correct_predictions += 1
            
            status = "✅" if is_correct else "❌"
            result = "TUMOR" if is_tumor else "NORMAL"
            expected = "TUMOR" if expected_label == 1 else "NORMAL"
            
            print(f"   {status} {filename[:20]:<20} | Pred: {result} ({prediction:.3f}) | Esperado: {expected}")
            
        except Exception as e:
            print(f"   ❌ Erro ao processar {filename}: {e}")
    
    # Estatísticas da categoria
    if predictions:
        avg_pred = np.mean(predictions)
        accuracy = correct_predictions / len(predictions)
        
        print(f"\n📊 ESTATÍSTICAS {category_name.upper()}:")
        print(f"   Amostras testadas: {len(predictions)}")
        print(f"   Predições corretas: {correct_predictions}")
        print(f"   Acurácia: {accuracy:.1%}")
        print(f"   Probabilidade média: {avg_pred:.3f}")
        
        # Análise
        if expected_label == 0:  # Normal
            if avg_pred < threshold:
                print(f"   ✅ Modelo está correto (baixa probabilidade de tumor)")
            else:
                print(f"   ⚠️ Modelo pode estar com viés (alta probabilidade mesmo para normal)")
        else:  # Tumor
            if avg_pred > threshold:
                print(f"   ✅ Modelo está correto (alta probabilidade de tumor)")
            else:
                print(f"   ⚠️ Modelo pode estar sub-detectando tumores")
    
    return predictions, correct_predictions, len(predictions)

def main():
    """Função principal para testar o modelo"""
    
    print("🔍 TESTE COM LIMIAR AJUSTADO (0.4)")
    print("=" * 60)
    
    # Carregar modelo
    model_path = "models/brain_cancer_balanced.h5"
    
    if not os.path.exists(model_path):
        print("❌ Modelo balanceado não encontrado!")
        return
    
    model = load_model(model_path)
    print(f"✅ Modelo carregado: {model_path}")
    
    # Definir categorias para teste
    test_categories = [
        ("datasets/brain_cancer/Testing/notumor", "NORMAL", 0),
        ("datasets/brain_cancer/Testing/glioma", "GLIOMA", 1),
        ("datasets/brain_cancer/Testing/meningioma", "MENINGIOMA", 1),
        ("datasets/brain_cancer/Testing/pituitary", "PITUITÁRIO", 1),
    ]
    
    total_correct = 0
    total_samples = 0
    all_predictions = []
    
    # Testar cada categoria
    for category_path, category_name, expected_label in test_categories:
        predictions, correct, samples = test_category(
            model, category_path, category_name, expected_label, threshold=0.4, num_samples=10
        )
        
        total_correct += correct
        total_samples += samples
        all_predictions.extend(predictions)
    
    # Resultado geral
    print(f"\n🎯 RESULTADO GERAL:")
    print("=" * 50)
    print(f"Total de amostras testadas: {total_samples}")
    print(f"Predições corretas: {total_correct}")
    print(f"Acurácia geral: {total_correct/total_samples:.1%}")
    
    if all_predictions:
        print(f"Probabilidade média geral: {np.mean(all_predictions):.3f}")
        print(f"Desvio padrão: {np.std(all_predictions):.3f}")
    
    # Análise final
    print(f"\n💡 ANÁLISE FINAL:")
    if total_correct/total_samples > 0.8:
        print("✅ Modelo está funcionando bem!")
    elif total_correct/total_samples > 0.6:
        print("⚠️ Modelo está funcionando, mas pode melhorar")
    else:
        print("❌ Modelo precisa de ajustes")
    
    # Teste de viés
    print(f"\n🔍 TESTE DE VIÉS:")
    noise_img = np.random.random((1, 128, 128, 3))
    noise_pred = model.predict(noise_img, verbose=0)[0][0]
    print(f"Ruído aleatório: {noise_pred:.4f} ({noise_pred*100:.1f}%)")
    
    if 0.1 < noise_pred < 0.9:
        print("✅ Modelo neutro (sem viés)")
    else:
        print("⚠️ Modelo ainda tem viés")

if __name__ == "__main__":
    # Definir seed para reprodutibilidade
    random.seed(42)
    np.random.seed(42)
    
    main()





