"""
Script para investigar a estrutura do dataset e identificar o problema
"""
import os

def investigate_brain_cancer_dataset():
    """Investiga a estrutura do dataset de câncer cerebral"""
    
    dataset_path = "datasets/brain_cancer"
    
    print("🔍 INVESTIGANDO DATASET DE CÂNCER CEREBRAL")
    print("=" * 50)
    
    if not os.path.exists(dataset_path):
        print("❌ Dataset não encontrado!")
        return
    
    # Explorar estrutura de diretórios
    print("📁 Estrutura de diretórios:")
    
    for root, dirs, files in os.walk(dataset_path):
        level = root.replace(dataset_path, '').count(os.sep)
        indent = ' ' * 2 * level
        
        folder_name = os.path.basename(root)
        if folder_name == 'brain_cancer':
            folder_name = 'brain_cancer (raiz)'
        
        # Contar arquivos de imagem
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        print(f"{indent}📂 {folder_name}/")
        if image_files:
            print(f"{indent}   🖼️ {len(image_files)} imagens")
            
            # Mostrar alguns exemplos de nomes
            if len(image_files) <= 5:
                for img in image_files[:3]:
                    print(f"{indent}      - {img}")
            else:
                for img in image_files[:2]:
                    print(f"{indent}      - {img}")
                print(f"{indent}      - ... e mais {len(image_files)-2}")
        
        # Parar após 3 níveis para não travar
        if level >= 2:
            continue
    
    print("\n🏷️ ANÁLISE DE LABELS:")
    print("-" * 30)
    
    # Analisar estrutura para determinar labels
    categories = {}
    
    for root, dirs, files in os.walk(dataset_path):
        folder_name = os.path.basename(root).lower()
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if image_files:
            # Classificar baseado no nome da pasta
            if any(word in folder_name for word in ['tumor', 'yes', 'positive', 'glioma', 'meningioma']):
                label = "TUMOR"
            elif any(word in folder_name for word in ['no', 'normal', 'negative', 'notumor']):
                label = "NORMAL"
            else:
                label = f"DESCONHECIDO ({folder_name})"
            
            if label not in categories:
                categories[label] = 0
            categories[label] += len(image_files)
    
    # Mostrar distribuição
    for category, count in categories.items():
        print(f"   {category}: {count} imagens")
    
    total_images = sum(categories.values())
    print(f"\n📊 TOTAL: {total_images} imagens")
    
    # Verificar balanceamento
    if len(categories) >= 2:
        values = list(categories.values())
        ratio = max(values) / min(values) if min(values) > 0 else float('inf')
        print(f"📈 Razão de desbalanceamento: {ratio:.1f}:1")
        
        if ratio > 3:
            print("⚠️ Dataset muito desbalanceado!")
        else:
            print("✅ Dataset relativamente balanceado")

def main():
    investigate_brain_cancer_dataset()

if __name__ == "__main__":
    main()