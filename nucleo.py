from main import Conversa
import json
import datetime

while True:
    sessao = []

    prompt = input("Você: ")
    if prompt.lower().strip() == "tchau":
        print("Obrigado por falar com o Q.U.I.N.T., até a próxima!")

        with open(f"Conversa{datetime.date}_{datetime.time}", "w", encoding="utf-8") as arquivo:
            json.dump(sessao, arquivo, ensure_ascii=False, indent=4)
        break

    conversa = Conversa(prompt)
    sessao.append(conversa)

    print(f"Quint: {conversa["RESPOSTA"]}")
    