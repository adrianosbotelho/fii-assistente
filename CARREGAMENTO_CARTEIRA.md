# 📊 Guia de Carregamento de Carteira

## Opções Disponíveis

### 1. 📄 CSV Manual (Atual - Simples)
**Vantagens:**
- ✅ Simples e direto
- ✅ Controle total sobre os dados
- ✅ Não depende de APIs externas

**Desvantagens:**
- ❌ Requer atualização manual
- ❌ Preços podem ficar desatualizados
- ❌ Dividendos precisam ser atualizados manualmente

**Uso:**
```python
# Manter arquivo data/carteira.csv com:
Ticker,Quantidade,Preco_Medio,Dividendo_Mensal
BTLG11,102,100.79,0.79
```

---

### 2. 🔄 CSV + Atualização Automática (Recomendado)
**Vantagens:**
- ✅ Mantém apenas quantidade no CSV (simples)
- ✅ Preços e dividendos atualizados automaticamente
- ✅ Sempre com dados atuais do mercado
- ✅ Facilita manutenção

**Desvantagens:**
- ⚠️ Depende de API do Yahoo Finance (pode ter rate limits)

**Uso:**
```python
from core.carteira_loader import carregar_carteira_completa

# CSV mínimo apenas com Ticker e Quantidade
# O sistema busca preços e dividendos automaticamente
df = carregar_carteira_completa(atualizar_dados=True)
```

**CSV simplificado:**
```csv
Ticker,Quantidade
BTLG11,102
VISC11,90
```

---

### 3. 📊 Google Sheets (Semi-automático)
**Vantagens:**
- ✅ Edição fácil via interface web
- ✅ Atualização automática ao abrir dashboard
- ✅ Acesso de qualquer lugar
- ✅ Compartilhamento fácil

**Desvantagens:**
- ⚠️ Requer configuração de credenciais Google
- ⚠️ Dependente de internet

**Setup:**
1. Criar planilha no Google Sheets
2. Colunas: `Ticker`, `Quantidade` (opcional: `Preco_Medio`, `Dividendo_Mensal`)
3. Obter ID da planilha da URL
4. Configurar credenciais Google (credentials.json)

**Uso:**
```python
from core.carteira_loader import carregar_carteira_google_sheets

df = carregar_carteira_google_sheets(
    sheet_id="SEU_SHEET_ID",
    worksheet_name="Carteira"
)
```

---

### 4. 📱 API de Corretora (Futuro)
**Vantagens:**
- ✅ Totalmente automático
- ✅ Dados sempre sincronizados
- ✅ Histórico completo

**Desvantagens:**
- ❌ Requer credenciais de API
- ❌ Cada corretora tem API diferente
- ❌ Pode ter custos

**Corretoras com API:**
- XP Investimentos
- Rico (Rico API)
- BTG Pactual
- Modal

---

## 🎯 Recomendação: CSV Simplificado + Atualização Automática

**Melhor equilíbrio entre simplicidade e automação:**

1. **Manter CSV mínimo:**
   ```csv
   Ticker,Quantidade
   BTLG11,102
   VISC11,90
   ```

2. **O sistema busca automaticamente:**
   - Preço atual de cada FII
   - Dividendos recentes (média dos últimos 3 meses)
   - Dividend Yield

3. **Vantagens:**
   - Só precisa atualizar quando comprar/vender
   - Dados sempre atualizados
   - Sem dependência de Google/APIs externas complexas

---

## 💡 Implementação no Dashboard

O `app.py` já suporta múltiplas opções. Para usar atualização automática:

```python
# Na sidebar do Streamlit, adicionar opção:
atualizar_automatico = st.sidebar.checkbox(
    "🔄 Atualizar preços e dividendos automaticamente",
    value=True
)

df = carregar_carteira_completa(
    atualizar_dados=atualizar_automatico,
    usar_preco_medio=False  # Usar preços atuais ao invés de médio
)
```

---

## 🚀 Próximos Passos

1. **Curto Prazo:** Usar CSV simplificado + atualização automática
2. **Médio Prazo:** Integrar Google Sheets para edição mais fácil
3. **Longo Prazo:** Integrar API da corretora (se disponível)
