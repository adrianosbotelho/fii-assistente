# 📊 Formato da Carteira CSV - FII Assistente

## 📁 Formatos Suportados

O FII Assistente aceita carteiras em dois formatos:

### 1. Formato Simples (Mínimo)
```csv
Ticker,Quantidade
HGLG11,100
XPML11,150
VISC11,200
```

**O sistema automaticamente adicionará:**
- `Preco_Medio`: Valores estimados baseados em dados históricos
- `Dividendo_Mensal`: Valores estimados baseados em dados históricos

### 2. Formato Completo (Recomendado)
```csv
Ticker,Quantidade,Preco_Medio,Dividendo_Mensal
HGLG11,100,160.50,1.20
XPML11,150,98.30,0.85
VISC11,200,95.80,0.92
```

## 🎯 Como Criar Sua Carteira

### Opção 1: Planilha Excel/Google Sheets

1. **Crie uma planilha** com as colunas:
   - `Ticker`: Código do FII (ex: HGLG11)
   - `Quantidade`: Número de cotas
   - `Preco_Medio`: Preço médio pago (opcional)
   - `Dividendo_Mensal`: Dividendo mensal por cota (opcional)

2. **Salve como CSV**:
   - Excel: Arquivo > Salvar Como > CSV
   - Google Sheets: Arquivo > Fazer download > CSV

### Opção 2: Editor de Texto

Crie um arquivo `minha_carteira.csv`:

```csv
Ticker,Quantidade,Preco_Medio,Dividendo_Mensal
BTLG11,102,95.50,0.85
VISC11,90,95.80,0.92
KNCR11,83,110.20,1.05
CPTS11,1100,8.50,0.08
XPML11,70,98.30,0.85
```

### Opção 3: Usar Carteira Existente

Se você já tem uma carteira com apenas `Ticker` e `Quantidade`:

1. **Faça upload** do arquivo atual
2. **O sistema automaticamente** adicionará as colunas faltantes
3. **Ajuste os valores** se necessário
4. **Salve** a carteira atualizada

## 📋 Regras e Validações

### Colunas Obrigatórias
- ✅ `Ticker`: Código do FII (formato: XXXX11)
- ✅ `Quantidade`: Número inteiro de cotas

### Colunas Opcionais
- 🔄 `Preco_Medio`: Preço médio de compra (R$)
- 🔄 `Dividendo_Mensal`: Dividendo mensal por cota (R$)

### Formato dos Dados
- **Ticker**: Texto (ex: HGLG11, XPML11)
- **Quantidade**: Número inteiro (ex: 100, 150)
- **Preco_Medio**: Número decimal (ex: 160.50, 98.30)
- **Dividendo_Mensal**: Número decimal (ex: 1.20, 0.85)

### Separadores
- **Vírgula**: Para separar colunas
- **Ponto**: Para decimais (não vírgula)
- **Sem espaços**: Nos códigos dos tickers

## 🔄 Atualização Automática

### Quando Usar "Atualizar Dados Automaticamente"

Marque esta opção na sidebar quando:
- ✅ Sua carteira tem apenas `Ticker` e `Quantidade`
- ✅ Quer preços atuais do mercado
- ✅ Quer dividendos atualizados
- ✅ Tem conexão com internet estável

### Quando NÃO Usar

Não marque quando:
- ❌ Quer manter seus preços médios históricos
- ❌ Tem conexão instável
- ❌ Quer análise mais rápida
- ❌ Já tem dados completos e atualizados

## 📊 Exemplos Práticos

### Carteira Pequena (5 FIIs)
```csv
Ticker,Quantidade,Preco_Medio,Dividendo_Mensal
HGLG11,100,160.50,1.20
XPML11,150,98.30,0.85
VISC11,200,95.80,0.92
BCFF11,80,85.20,0.78
MXRF11,120,10.45,0.09
```

### Carteira Média (10 FIIs)
```csv
Ticker,Quantidade,Preco_Medio,Dividendo_Mensal
BTLG11,102,95.50,0.85
VISC11,90,95.80,0.92
KNCR11,83,110.20,1.05
CPTS11,1100,8.50,0.08
XPML11,70,98.30,0.85
GARE11,810,12.80,0.12
MXRF11,751,10.45,0.09
VGIA11,690,9.20,0.08
XPCA11,600,16.50,0.15
CPUR11,200,5.80,0.05
```

### Carteira Simples (Só Ticker + Quantidade)
```csv
Ticker,Quantidade
HGLG11,100
XPML11,150
VISC11,200
BCFF11,80
MXRF11,120
```

## 🛠️ Ferramentas Úteis

### Conversão de Formatos
- **Excel para CSV**: Arquivo > Salvar Como > CSV (separado por vírgulas)
- **Google Sheets**: Arquivo > Fazer download > Valores separados por vírgula (.csv)
- **LibreOffice Calc**: Arquivo > Salvar Como > Texto CSV

### Validação Online
- Use o próprio FII Assistente para validar
- Faça upload e veja se há erros
- O sistema mostra mensagens claras sobre problemas

### Backup
- Sempre mantenha backup da carteira original
- O sistema cria backups automáticos
- Salve versões com data (ex: carteira_2024_01_20.csv)

## 🐛 Problemas Comuns

### "Coluna não encontrada"
- ✅ Verifique se os nomes das colunas estão corretos
- ✅ Não use acentos ou espaços nos nomes
- ✅ Use exatamente: `Ticker,Quantidade,Preco_Medio,Dividendo_Mensal`

### "Erro ao ler CSV"
- ✅ Salve como CSV UTF-8
- ✅ Use vírgula como separador
- ✅ Use ponto para decimais (não vírgula)

### "Ticker inválido"
- ✅ Use formato XXXX11 (ex: HGLG11)
- ✅ Verifique se o FII existe
- ✅ Sem espaços antes/depois do código

### "Quantidade inválida"
- ✅ Use apenas números inteiros
- ✅ Sem vírgulas ou pontos na quantidade
- ✅ Valores maiores que zero

## 💡 Dicas Avançadas

### Performance
- Carteiras até 50 FIIs: Performance ótima
- Carteiras 50-100 FIIs: Performance boa
- Carteiras 100+ FIIs: Considere dividir em grupos

### Organização
- Ordene por ticker alfabeticamente
- Agrupe por tipo de FII se necessário
- Use nomes consistentes nos arquivos

### Manutenção
- Atualize mensalmente após aportes
- Revise preços médios trimestralmente
- Monitore dividendos que mudaram

---

**📊 Com esses formatos, sua carteira estará sempre organizada e pronta para análise!**