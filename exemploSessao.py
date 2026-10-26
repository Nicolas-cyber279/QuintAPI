import requests

while True:
    print("=== Q.U.I.N.T. ===")
    print()
    print("1- Iniciar conversa")
    print("2- Retomar conversa")
    print("3- Sair")

    try:
        escolha = int(input("Qual opção você escolhe?"))
    except:
        print("digite um número válido!")
        continue
    
    if escolha == 1:
        prompt = input("Você: ")
        requisicaoHttp = requests.get("https://api.nicolasvaladares.pro/QUINT/IniciarSessao", params={"primeiroPrompt":prompt})
        requisicaoHttp.raise_for_status()
        sessao = requisicaoHttp.json()

        identificador = sessao[0]['ID']
        print(f"QUINT: {sessao[1]['QUINT']}")

        print("\n**Para parar a conversa, digite 'tchau'.**\n")

        while True:
            prompt = input("Você: ")

            if prompt.lower().strip() == "tchau":
                break
                
            respostaHTTP = requests.get("https://api.nicolasvaladares.pro/QUINT/ContinuarSessao", params={"id": identificador, "prompt":prompt})
            respostaHTTP.raise_for_status()
            resposta = respostaHTTP.json()

            print(f"QUINT: {resposta['QUINT']}")
            
    elif escolha == 2:
        historicoHTTP = requests.get("https://api.nicolasvaladares.pro/QUINT/Conversas")
        historicoHTTP.raise_for_status()
        historicoConversas = historicoHTTP.json()

        if not historicoConversas:
            print("Ainda não há nenhuma conversa!")
            continue

        print("Suas conversas recentes: ")

        for indice, conversa in enumerate(historicoConversas, start=1):
            print(f"{indice} -- {conversa['TÍTULO']}")

        try:
            idConversa = int(input("Digite o número da conversa que você quer retomar: "))
        except:
            print("digite um número válido!")
            continue

        identificador = historicoConversas[idConversa-1]['ID']

        print("\n**Para parar a conversa, digite 'tchau'.**\n")

        while True:
            prompt = input("Você: ")

            if prompt.lower().strip() == "tchau":
                break
                
            respostaHTTP = requests.get("https://api.nicolasvaladares.pro/QUINT/ContinuarSessao", params={"id": identificador, "prompt":prompt})
            respostaHTTP.raise_for_status()
            resposta = respostaHTTP.json()

            print(f"QUINT: {resposta['QUINT']}")
        
    elif escolha == 3:
        print("Obrigado por falar com o Q.U.I.N.T.! até a próxima!")
        break
    else:
        print("Opção inválida!")