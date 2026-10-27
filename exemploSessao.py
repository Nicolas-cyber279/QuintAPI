import requests
enderecoPublico = "https://api.nicolasvaladares.pro"
enderecoLocal = "http://localhost:8000"

while True:
    print()
    print("=== Q.U.I.N.T. ===")
    print()
    print("1- Iniciar conversa")
    print("2- Retomar conversa")
    print("3- Sair")

    try:
        escolha = int(input("Qual opção você escolhe? "))
    except:
        print("digite um número válido!")
        continue
    
    if escolha == 1:
        prompt = input("Você: ")

        try:
            requisicaoHttp = requests.post(f"{enderecoLocal}/QUINT/IniciarSessao", json={"primeiroPrompt": prompt}, timeout=180)
            requisicaoHttp.raise_for_status()
            sessao = requisicaoHttp.json()
        except Exception as erro:
            print(f"Erro ao se conectar com a API [{erro}]")
            continue

        identificador = sessao[0]['ID']
        print(f"QUINT: {sessao[1]['QUINT']}")

        print("\n**Para parar a conversa, digite 'tchau'.**\n")

        while True:
            prompt = input("Você: ")

            if prompt.lower().strip() == "tchau":
                break

            try: 
                respostaHTTP = requests.post(f"{enderecoLocal}/QUINT/ContinuarSessao", json={"id": identificador, "prompt":prompt}, timeout=180)
                respostaHTTP.raise_for_status()
                resposta = respostaHTTP.json()
            except Exception as erro:
                print(f"Erro ao se conectar com a API [{erro}]")

            print(f"QUINT: {resposta['QUINT']}")
            
    elif escolha == 2:

        try:
            historicoHTTP = requests.get(f"{enderecoLocal}/QUINT/Conversas", timeout=180)
            historicoHTTP.raise_for_status()
            historicoConversas = historicoHTTP.json()
        except Exception as erro:
            print(f"Erro ao se conectar com a API [{erro}]")
            continue

        if not historicoConversas:
            print("Não há nenhuma conversa ainda...")
            continue
        
        print("Suas conversas recentes: ")

        for indice, conversa in enumerate(historicoConversas):
            print(f"{indice + 1} -- {conversa['TÍTULO']}")

        try:
            idConversa = int(input("Digite o número da conversa que você quer retomar: "))
        except:
            print("digite um número válido!")
            continue

        if idConversa < 0 or idConversa > enumerate(historicoConversas):
            print("Número inválido!")
            continue
        
        identificador = historicoConversas[idConversa-1]['ID']

        print("\n**Para parar a conversa, digite 'tchau'.**\n")

        while True:
            prompt = input("Você: ")

            if prompt.lower().strip() == "tchau":
                break

            try:    
                respostaHTTP = requests.post(f"{enderecoLocal}/QUINT/ContinuarSessao", json={"id": identificador, "prompt":prompt}, timeout=180)
                respostaHTTP.raise_for_status()
                resposta = respostaHTTP.json()
            except Exception as erro:
                print(f"Erro ao se conectar com a API [{erro}]")
                continue

            print(f"QUINT: {resposta['QUINT']}")
        
    elif escolha == 3:
        print("Obrigado por falar com o Q.U.I.N.T.! até a próxima!")
        break
    else:
        print("Opção inválida!")