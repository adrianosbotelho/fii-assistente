import yaml
from services.loader import carregar_carteira
from services.analytics import calcular_renda
from services.reinvest import sugestao_reinvestimento
from services.alerts import enviar_email

carteira = carregar_carteira()
renda = calcular_renda(carteira)

with open("config/regras.yaml") as f:
    regras = yaml.safe_load(f)["meta_percentual"]

sugestao = sugestao_reinvestimento(renda, regras)

mensagem = f"Renda mensal estimada: R$ {renda}\n\nSugestão de reinvestimento:\n"

for ativo, valor in sugestao.items():
    mensagem += f"- {ativo}: R$ {valor}\n"

enviar_email(
    "Relatório mensal – FII Assistente",
    mensagem
)
