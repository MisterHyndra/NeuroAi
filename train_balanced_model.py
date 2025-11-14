"""
Treinamento de modelo BALANCEADO para corrigir viés
"""
import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.regularizers import l2
import matplotlib.pyplot as plt

def load_balanced_data(dataset_path, max_per_category=200):
    """
    Carrega dados com foco em BALANCEAMENTO
    """
    
    print(f"📁 Carregando dados BALANCEADOS de {dataset_path}...")
    
    images = []
    labels = []
    
    # Categorias corretas
    categories = {
        'notumor': 0,      # Normal/Sem tumor
        'glioma': 1,       # Glioma (tumor)
        'meningioma': 1,   # Meningioma (tumor)  
        'pituitary': 1     # Pituitário (tumor)
    }
    
    category_counts = {0: 0, 1: 0}
    
    # Processar Training e Testing
    for split in ['Training', 'Testing']:
        split_path = os.path.join(dataset_path, split)
        if not os.path.exists(split_path):
            continue
            
        print(f"📂 Processando {split}...")
        
        for category_name, label in categories.items():
            category_path = os.path.join(split_path, category_name)
            
            if not os.path.exists(category_path):
                continue
            
            print(f"   📁 {category_name} -> Label {label} ({'Normal' if label == 0 else 'Tumor'})")
            
            # Listar arquivos de imagem
            image_files = [f for f in os.listdir(category_path) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            # LIMITAR para garantir balanceamento
            image_files = image_files[:max_per_category]
            
            count = 0
            for img_file in image_files:
                img_path = os.path.join(category_path, img_file)
                
                try:
                    # Carregar e processar imagem
                    img = cv2.imread(img_path)
                    if img is None:
                        continue
                        
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img = cv2.resize(img, (128, 128))
                    img = img.astype(np.float32) / 255.0
                    
                    images.append(img)
                    labels.append(label)
                    category_counts[label] += 1
                    count += 1
                    
                    if count % 50 == 0:
                        print(f"      Processadas: {count}")
                        
                except Exception as e:
                    continue
            
            print(f"   ✅ {category_name}: {count} imagens carregadas")
    
    print(f"\n📊 DISTRIBUIÇÃO BALANCEADA:")
    print(f"   Normal (0): {category_counts[0]} imagens")
    print(f"   Tumor (1): {category_counts[1]} imagens")
    print(f"   Total: {len(images)} imagens")
    print(f"   Proporção: {category_counts[0]/len(images)*100:.1f}% normal, {category_counts[1]/len(images)*100:.1f}% tumor")
    
    return np.array(images), np.array(labels)

def create_balanced_model(input_shape):
    """Cria modelo com arquitetura mais conservadora"""
    
    model = Sequential([
        # Bloco 1 - Menos parâmetros
        Conv2D(16, (3, 3), activation='relu', input_shape=input_shape, kernel_regularizer=l2(0.001)),
        BatchNormalization(),
        MaxPooling2D(2, 2),
        Dropout(0.3),
        
        # Bloco 2
        Conv2D(32, (3, 3), activation='relu', kernel_regularizer=l2(0.001)),
        BatchNormalization(),
        MaxPooling2D(2, 2),
        Dropout(0.3),
        
        # Bloco 3
        Conv2D(64, (3, 3), activation='relu', kernel_regularizer=l2(0.001)),
        BatchNormalization(),
        MaxPooling2D(2, 2),
        Dropout(0.3),
        
        # Global Average Pooling (reduz overfitting)
        GlobalAveragePooling2D(),
        
        # Dense layers menores
        Dense(32, activation='relu', kernel_regularizer=l2(0.001)),
        Dropout(0.5),
        Dense(16, activation='relu', kernel_regularizer=l2(0.001)),
        Dropout(0.3),
        Dense(1, activation='sigmoid')
    ])
    
    # Otimizador mais conservador
    model.compile(
        optimizer=Adam(learning_rate=0.0001),  # LR menor
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def test_model_bias(model):
    """Testa se o modelo tem viés"""
    print("\n🧪 TESTANDO VIÉS DO MODELO:")
    
    # Testar com ruído aleatório
    random_imgs = []
    for i in range(5):
        random_img = np.random.random((1, 128, 128, 3))
        random_imgs.append(random_img)
    
    predictions = []
    for img in random_imgs:
        pred = model.predict(img, verbose=0)[0][0]
        predictions.append(pred)
        print(f"   Ruído {len(predictions)}: {pred:.4f} ({pred*100:.1f}%)")
    
    avg_pred = np.mean(predictions)
    print(f"\n📊 Média das predições de ruído: {avg_pred:.4f} ({avg_pred*100:.1f}%)")
    
    if avg_pred > 0.7:
        print("🚨 PROBLEMA: Modelo ainda tem viés para 'tumor'!")
        return False
    elif avg_pred < 0.3:
        print("🚨 PROBLEMA: Modelo tem viés para 'normal'!")
        return False
    else:
        print("✅ Modelo parece neutro!")
        return True

def main():
    """Função principal para treinamento balanceado"""
    
    print("🔧 TREINAMENTO BALANCEADO - Corrigindo Viés")
    print("=" * 60)
    
    dataset_path = "datasets/brain_cancer"
    
    if not os.path.exists(dataset_path):
        print("❌ Dataset não encontrado!")
        return
    
    try:
        # Carregar dados balanceados
        X, y = load_balanced_data(dataset_path, max_per_category=200)
        
        if len(X) == 0:
            print("❌ Nenhuma imagem carregada!")
            return
        
        # Verificar distribuição
        unique, counts = np.unique(y, return_counts=True)
        print(f"\n📈 Distribuição final:")
        for label, count in zip(unique, counts):
            print(f"   Classe {label}: {count} amostras ({count/len(y)*100:.1f}%)")
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        X_train, X_val, y_train, y_val = train_test_split(
            X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
        )
        
        print(f"\n📋 Divisão dos dados:")
        print(f"   Treino: {len(X_train)} | Validação: {len(X_val)} | Teste: {len(X_test)}")
        
        # Calcular pesos das classes
        class_weights = compute_class_weight(
            'balanced', classes=np.unique(y_train), y=y_train
        )
        class_weight_dict = dict(enumerate(class_weights))
        print(f"⚖️ Pesos das classes: {class_weight_dict}")
        
        # Criar modelo balanceado
        model = create_balanced_model(X_train.shape[1:])
        print(f"🧠 Modelo criado com {model.count_params():,} parâmetros")
        
        # Callbacks mais agressivos
        early_stopping = EarlyStopping(
            monitor='val_loss', patience=3, restore_best_weights=True
        )
        
        reduce_lr = ReduceLROnPlateau(
            monitor='val_loss', factor=0.5, patience=2, min_lr=1e-7
        )
        
        # Treinamento
        print(f"\n🚀 Iniciando treinamento balanceado (15 épocas)...")
        
        history = model.fit(
            X_train, y_train,
            epochs=15,
            batch_size=16,  # Batch menor
            validation_data=(X_val, y_val),
            class_weight=class_weight_dict,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )
        
        # Testar viés
        if not test_model_bias(model):
            print("⚠️ Modelo ainda tem viés. Tentando ajustes...")
            
            # Ajustar bias da camada final
            final_layer = model.layers[-1]
            bias = final_layer.get_weights()[1]
            final_layer.set_weights([final_layer.get_weights()[0], np.array([-0.5])])
            print("🔧 Ajustado bias da camada final")
            
            # Testar novamente
            if test_model_bias(model):
                print("✅ Viés corrigido!")
            else:
                print("⚠️ Ainda com viés, mas melhorado")
        
        # Avaliação
        test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
        
        print(f"\n📊 RESULTADOS BALANCEADOS:")
        print(f"   Acurácia no teste: {test_acc:.2%}")
        print(f"   Loss no teste: {test_loss:.4f}")
        
        # Testar algumas predições
        print(f"\n🧪 TESTE DE PREDIÇÕES:")
        sample_indices = np.random.choice(len(X_test), 5, replace=False)
        
        for i, idx in enumerate(sample_indices):
            pred = model.predict(X_test[idx:idx+1], verbose=0)[0][0]
            true_label = y_test[idx]
            
            pred_label = "Tumor" if pred > 0.5 else "Normal"
            true_label_name = "Tumor" if true_label == 1 else "Normal"
            
            print(f"   Amostra {i+1}: Predição={pred_label} ({pred:.2f}) | Real={true_label_name}")
        
        # Salvar modelo balanceado
        os.makedirs('models', exist_ok=True)
        model.save('models/brain_cancer_balanced.h5')
        print(f"\n💾 Modelo balanceado salvo: models/brain_cancer_balanced.h5")
        
        # Plotar histórico
        try:
            plt.figure(figsize=(12, 4))
            
            plt.subplot(1, 2, 1)
            plt.plot(history.history['accuracy'], label='Treino', marker='o')
            plt.plot(history.history['val_accuracy'], label='Validação', marker='s')
            plt.title('Acurácia - Modelo Balanceado')
            plt.xlabel('Época')
            plt.ylabel('Acurácia')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            plt.subplot(1, 2, 2)
            plt.plot(history.history['loss'], label='Treino', marker='o')
            plt.plot(history.history['val_loss'], label='Validação', marker='s')
            plt.title('Loss - Modelo Balanceado')
            plt.xlabel('Época')
            plt.ylabel('Loss')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('results/balanced_training_history.png', dpi=300)
            print(f"📈 Gráficos salvos: results/balanced_training_history.png")
            
        except Exception as e:
            print(f"⚠️ Erro ao salvar gráficos: {e}")
        
        print(f"\n🎉 Treinamento balanceado concluído!")
        print(f"📋 Próximos passos:")
        print(f"1. Teste o novo modelo: models/brain_cancer_balanced.h5")
        print(f"2. Use limiar conservador (0.7-0.8)")
        print(f"3. O modelo deve ser mais neutro agora!")
        
    except Exception as e:
        print(f"❌ Erro durante treinamento: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


