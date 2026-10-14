from main import Conversa
from main import SalvarSessao

sessao = []

while True:
    prompt = input("Você: ")
    if prompt.lower().strip() == "tchau":
        print(SalvarSessao(sessao))
        break

    try:
        conversa = Conversa(prompt)
        sessao.append(conversa)
        print(f"Quint: {conversa['RESPOSTA']}")

    except Exception as e:
        print(f"Falha ao conectar com a API: {e}")