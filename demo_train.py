"""
Treinamento de demonstração rápido - versão otimizada
"""
import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

def load_sample_images(dataset_path, max_images=200):
    """Carrega apenas uma amostra pequena de imagens para teste rápido"""
    
    print(f"📁 Carregando amostra de {max_images} imagens de {dataset_path}...")
    
    images = []
    labels = []
    count = 0
    
    # Procurar imagens recursivamente
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if count >= max_images:
                break
                
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(root, file)
                
                try:
                    # Carregar e redimensionar imagem
                    img = cv2.imread(img_path)
                    if img is not None:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, (128, 128))  # Tamanho menor para teste
                        img = img.astype(np.float32) / 255.0
                        
                        images.append(img)
                        
                        # Label baseado no diretório/nome do arquivo
                        if any(word in root.lower() for word in ['tumor', 'yes', 'positive', 'malignant']):
                            labels.append(1)  # Tumor
                        else:
                            labels.append(0)  # Normal
                        
                        count += 1
                        
                        if count % 50 == 0:
                            print(f"   Processadas: {count}/{max_images}")
                            
                except Exception as e:
                    continue
        
        if count >= max_images:
            break
    
    print(f"✅ Total carregado: {len(images)} imagens")
    return np.array(images), np.array(labels)

def create_simple_model(input_shape):
    """Cria modelo CNN simples para teste rápido"""
    
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D(2, 2),
        
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        
        Flatten(),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def main():
    """Função principal para demo rápido"""
    
    print("🚀 TREINAMENTO DE DEMONSTRAÇÃO RÁPIDO")
    print("=" * 50)
    
    # Verificar se existe dataset
    dataset_path = "datasets/brain_cancer"
    
    if not os.path.exists(dataset_path):
        print("❌ Dataset não encontrado!")
        return
    
    try:
        # Carregar amostra pequena
        X, y = load_sample_images(dataset_path, max_images=200)
        
        if len(X) == 0:
            print("❌ Nenhuma imagem carregada!")
            return
        
        print(f"📊 Distribuição das classes: {np.bincount(y)}")
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"📋 Treino: {len(X_train)} | Teste: {len(X_test)}")
        
        # Criar modelo simples
        model = create_simple_model(X_train.shape[1:])
        
        print(f"🧠 Modelo criado com {model.count_params():,} parâmetros")
        
        # Treinamento rápido
        print("\n🏃 Iniciando treinamento rápido (3 épocas)...")
        
        history = model.fit(
            X_train, y_train,
            epochs=3,  # Apenas 3 épocas para teste
            batch_size=16,  # Batch pequeno
            validation_data=(X_test, y_test),
            verbose=1
        )
        
        # Avaliar modelo
        test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
        
        print(f"\n📊 RESULTADOS:")
        print(f"   Acurácia no teste: {test_acc:.2%}")
        print(f"   Loss no teste: {test_loss:.4f}")
        
        # Salvar modelo
        os.makedirs('models', exist_ok=True)
        model.save('models/demo_brain_cancer_model.h5')
        print(f"💾 Modelo salvo: models/demo_brain_cancer_model.h5")
        
        # Plotar histórico se possível
        try:
            plt.figure(figsize=(12, 4))
            
            plt.subplot(1, 2, 1)
            plt.plot(history.history['accuracy'], label='Treino')
            plt.plot(history.history['val_accuracy'], label='Validação')
            plt.title('Acurácia')
            plt.legend()
            
            plt.subplot(1, 2, 2)
            plt.plot(history.history['loss'], label='Treino')
            plt.plot(history.history['val_loss'], label='Validação')
            plt.title('Loss')
            plt.legend()
            
            plt.tight_layout()
            plt.savefig('results/demo_training_history.png')
            print(f"📈 Gráficos salvos: results/demo_training_history.png")
            
        except Exception as e:
            print(f"⚠️ Erro ao salvar gráficos: {e}")
        
        print("\n🎉 Demonstração concluída com sucesso!")
        print("\n📋 Próximos passos:")
        print("1. Teste predições: python src/predict.py")
        print("2. Treinamento completo: python src/train_model.py")
        
    except Exception as e:
        print(f"❌ Erro durante treinamento: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()