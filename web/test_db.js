/**
 * Teste de Conexão PostgreSQL
 */

const { Client } = require('pg');

const client = new Client({
  host: 'localhost',
  port: 5433,
  database: 'neuroia',
  user: 'postgres',
  password: 'neuro'
});

async function testConnection() {
  try {
    console.log('🔌 Testando conexão com PostgreSQL...\n');
    
    await client.connect();
    console.log('✅ Conectado com sucesso!\n');
    
    // Testa query simples
    const result = await client.query('SELECT NOW() as current_time');
    console.log('⏰ Hora do servidor:', result.rows[0].current_time);
    
    // Lista tabelas
    const tables = await client.query(`
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = 'public'
      ORDER BY table_name
    `);
    
    console.log('\n📋 Tabelas no database neuroia:');
    if (tables.rows.length === 0) {
      console.log('   (nenhuma tabela encontrada - execute setup_database.js primeiro)');
    } else {
      tables.rows.forEach(row => {
        console.log(`   - ${row.table_name}`);
      });
    }
    
    // Lista usuários
    try {
      const users = await client.query('SELECT id, username, role, created_at FROM users');
      console.log(`\n👥 Usuários cadastrados (${users.rows.length}):`);
      users.rows.forEach(user => {
        console.log(`   ${user.id}. ${user.username} (${user.role}) - ${user.created_at}`);
      });
    } catch (e) {
      console.log('\n⚠️  Tabela users não existe ainda');
    }
    
    await client.end();
    console.log('\n✅ Teste concluído!');
    
  } catch (error) {
    console.error('❌ Erro na conexão:', error.message);
    console.error('\n💡 Verifique:');
    console.error('   - PostgreSQL está rodando?');
    console.error('   - Porta 5433 está correta?');
    console.error('   - Usuário e senha estão corretos?');
    console.error('   - Database neuroia existe?');
    process.exit(1);
  }
}

testConnection();
