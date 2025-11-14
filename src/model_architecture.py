"""
Arquiteturas de modelos CNN para diagnóstico de câncer multi-classe
"""
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import (
    Conv2D, MaxPooling2D, Flatten, Dense, Dropout, 
    BatchNormalization, GlobalAveragePooling2D, Input
)
from tensorflow.keras.applications import (
    VGG16, ResNet50, InceptionV3, EfficientNetB0
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import (
    EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
)
import matplotlib.pyplot as plt

class CancerCNNModels:
    def __init__(self, input_shape=(224, 224, 3), num_classes=2):
        self.input_shape = input_shape
        self.num_classes = num_classes
        
    def create_basic_cnn(self):
        """
        Cria uma CNN básica para diagnóstico de câncer
        """
        model = Sequential([
            # Primeira camada convolucional
            Conv2D(32, (3, 3), activation='relu', input_shape=self.input_shape),
            BatchNormalization(),
            MaxPooling2D(2, 2),
            
            # Segunda camada convolucional
            Conv2D(64, (3, 3), activation='relu'),
            BatchNormalization(),
            MaxPooling2D(2, 2),
            
            # Terceira camada convolucional
            Conv2D(128, (3, 3), activation='relu'),
            BatchNormalization(),
            MaxPooling2D(2, 2),
            
            # Quarta camada convolucional
            Conv2D(256, (3, 3), activation='relu'),
            BatchNormalization(),
            MaxPooling2D(2, 2),
            
            # Camadas densas
            Flatten(),
            Dense(512, activation='relu'),
            Dropout(0.5),
            Dense(256, activation='relu'),
            Dropout(0.3),
            Dense(self.num_classes, activation='softmax' if self.num_classes > 2 else 'sigmoid')
        ])
        
        return model
    
    def create_advanced_cnn(self):
        """
        Cria uma CNN mais avançada com mais camadas
        """
        model = Sequential([
            # Bloco 1
            Conv2D(64, (3, 3), activation='relu', padding='same', input_shape=self.input_shape),
            Conv2D(64, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D(2, 2),
            Dropout(0.25),
            
            # Bloco 2  
            Conv2D(128, (3, 3), activation='relu', padding='same'),
            Conv2D(128, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D(2, 2),
            Dropout(0.25),
            
            # Bloco 3
            Conv2D(256, (3, 3), activation='relu', padding='same'),
            Conv2D(256, (3, 3), activation='relu', padding='same'),
            Conv2D(256, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D(2, 2),
            Dropout(0.25),
            
            # Bloco 4
            Conv2D(512, (3, 3), activation='relu', padding='same'),
            Conv2D(512, (3, 3), activation='relu', padding='same'),
            Conv2D(512, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D(2, 2),
            Dropout(0.25),
            
            # Classificação
            GlobalAveragePooling2D(),
            Dense(1024, activation='relu'),
            Dropout(0.5),
            Dense(512, activation='relu'),
            Dropout(0.3),
            Dense(self.num_classes, activation='softmax' if self.num_classes > 2 else 'sigmoid')
        ])
        
        return model
    
    def create_transfer_learning_model(self, base_model_name='vgg16', trainable_layers=0):
        """
        Cria modelo usando transfer learning
        
        Args:
            base_model_name: Nome do modelo base ('vgg16', 'resnet50', 'inception', 'efficientnet')
            trainable_layers: Número de camadas finais para treinar (0 = todas congeladas)
        """
        
        # Selecionar modelo base
        if base_model_name.lower() == 'vgg16':
            base_model = VGG16(
                weights='imagenet',
                include_top=False,
                input_shape=self.input_shape
            )
        elif base_model_name.lower() == 'resnet50':
            base_model = ResNet50(
                weights='imagenet',
                include_top=False,
                input_shape=self.input_shape
            )
        elif base_model_name.lower() == 'inception':
            base_model = InceptionV3(
                weights='imagenet',
                include_top=False,
                input_shape=self.input_shape
            )
        elif base_model_name.lower() == 'efficientnet':
            base_model = EfficientNetB0(
                weights='imagenet',
                include_top=False,
                input_shape=self.input_shape
            )
        else:
            raise ValueError(f"Modelo base não suportado: {base_model_name}")
        
        # Congelar camadas do modelo base
        if trainable_layers == 0:
            base_model.trainable = False
        else:
            # Congelar todas exceto as últimas N camadas
            for layer in base_model.layers[:-trainable_layers]:
                layer.trainable = False
        
        # Adicionar camadas de classificação
        model = Sequential([
            base_model,
            GlobalAveragePooling2D(),
            Dense(512, activation='relu'),
            Dropout(0.5),
            Dense(256, activation='relu'),
            Dropout(0.3),
            Dense(self.num_classes, activation='softmax' if self.num_classes > 2 else 'sigmoid')
        ])
        
        return model
    
    def create_multi_cancer_classifier(self):
        """
        Cria um modelo para classificar múltiplos tipos de câncer
        """
        # Entrada
        inputs = Input(shape=self.input_shape)
        
        # Feature extraction backbone
        x = Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
        x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
        x = BatchNormalization()(x)
        x = MaxPooling2D(2, 2)(x)
        x = Dropout(0.25)(x)
        
        x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
        x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
        x = BatchNormalization()(x)
        x = MaxPooling2D(2, 2)(x)
        x = Dropout(0.25)(x)
        
        x = Conv2D(256, (3, 3), activation='relu', padding='same')(x)
        x = Conv2D(256, (3, 3), activation='relu', padding='same')(x)
        x = BatchNormalization()(x)
        x = MaxPooling2D(2, 2)(x)
        x = Dropout(0.25)(x)
        
        x = Conv2D(512, (3, 3), activation='relu', padding='same')(x)
        x = Conv2D(512, (3, 3), activation='relu', padding='same')(x)
        x = BatchNormalization()(x)
        x = MaxPooling2D(2, 2)(x)
        x = Dropout(0.25)(x)
        
        # Global pooling
        x = GlobalAveragePooling2D()(x)
        
        # Shared dense layers
        x = Dense(1024, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.3)(x)
        
        # Cabeças de classificação específicas para cada tipo de câncer
        breast_output = Dense(2, activation='softmax', name='breast_cancer')(x)
        skin_output = Dense(2, activation='softmax', name='skin_cancer')(x)
        lung_output = Dense(2, activation='softmax', name='lung_cancer')(x)
        brain_output = Dense(2, activation='softmax', name='brain_cancer')(x)
        
        # Criar modelo
        model = Model(
            inputs=inputs,
            outputs=[breast_output, skin_output, lung_output, brain_output]
        )
        
        return model
    
    def compile_model(self, model, learning_rate=0.001, loss_function=None):
        """
        Compila o modelo com otimizador e função de perda
        """
        
        # Definir função de perda baseada no número de classes
        if loss_function is None:
            if self.num_classes == 2:
                loss = 'binary_crossentropy'
                metrics = ['accuracy', 'precision', 'recall']
            else:
                loss = 'categorical_crossentropy' 
                metrics = ['accuracy']
        else:
            loss = loss_function
            metrics = ['accuracy']
        
        # Compilar modelo
        model.compile(
            optimizer=Adam(learning_rate=learning_rate),
            loss=loss,
            metrics=metrics
        )
        
        return model
    
    def get_callbacks(self, model_name='cancer_model'):
        """
        Cria callbacks para treinamento
        """
        callbacks = [
            # Early stopping
            EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            
            # Reduzir learning rate quando não houver melhora
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.2,
                patience=5,
                min_lr=1e-7,
                verbose=1
            ),
            
            # Salvar melhor modelo
            ModelCheckpoint(
                filepath=f'models/{model_name}_best.h5',
                monitor='val_loss',
                save_best_only=True,
                verbose=1
            )
        ]
        
        return callbacks
    
    def plot_model_architecture(self, model, filename='model_architecture'):
        """
        Plota a arquitetura do modelo
        """
        try:
            tf.keras.utils.plot_model(
                model,
                to_file=f'results/{filename}.png',
                show_shapes=True,
                show_layer_names=True,
                rankdir='TB'
            )
            print(f"✅ Arquitetura do modelo salva em 'results/{filename}.png'")
        except Exception as e:
            print(f"❌ Erro ao plotar arquitetura: {e}")

def test_models():
    """Função para testar a criação dos modelos"""
    
    print("🧠 Testando arquiteturas de modelos CNN...")
    
    # Criar instância da classe
    cnn_models = CancerCNNModels(input_shape=(224, 224, 3), num_classes=2)
    
    # Testar modelo básico
    print("\n1️⃣ Criando modelo CNN básico...")
    basic_model = cnn_models.create_basic_cnn()
    basic_model = cnn_models.compile_model(basic_model)
    print(f"   Parâmetros: {basic_model.count_params():,}")
    
    # Testar modelo avançado
    print("\n2️⃣ Criando modelo CNN avançado...")
    advanced_model = cnn_models.create_advanced_cnn()
    advanced_model = cnn_models.compile_model(advanced_model)
    print(f"   Parâmetros: {advanced_model.count_params():,}")
    
    # Testar transfer learning
    print("\n3️⃣ Criando modelo com transfer learning (VGG16)...")
    try:
        transfer_model = cnn_models.create_transfer_learning_model('vgg16')
        transfer_model = cnn_models.compile_model(transfer_model)
        print(f"   Parâmetros: {transfer_model.count_params():,}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Salvar resumos dos modelos
    with open('results/model_summaries.txt', 'w') as f:
        f.write("RESUMO DOS MODELOS CNN\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("1. MODELO BÁSICO\n")
        f.write("-" * 20 + "\n")
        basic_model.summary(print_fn=lambda x: f.write(x + '\n'))
        
        f.write("\n\n2. MODELO AVANÇADO\n")
        f.write("-" * 20 + "\n")
        advanced_model.summary(print_fn=lambda x: f.write(x + '\n'))
    
    print("\n✅ Todos os modelos criados com sucesso!")
    print("📄 Resumos salvos em 'results/model_summaries.txt'")

if __name__ == "__main__":
    test_models()