/**
 * Script de Setup do Banco de Dados PostgreSQL
 * Cria database, tabelas e usuário admin padrão
 */

const { Client } = require('pg');

// Conexão inicial (sem database específico)
const adminClient = new Client({
  host: 'localhost',
  port: 5433,
  database: 'postgres',  // Database padrão
  user: 'postgres',
  password: 'neuro'
});

// Conexão para o database neuroia
const neuroiaClient = new Client({
  host: 'localhost',
  port: 5433,
  database: 'neuroia',
  user: 'postgres',
  password: 'neuro'
});

async function setupDatabase() {
  try {
    console.log('🔧 Iniciando setup do banco de dados...\n');

    // 1. Conecta no postgres para criar o database
    await adminClient.connect();
    console.log('✅ Conectado ao PostgreSQL');

    // 2. Verifica se database neuroia existe
    const checkDb = await adminClient.query(
      "SELECT 1 FROM pg_database WHERE datname = 'neuroia'"
    );

    if (checkDb.rows.length === 0) {
      console.log('📦 Criando database neuroia...');
      await adminClient.query('CREATE DATABASE neuroia');
      console.log('✅ Database neuroia criado');
    } else {
      console.log('ℹ️  Database neuroia já existe');
    }

    await adminClient.end();

    // 3. Conecta no database neuroia
    await neuroiaClient.connect();
    console.log('✅ Conectado ao database neuroia\n');

    // 4. Cria tabela de usuários
    console.log('📋 Criando tabela de usuários...');
    await neuroiaClient.query(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        full_name VARCHAR(100),
        email VARCHAR(100),
        role VARCHAR(20) DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        is_active BOOLEAN DEFAULT true
      )
    `);
    console.log('✅ Tabela users criada');

    // 5. Cria tabela de sessões
    console.log('📋 Criando tabela de sessões...');
    await neuroiaClient.query(`
      CREATE TABLE IF NOT EXISTS sessions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        token VARCHAR(255) UNIQUE NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    console.log('✅ Tabela sessions criada');

    // 6. Cria tabela de análises (histórico)
    console.log('📋 Criando tabela de análises...');
    await neuroiaClient.query(`
      CREATE TABLE IF NOT EXISTS analysis_history (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        image_name VARCHAR(255),
        prediction_normal DECIMAL(5,4),
        prediction_tumor DECIMAL(5,4),
        confidence DECIMAL(5,4),
        threshold_used DECIMAL(3,2),
        result VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `);
    console.log('✅ Tabela analysis_history criada\n');

    // 7. Verifica se usuário admin existe
    const checkAdmin = await neuroiaClient.query(
      "SELECT 1 FROM users WHERE username = 'admin'"
    );

    if (checkAdmin.rows.length === 0) {
      console.log('👤 Criando usuário admin padrão...');
      
      // Senha: 'admin' (em produção, use bcrypt!)
      // Por simplicidade inicial, salvando diretamente
      await neuroiaClient.query(`
        INSERT INTO users (username, password, full_name, email, role)
        VALUES ('admin', 'admin', 'Administrador', 'admin@neuroai.local', 'admin')
      `);
      console.log('✅ Usuário admin criado');
      console.log('   Username: admin');
      console.log('   Password: admin\n');
    } else {
      console.log('ℹ️  Usuário admin já existe\n');
    }

    // 8. Testa consulta
    console.log('🧪 Testando consulta...');
    const result = await neuroiaClient.query('SELECT * FROM users');
    console.log(`✅ ${result.rows.length} usuário(s) encontrado(s):\n`);
    
    result.rows.forEach(user => {
      console.log(`   ID: ${user.id}`);
      console.log(`   Username: ${user.username}`);
      console.log(`   Nome: ${user.full_name}`);
      console.log(`   Role: ${user.role}`);
      console.log(`   Criado em: ${user.created_at}`);
      console.log('');
    });

    await neuroiaClient.end();
    
    console.log('✅ Setup concluído com sucesso!');
    console.log('\n🚀 Você pode agora:');
    console.log('   1. Iniciar o servidor: node web/auth_server.js');
    console.log('   2. Fazer login com: admin / admin');
    console.log('   3. Acessar: http://localhost:5000/web/login.html\n');

  } catch (error) {
    console.error('❌ Erro no setup:', error.message);
    console.error(error);
    process.exit(1);
  }
}

// Executa setup
setupDatabase();
