# 🔐 Configuração Simples - FII Assistente

Sistema de autenticação simplificado para **adrianosbotelho@gmail.com** apenas.

## ✨ Como Funciona

- **Email fixo**: `adrianosbotelho@gmail.com` (único usuário autorizado)
- **Senha configurável**: Definida via variável de ambiente
- **Login simples**: Apenas email + senha
- **Dados únicos**: Todos os dados ficam na pasta `data/`
- **Segurança**: Rate limiting (5 tentativas por hora)

## 🚀 Configuração Local

### 1. Definir Senha (OBRIGATÓRIO)

Crie um arquivo `.env` (copie de `.env.example`):

```bash
cp .env.example .env
```

Edite o `.env` e defina sua senha:

```bash
# Sua senha de acesso (OBRIGATÓRIA)
AUTH_PASSWORD=sua_senha_segura_aqui

# Modo debug (opcional)
DEBUG=false
```

⚠️ **Importante**: A senha é obrigatória. A aplicação não iniciará sem ela.

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Executar

```bash
streamlit run app.py
```

### 4. Fazer Login

1. Acesse `http://localhost:8501`
2. Digite: `adrianosbotelho@gmail.com`
3. Digite sua senha (definida no `.env`)
4. Clique em "Entrar"

## 🌐 Deploy no Render

### 1. Configurar Variável de Ambiente

No painel do Render, adicione:

```
AUTH_PASSWORD=sua_senha_segura
```

### 2. Deploy

O `render.yaml` já está configurado. Apenas faça push do código.

## 🛡️ Segurança

### Recursos de Segurança
- ✅ Email fixo (apenas você pode acessar)
- ✅ Senha com hash SHA-256
- ✅ Rate limiting (5 tentativas/hora)
- ✅ Bloqueio temporário após tentativas
- ✅ Session state seguro

### Recomendações
- Use uma senha forte (mínimo 8 caracteres)
- Não compartilhe a senha
- Mude a senha periodicamente
- Use HTTPS em produção (Render fornece automaticamente)

## 📁 Estrutura de Dados

```
data/
├── carteira.csv              # Sua carteira principal
├── user_config.json          # Suas configurações
├── carteira_backup_*.csv     # Backups automáticos
└── reports/                  # Histórico de relatórios
    └── report_*.json
```

## 🎯 Funcionalidades

### Login
- Email: `adrianosbotelho@gmail.com` (fixo)
- Senha: Configurável via `.env`
- Rate limiting: 5 tentativas por hora
- Logout seguro

### Dados Pessoais
- Carteira individual
- Configurações salvas (tema, preferências)
- Backups automáticos
- Histórico de relatórios

### Segurança
- Dados isolados
- Senha criptografada
- Proteção contra força bruta
- Session timeout

## 🔧 Personalização

### Alterar Email Autorizado

Edite `simple_auth.py`, linha 15:

```python
self.authorized_email = "seu_novo_email@gmail.com"
```

### Alterar Tempo de Bloqueio

Edite `simple_auth.py`, linha 35:

```python
if current_time - st.session_state.last_attempt < 3600:  # 1 hora
```

### Alterar Número de Tentativas

Edite `simple_auth.py`, linha 32:

```python
if st.session_state.login_attempts >= 5:  # 5 tentativas
```

## 🐛 Troubleshooting

### "Credenciais inválidas"
- Verifique se o email é exatamente `adrianosbotelho@gmail.com`
- Confirme se a senha no `.env` está correta
- Verifique se não há espaços extras

### "Muitas tentativas"
- Aguarde 1 hora ou reinicie a aplicação
- Verifique se a senha está correta

### Dados não salvam
- Verifique permissões da pasta `data/`
- Confirme se está logado
- Verifique logs de erro

### Senha não funciona
- Confirme se o arquivo `.env` existe
- Verifique se `AUTH_PASSWORD` está definido
- Reinicie a aplicação após alterar `.env`

## 📞 Suporte

Para problemas:
1. Verifique se `.env` está configurado
2. Confirme email e senha
3. Teste com `DEBUG=true` no `.env`
4. Verifique logs da aplicação

---

**🎉 Sistema simples e seguro para uso pessoal!**