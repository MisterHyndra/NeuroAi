"""
Servidor Flask para API local do NeuroAI
Permite usar o modelo .h5 treinado diretamente na web sem conversão
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import io
import os
import psycopg2
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
CORS(app)  # Permite requisições do navegador

# Configuração PostgreSQL
DB_CONFIG = {
    'host': 'localhost',
    'port': 5433,
    'database': 'neuroia',
    'user': 'postgres',
    'password': 'neuro'
}

def get_db_connection():
    """Cria conexão com PostgreSQL"""
    return psycopg2.connect(**DB_CONFIG)

# Carrega o modelo na inicialização
MODEL_PATH = 'models/brain_cancer_final.h5'
model = None

def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        print(f"Carregando modelo: {MODEL_PATH}")
        model = tf.keras.models.load_model(MODEL_PATH)
        print(f"Modelo carregado! Input shape: {model.input_shape}")
    else:
        print(f"⚠️ Modelo não encontrado: {MODEL_PATH}")
        print("Procurando outros modelos...")
        # Tenta outros modelos
        alternatives = [
            'models/brain_cancer_balanced.h5',
            'models/brain_cancer_corrected.h5',
            'models/demo_brain_cancer_model.h5'
        ]
        for alt in alternatives:
            if os.path.exists(alt):
                print(f"Usando modelo alternativo: {alt}")
                model = tf.keras.models.load_model(alt)
                break

def preprocess_image(image_bytes, target_size=(128, 128)):
    """Preprocessa imagem EXATAMENTE igual ao visual_diagnosis_modern.py"""
    # Abre imagem
    img = Image.open(io.BytesIO(image_bytes))
    
    # Converte para array numpy RGB
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img_array = np.array(img)
    
    # 1. Crop 10% das bordas (remove régua/legendas)
    h, w = img_array.shape[:2]
    margin_h = int(h * 0.10)
    margin_w = int(w * 0.10)
    cropped = img_array[margin_h:h - margin_h, margin_w:w - margin_w]
    
    # 2. Converte para grayscale
    if len(cropped.shape) == 3:
        gray = cv2.cvtColor(cropped, cv2.COLOR_RGB2GRAY)
    else:
        gray = cropped
    
    # 3. Aplica CLAHE (equalização adaptativa)
    try:
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
    except Exception:
        gray = cv2.equalizeHist(gray)
    
    # 4. Normaliza [0, 255] -> [0, 1]
    gray = gray.astype(np.float32) / 255.0
    
    # 5. Replica para 3 canais RGB (grayscale replicado)
    img_rgb = np.stack([gray, gray, gray], axis=-1)
    
    # 6. Resize para tamanho do modelo
    img_resized = cv2.resize(img_rgb, target_size)
    
    # 7. Adiciona batch dimension
    img_resized = np.expand_dims(img_resized, axis=0)
    
    return img_resized

@app.route('/api/health', methods=['GET'])
def health():
    """Verifica se o servidor está rodando"""
    return jsonify({
        'status': 'ok',
        'model_loaded': model is not None,
        'model_path': MODEL_PATH if model else None
    })

def create_activation_heatmap(tumor_prob, confidence):
    """Cria mapa de ativação simulado (igual ao desktop)"""
    import base64
    from io import BytesIO
    
    heatmap = np.zeros((128, 128))
    
    if tumor_prob > 0.35:  # Tumor detectado
        # Foco principal (região central-superior)
        center_x, center_y = 64, 45
        for i in range(128):
            for j in range(128):
                dist = np.sqrt((i - center_x)**2 + (j - center_y)**2)
                activation = max(0, confidence - dist / 50)
                heatmap[j, i] = activation
        
        # Foco secundário
        if confidence > 0.7:
            center_x2, center_y2 = 50, 70
            for i in range(128):
                for j in range(128):
                    dist = np.sqrt((i - center_x2)**2 + (j - center_y2)**2)
                    activation = max(0, confidence * 0.6 - dist / 60)
                    heatmap[j, i] = max(heatmap[j, i], activation)
    else:
        # Normal - ativação baixa e dispersa
        heatmap = np.random.rand(128, 128) * 0.2
    
    # Normaliza e converte para imagem
    heatmap = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min() + 1e-8)
    heatmap_colored = (plt.cm.hot(heatmap)[:, :, :3] * 255).astype(np.uint8)
    
    # Converte para base64
    img_pil = Image.fromarray(heatmap_colored)
    buffer = BytesIO()
    img_pil.save(buffer, format='PNG')
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return img_base64

@app.route('/api/predict', methods=['POST'])
def predict():
    """Endpoint de predição"""
    if model is None:
        return jsonify({
            'error': 'Modelo não carregado. Verifique se o arquivo existe.'
        }), 500
    
    try:
        # Pega a imagem do request
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhuma imagem enviada'}), 400
        
        file = request.files['image']
        image_bytes = file.read()
        
        # Preprocessa
        img_array = preprocess_image(image_bytes)
        
        # Predição
        predictions = model.predict(img_array, verbose=0)
        
        # Extrai probabilidades
        probs = predictions[0].tolist()
        
        # 🔍 Detecta formato do modelo (sigmoid=1 saída vs softmax=2 saídas)
        if len(probs) == 1:
            # Modelo com sigmoid (saída única): 0=normal, 1=tumor
            tumor_prob = float(probs[0])
            normal_prob = 1.0 - tumor_prob
            print(f"\n{'='*60}")
            print(f" MODELO SIGMOID (1 saída):")
            print(f"   Valor bruto: {tumor_prob:.4f}")
            print(f"   Normal: {normal_prob:.4f} ({normal_prob*100:.2f}%)")
            print(f"   Tumor:  {tumor_prob:.4f} ({tumor_prob*100:.2f}%)")
            print(f"{'='*60}\n")
        else:
            # Modelo com softmax (2 saídas): [normal, tumor]
            normal_prob = float(probs[0])
            tumor_prob = float(probs[1])
            print(f"\n{'='*60}")
            print(f" MODELO SOFTMAX (2 saídas):")
            print(f"   Normal: {normal_prob:.4f} ({normal_prob*100:.2f}%)")
            print(f"   Tumor:  {tumor_prob:.4f} ({tumor_prob*100:.2f}%)")
            print(f"{'='*60}\n")
        
        # Gera mapa de ativação
        heatmap_base64 = create_activation_heatmap(tumor_prob, max(normal_prob, tumor_prob))
        
        # Formato de resposta
        result = {
            'success': True,
            'predictions': {
                'normal': normal_prob,
                'tumor': tumor_prob
            },
            'confidence': float(max(normal_prob, tumor_prob)),
            'classification': 'tumor' if tumor_prob > 0.5 else 'normal',
            'heatmap': heatmap_base64
        }
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Erro na predição: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Retorna informações do modelo"""
    if model is None:
        return jsonify({'error': 'Modelo não carregado'}), 500
    
    try:
        return jsonify({
            'input_shape': [int(x) if x else None for x in model.input_shape],
            'output_shape': [int(x) if x else None for x in model.output_shape],
            'layers': len(model.layers),
            'trainable_params': int(np.sum([tf.size(w).numpy() for w in model.trainable_weights]))
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== ROTAS DE AUTENTICAÇÃO =====

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login de usuário"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Busca usuário (sem hash de senha por simplicidade - use bcrypt em produção!)
        cur.execute(
            "SELECT id, username, full_name, email, role FROM users WHERE username = %s AND password = %s AND is_active = true",
            (username, password)
        )
        user = cur.fetchone()
        
        if user:
            user_id, username, full_name, email, role = user
            
            # Gera token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=24)
            
            # Salva sessão
            cur.execute(
                "INSERT INTO sessions (user_id, token, expires_at) VALUES (%s, %s, %s)",
                (user_id, token, expires_at)
            )
            
            # Atualiza last_login
            cur.execute(
                "UPDATE users SET last_login = %s WHERE id = %s",
                (datetime.now(), user_id)
            )
            
            conn.commit()
            cur.close()
            conn.close()
            
            return jsonify({
                'success': True,
                'token': token,
                'user': {
                    'id': user_id,
                    'username': username,
                    'full_name': full_name,
                    'email': email,
                    'role': role
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Usuário ou senha incorretos'
            }), 401
            
    except Exception as e:
        print(f"Erro no login: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/auth/verify', methods=['POST'])
def verify_token():
    """Verifica se token é válido"""
    try:
        token = request.json.get('token')
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            """SELECT u.id, u.username, u.full_name, u.role 
               FROM sessions s 
               JOIN users u ON s.user_id = u.id 
               WHERE s.token = %s AND s.expires_at > %s""",
            (token, datetime.now())
        )
        result = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if result:
            user_id, username, full_name, role = result
            return jsonify({
                'valid': True,
                'user': {
                    'id': user_id,
                    'username': username,
                    'full_name': full_name,
                    'role': role
                }
            })
        else:
            return jsonify({'valid': False}), 401
            
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout - invalida token"""
    try:
        token = request.json.get('token')
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM sessions WHERE token = %s", (token,))
        conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== ROTAS DE HISTÓRICO =====

@app.route('/api/history', methods=['GET'])
def get_history():
    """Lista histórico de análises do usuário"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verifica token
        cur.execute(
            "SELECT user_id FROM sessions WHERE token = %s AND expires_at > %s",
            (token, datetime.now())
        )
        session = cur.fetchone()
        
        if not session:
            return jsonify({'error': 'Token inválido'}), 401
        
        user_id = session[0]
        
        # Busca histórico
        cur.execute(
            """SELECT id, image_name, prediction_normal, prediction_tumor, 
                      confidence, threshold_used, result, created_at
               FROM analysis_history 
               WHERE user_id = %s 
               ORDER BY created_at DESC 
               LIMIT 50""",
            (user_id,)
        )
        
        history = []
        for row in cur.fetchall():
            history.append({
                'id': row[0],
                'image_name': row[1],
                'prediction_normal': float(row[2]),
                'prediction_tumor': float(row[3]),
                'confidence': float(row[4]),
                'threshold_used': float(row[5]),
                'result': row[6],
                'created_at': row[7].isoformat()
            })
        
        cur.close()
        conn.close()
        
        return jsonify({'success': True, 'history': history})
        
    except Exception as e:
        print(f"Erro ao buscar histórico: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['POST'])
def save_analysis():
    """Salva análise no histórico"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        data = request.json
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verifica token
        cur.execute(
            "SELECT user_id FROM sessions WHERE token = %s AND expires_at > %s",
            (token, datetime.now())
        )
        session = cur.fetchone()
        
        if not session:
            return jsonify({'error': 'Token inválido'}), 401
        
        user_id = session[0]
        
        # Salva análise
        cur.execute(
            """INSERT INTO analysis_history 
               (user_id, image_name, prediction_normal, prediction_tumor, 
                confidence, threshold_used, result)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               RETURNING id""",
            (
                user_id,
                data.get('image_name'),
                data.get('prediction_normal'),
                data.get('prediction_tumor'),
                data.get('confidence'),
                data.get('threshold_used'),
                data.get('result')
            )
        )
        
        analysis_id = cur.fetchone()[0]
        conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify({'success': True, 'id': analysis_id})
        
    except Exception as e:
        print(f"Erro ao salvar análise: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/<int:analysis_id>', methods=['DELETE'])
def delete_analysis(analysis_id):
    """Deleta uma análise específica"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verifica token
        cur.execute(
            "SELECT user_id FROM sessions WHERE token = %s AND expires_at > %s",
            (token, datetime.now())
        )
        session = cur.fetchone()
        
        if not session:
            return jsonify({'error': 'Token inválido'}), 401
        
        user_id = session[0]
        
        # Verifica se análise pertence ao usuário
        cur.execute(
            "SELECT id FROM analysis_history WHERE id = %s AND user_id = %s",
            (analysis_id, user_id)
        )
        if not cur.fetchone():
            return jsonify({'error': 'Análise não encontrada'}), 404
        
        # Deleta análise
        cur.execute("DELETE FROM analysis_history WHERE id = %s", (analysis_id,))
        conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Erro ao deletar análise: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/clear-all', methods=['DELETE'])
def clear_all_history():
    """Deleta todo o histórico do usuário"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verifica token
        cur.execute(
            "SELECT user_id FROM sessions WHERE token = %s AND expires_at > %s",
            (token, datetime.now())
        )
        session = cur.fetchone()
        
        if not session:
            return jsonify({'error': 'Token inválido'}), 401
        
        user_id = session[0]
        
        # Deleta todas as análises do usuário
        cur.execute("DELETE FROM analysis_history WHERE user_id = %s", (user_id,))
        conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify({'success': True})
        
    except Exception as e:
        print(f"Erro ao limpar histórico: {e}")
        return jsonify({'error': str(e)}), 500

# ===== ROTA PARA SERVIR ARQUIVOS ESTÁTICOS =====

@app.route('/web/<path:path>')
def serve_static(path):
    """Serve arquivos estáticos da pasta web"""
    return send_from_directory('.', path)

if __name__ == '__main__':
    print("=" * 60)
    print(" NeuroAI - Servidor de Inferência Local")
    print("=" * 60)
    
    # Carrega modelo
    load_model()
    
    if model is None:
        print("\n ATENÇÃO: Modelo não encontrado!")
        print("Execute o treinamento primeiro ou verifique o caminho.")
    else:
        print("\n Modelo carregado com sucesso!")
    
    print("\n Servidor rodando em: http://localhost:5000")
    print(" API disponível em: http://localhost:5000/api/predict")
    print("\n Abra a interface web: http://localhost:5000/web/index.html")
    print("\nPressione Ctrl+C para parar o servidor")
    print("=" * 60)
    
    # Roda servidor
    app.run(host='0.0.0.0', port=5000, debug=True)
