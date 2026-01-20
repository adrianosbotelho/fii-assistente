# 🎯 Como Usar - FII Assistente com Login Simples

## 🚀 Início Rápido

### 1. Primeira Execução

```bash
# 1. Copiar configuração
cp .env.example .env

# 2. Editar senha (OBRIGATÓRIO)
# Abra .env e altere AUTH_PASSWORD=sua_senha_segura

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar aplicação
streamlit run app.py
```

### 2. Fazer Login

1. **Acesse**: `http://localhost:8501`
2. **Email**: `adrianosbotelho@gmail.com`
3. **Senha**: A que você definiu no `.env`
4. **Clique**: "🚀 Entrar"

## 📊 Funcionalidades Após Login

### Dashboard Principal
- **KPIs**: Patrimônio, renda mensal, yield médio
- **Análise de IA**: Saúde da carteira com insights
- **Projeções**: Crescimento com reinvestimento
- **Benchmarks**: Comparação com SELIC, IFIX, Poupança

### Gestão de Carteira
- **Upload**: Importe sua carteira via CSV
- **Análise**: Visualize distribuição e performance
- **Reinvestimento**: Calcule e aplique dividendos
- **Backup**: Backups automáticos a cada alteração

### Configurações Pessoais
- **Tema**: Dark/Light mode (salvo automaticamente)
- **Horizonte**: Período de projeção preferido
- **Estratégia**: Método de reinvestimento padrão
- **Auto-update**: Atualização automática de preços

## 📁 Estrutura de Arquivos

Após o primeiro login, será criado:

```
data/
├── carteira.csv              # Sua carteira (criada automaticamente)
├── user_config.json          # Suas preferências
├── carteira_backup_*.csv     # Backups automáticos
└── reports/                  # Relatórios salvos
    └── report_*.json
```

## 🔄 Fluxo de Trabalho Típico

### 1. Login Diário
1. Acesse a aplicação
2. Faça login com seu email e senha
3. Veja o dashboard atualizado

### 2. Atualizar Carteira
1. **Opção A**: Upload de novo CSV
2. **Opção B**: Editar `data/carteira.csv` diretamente
3. Recarregue a página para ver mudanças

### 3. Reinvestimento Mensal
1. Vá na aba "💰 Calcular e Aplicar Reinvestimento"
2. Escolha sua estratégia preferida
3. Revise os cálculos
4. Clique "💾 Salvar Diretamente"
5. Recarregue para ver carteira atualizada

### 4. Análise e Relatórios
1. Explore as diferentes abas de análise
2. Compare fundos lado a lado
3. Veja projeções de crescimento
4. Analise benchmarks de mercado

## ⚙️ Configurações Avançadas

### Alterar Senha
1. Edite `.env`: `AUTH_PASSWORD=nova_senha`
2. Reinicie a aplicação
3. Faça login com a nova senha

### Modo Debug
1. Edite `.env`: `DEBUG=true`
2. Reinicie a aplicação
3. Veja informações extras na tela de login

### Personalizar Carteira Inicial
Edite `user_manager.py`, função `_create_default_carteira()`:

```python
default_data = {
    "Ticker": ["SEUS", "FIIS", "AQUI"],
    "Quantidade": [100, 200, 150],
    "Preco_Medio": [100.00, 95.50, 110.20],
    "Dividendo_Mensal": [1.00, 0.90, 1.10]
}
```

## 🛡️ Segurança e Backup

### Backups Automáticos
- Criados a cada alteração da carteira
- Formato: `carteira_backup_YYYYMMDD_HHMMSS.csv`
- Limpeza automática após 30 dias

### Dados Seguros
- Senha criptografada com SHA-256
- Rate limiting (5 tentativas/hora)
- Session state isolado
- Dados locais protegidos

### Recuperação
Se perder dados:
1. Verifique backups em `data/carteira_backup_*.csv`
2. Renomeie o backup mais recente para `carteira.csv`
3. Recarregue a aplicação

## 🌐 Deploy em Produção

### Render (Recomendado)
1. Faça push do código para GitHub
2. Conecte repositório no Render
3. Configure variável: `AUTH_PASSWORD=sua_senha`
4. Deploy automático

### Outras Plataformas
- Heroku: Configure `AUTH_PASSWORD` nas config vars
- Railway: Adicione variável de ambiente
- Vercel: Configure em Environment Variables

## 🎯 Dicas de Uso

### Performance
- Use "Atualizar dados automaticamente" apenas quando necessário
- Mantenha carteira com até 50 FIIs para melhor performance
- Limpe backups antigos periodicamente

### Análise
- Compare sempre com benchmarks
- Use diferentes estratégias de reinvestimento
- Acompanhe evolução do yield médio
- Monitore concentração por fundo

### Manutenção
- Faça backup manual importante antes de grandes mudanças
- Atualize preços mensalmente
- Revise estratégia de reinvestimento trimestralmente
- Monitore alertas de saúde da carteira

## 🐛 Problemas Comuns

### "Credenciais inválidas"
- ✅ Email: `adrianosbotelho@gmail.com` (exato)
- ✅ Senha: Confira no `.env`
- ✅ Sem espaços extras

### "Muitas tentativas"
- ⏰ Aguarde 1 hora
- 🔄 Ou reinicie aplicação
- ✅ Confirme senha correta

### Dados não salvam
- ��� Verifique permissões pasta `data/`
- 🔐 Confirme se está logado
- 🔄 Tente recarregar página

### Aplicação não inicia
- 📦 `pip install -r requirements.txt`
- 📄 Verifique se `.env` existe
- 🐍 Use Python 3.8+

---

**🎉 Agora você tem controle total da sua carteira de FIIs!**