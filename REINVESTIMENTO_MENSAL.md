# 💰 Guia de Reinvestimento Mensal de Dividendos

## 📋 Visão Geral

Este guia explica como usar a ferramenta de reinvestimento mensal para atualizar automaticamente a quantidade de cotas dos fundos após receber e reinvestir os dividendos.

---

## 🔄 Processo Mensal

### Passo 1: Receber Dividendos
Mensalmente, você recebe dividendos dos FIIs da sua carteira. A quantidade varia conforme o desempenho de cada fundo.

### Passo 2: Reinvestir Dividendos
Com os dividendos recebidos, você compra mais cotas dos fundos, aumentando sua posição.

### Passo 3: Atualizar Carteira no Sistema
Use a ferramenta no dashboard para calcular e atualizar as novas quantidades automaticamente.

---

## 🛠️ Como Usar a Ferramenta

### No Dashboard:

1. **Acesse a aba "💰 Calcular e Aplicar Reinvestimento"**
   - Na seção "Análise Detalhada e Comparação de Fundos"
   - Última aba à direita

2. **Selecione a Estratégia de Distribuição:**
   - **🔄 Proporcional**: Distribui conforme a renda gerada por cada fundo
   - **📈 Yield Alto**: Prioriza fundos com maior yield
   - **🎯 Diversificação**: Prioriza fundos menos representados na carteira

3. **Revise os Resultados:**
   - Veja quantas cotas serão compradas
   - Valores investidos por fundo
   - Nova quantidade total após reinvestimento

4. **Atualize a Carteira:**
   
   **Opção A - Download Manual:**
   - Clique em "📥 Gerar CSV Atualizado"
   - Baixe o arquivo gerado
   - Substitua `data/carteira.csv` pelo novo arquivo
   
   **Opção B - Salvar Automaticamente:**
   - Clique em "💾 Salvar Diretamente"
   - O sistema atualiza `data/carteira.csv` automaticamente
   - Cria backup automático antes de atualizar

---

## 📊 O Que o Sistema Calcula

### Automaticamente:

1. **Cotas Compradas:**
   - Calcula quantas cotas podem ser compradas com cada dividendo
   - Usa preços atuais do mercado (via API)

2. **Preço Médio Atualizado:**
   - Recalcula o preço médio ponderado após comprar novas cotas
   - Fórmula: (Quantidade Anterior × Preço Médio Anterior + Novas Cotas × Preço Atual) / Nova Quantidade Total

3. **Nova Quantidade:**
   - Soma a quantidade atual + cotas compradas

4. **Valor Não Utilizado:**
   - Mostra a "sobra" que não deu para comprar cota inteira
   - Pode ser acumulado para o próximo mês

---

## 📝 Exemplo Prático

### Situação Inicial:
```
Ticker: VGIA11
Quantidade: 690 cotas
Preço Médio: R$ 9,12
Dividendo Mensal: R$ 0,14/cota
Renda Mensal: R$ 96,60 (690 × 0,14)
```

### Após Receber Dividendos:
```
Dividendos Recebidos: R$ 96,60
Preço Atual do VGIA11: R$ 9,50
```

### Reinvestimento:
```
Valor para Reinvestir: R$ 96,60
Preço Atual: R$ 9,50
Cotas Compradas: 10 (R$ 96,60 ÷ R$ 9,50 = 10,17 → arredonda para 10)
Valor Utilizado: R$ 95,00 (10 × R$ 9,50)
Sobra: R$ 1,60
```

### Nova Carteira:
```
Nova Quantidade: 700 cotas (690 + 10)
Valor Anterior: R$ 6.292,80 (690 × 9,12)
Valor Novo: R$ 95,00 (10 × 9,50)
Total Investido: R$ 6.387,80
Novo Preço Médio: R$ 9,13 (6.387,80 ÷ 700)
```

---

## ⚠️ Importante

### Frequência:
- Execute o reinvestimento **mensalmente**, após receber os dividendos
- Geralmente os dividendos são pagos entre os dias 10-20 de cada mês

### Backup:
- O sistema cria backup automático ao salvar
- Mantenha backups antigos para histórico

### Preços:
- O sistema busca preços atuais automaticamente
- Se houver problema de conexão, use preços que você conhece e ajuste manualmente

### Sobras:
- Valores pequenos que não dão para comprar cota inteira ficam como "sobra"
- Essas sobras podem ser acumuladas para o próximo mês

---

## 🎯 Dicas

1. **Estratégia Recomendada:**
   - Use "Proporcional" para manter a alocação atual
   - Use "Yield Alto" se quiser maximizar retorno
   - Use "Diversificação" para balancear melhor a carteira

2. **Revisão:**
   - Sempre revise os resultados antes de salvar
   - Verifique se as quantidades fazem sentido

3. **Histórico:**
   - Mantenha os CSVs de backup para acompanhar evolução
   - Compare mês a mês para ver crescimento

4. **Documentação:**
   - Anote manualmente os dividendos recebidos (opcional)
   - Compare com os cálculos do sistema para validar

---

## 📂 Estrutura de Arquivos

```
data/
  ├── carteira.csv                    # Carteira atual (apenas Ticker e Quantidade)
  ├── carteira_backup_YYYYMMDD.csv   # Backups automáticos
  └── carteira_atualizada_YYYYMMDD.csv # CSVs gerados para download
```

---

## ❓ Perguntas Frequentes

**P: Preciso atualizar manualmente os dividendos?**
R: Não! Se você usar a opção "Atualizar preços e dividendos automaticamente", o sistema busca tudo via API.

**P: E se eu quiser reinvestir em apenas um fundo?**
R: Você pode editar manualmente o CSV sugerido antes de salvar, ou ajustar os valores na tabela.

**P: O que fazer com a "sobra" não utilizada?**
R: Ela fica registrada e pode ser considerada no próximo mês. Alguns sistemas acumulam automaticamente.

**P: Posso usar preços diferentes dos atuais?**
R: Sim, você pode editar o CSV gerado e usar preços de compra diferentes.

**P: Quantas vezes por mês devo atualizar?**
R: Geralmente uma vez por mês, após receber todos os dividendos.

---

## 🔗 Recursos Relacionados

- **Dashboard**: Acesse a aba "💰 Calcular e Aplicar Reinvestimento"
- **Sugestões**: Veja a aba "💡 Sugestão de Reinvestimento" para análise prévia
- **Histórico**: Mantenha os backups para acompanhar evolução

---

**💡 Dica Final:** O crescimento orgânico via reinvestimento é poderoso! Mantenha a disciplina de reinvestir mensalmente para maximizar o crescimento da sua carteira.
