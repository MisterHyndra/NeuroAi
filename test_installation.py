"""
Teste para verificar se todas as dependências estão instaladas corretamente
"""
import sys

def test_imports():
    """Testa importação de todas as bibliotecas necessárias"""
    
    print("🧪 Testando importações...")
    
    tests = [
        ("TensorFlow", "import tensorflow as tf; print(f'   TensorFlow {tf.__version__}')"),
        ("OpenCV", "import cv2; print(f'   OpenCV {cv2.__version__}')"),
        ("NumPy", "import numpy as np; print(f'   NumPy {np.__version__}')"),
        ("Pandas", "import pandas as pd; print(f'   Pandas {pd.__version__}')"),
        ("Matplotlib", "import matplotlib; print(f'   Matplotlib {matplotlib.__version__}')"),
        ("Scikit-learn", "import sklearn; print(f'   Scikit-learn {sklearn.__version__}')"),
        ("Seaborn", "import seaborn as sns; print(f'   Seaborn {sns.__version__}')"),
        ("PIL", "from PIL import Image; print('   PIL/Pillow OK')"),
    ]
    
    failed = []
    
    for name, test_code in tests:
        try:
            exec(test_code)
        except ImportError as e:
            print(f"   ❌ {name}: {e}")
            failed.append(name)
        except Exception as e:
            print(f"   ⚠️ {name}: {e}")
    
    if not failed:
        print("\n✅ Todas as bibliotecas foram importadas com sucesso!")
        return True
    else:
        print(f"\n❌ Falha ao importar: {', '.join(failed)}")
        return False

def test_tensorflow_gpu():
    """Testa se TensorFlow pode usar GPU"""
    try:
        import tensorflow as tf
        
        print("\n🖥️ Testando suporte a GPU...")
        
        # Verificar dispositivos disponíveis
        devices = tf.config.list_physical_devices()
        print(f"   Dispositivos físicos: {len(devices)}")
        
        for device in devices:
            print(f"   - {device}")
        
        # Verificar GPUs
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"   🎯 {len(gpus)} GPU(s) detectada(s)!")
        else:
            print("   💻 Nenhuma GPU detectada - usando CPU")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao testar GPU: {e}")
        return False

def test_basic_model():
    """Testa criação de um modelo simples"""
    try:
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense
        
        print("\n🧠 Testando criação de modelo básico...")
        
        # Criar modelo simples
        model = Sequential([
            Dense(10, activation='relu', input_shape=(5,)),
            Dense(1, activation='sigmoid')
        ])
        
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        
        print(f"   ✅ Modelo criado com {model.count_params()} parâmetros")
        
        # Testar com dados sintéticos
        import numpy as np
        X_test = np.random.rand(10, 5)
        y_pred = model.predict(X_test, verbose=0)
        
        print(f"   ✅ Predição bem-sucedida: shape {y_pred.shape}")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao criar modelo: {e}")
        return False

def test_opencv():
    """Testa funcionalidades básicas do OpenCV"""
    try:
        import cv2
        import numpy as np
        
        print("\n📸 Testando OpenCV...")
        
        # Criar imagem sintética
        img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        # Redimensionar
        resized = cv2.resize(img, (50, 50))
        print(f"   ✅ Redimensionamento: {img.shape} -> {resized.shape}")
        
        # Conversão de cores
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print(f"   ✅ Conversão para cinza: {gray.shape}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro no OpenCV: {e}")
        return False

def main():
    """Função principal de teste"""
    
    print("🔬 TESTE DE INSTALAÇÃO - Sistema de Diagnóstico de Câncer")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Teste 1: Importações
    if not test_imports():
        all_tests_passed = False
    
    # Teste 2: TensorFlow GPU
    if not test_tensorflow_gpu():
        all_tests_passed = False
    
    # Teste 3: Modelo básico
    if not test_basic_model():
        all_tests_passed = False
    
    # Teste 4: OpenCV
    if not test_opencv():
        all_tests_passed = False
    
    print("\n" + "="*60)
    
    if all_tests_passed:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema pronto para uso")
        print("\n📋 Próximos passos:")
        print("1. Configure sua API do Kaggle")
        print("2. Execute: python src/data_downloader.py")
        print("3. Execute: python src/train_model.py")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("🔧 Verifique as instalações das bibliotecas")
    
    print("\n💡 Para começar rapidamente, execute:")
    print("   python quick_start.py")

if __name__ == "__main__":
    main()