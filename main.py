from fastapi import FastAPI
from pathlib import Path
from modeloDeLinguagem import Quint
from uuid import uuid4
import json
from datetime import datetime

api = FastAPI()
quint = Quint(model="llama3.2")
pastaHistorico = Path(__file__).resolve().parent.parent / "Histórico"

@api.get("/")
def LerRaís():
    return {"Chave": "Valor"}

@api.get("/QUINT/IniciarSessao")
def IniciarSessao(primeiroPrompt: str):
    título = TitularArquivo(primeiroPrompt)
    diálogo = Conversar(primeiroPrompt)
    identificador = CriarID()
    
    sessao = []
    sessao.append({
               "ID": identificador,
               "TÍTULO": título["TÍTULO"],
               "CRIAÇÃO": f"{datetime.now()}",
               "ULTIMA_ATUALIZAÇÃO": f"{datetime.now()}"
                })
    sessao.append(diálogo)
    
    pastaHistorico.mkdir(parents=True, exist_ok=True)
    
    nomeArquivo = f"{identificador}.json"
    caminhoArquivo = pastaHistorico / nomeArquivo

    try:
        with caminhoArquivo.open("w", encoding="utf-8") as arquivo:
            json.dump(sessao, arquivo, ensure_ascii=False, indent=4)
    
        return sessao
        
    except (OSError, TypeError) as erro:
        return f"Erro '{erro}' ao criar a sessão"

@api.get("/QUINT/Conversas")
def EnviarConversas():
    conversas = []

    for caminhoArquivo in sorted(pastaHistorico.glob("*.json")):
        with caminhoArquivo.open("r", encoding="utf-8") as arquivo:
            sessao = json.load(arquivo)

        conversas.append({
            "ID": sessao[0]['ID'],
            "TÍTULO": sessao[0]['TÍTULO']
        })

    return conversas

@api.get("/QUINT/ContinuarSessao")
def ContinuarSessao(id: str, prompt: str):
    diálogo = Conversar(prompt)

    caminhoArquivo = pastaHistorico / f"{id}.json"

    try:
        with open(caminhoArquivo, "r", encoding="utf-8") as arquivo:
            conversa = json.load(arquivo)
        
        conversa.append(diálogo)

        with caminhoArquivo.open("w", encoding="utf-8") as arquivo:
            json.dump(conversa, arquivo, ensure_ascii=False, indent=4)

        return diálogo

    except (OSError, TypeError) as erro:
        return f"Erro '{erro}' ao salvar a sessão"

def CriarID():
    while True:
        identificador = str(uuid4())
        caminhoArquivo = pastaHistorico / f"{identificador}.json"

        if not caminhoArquivo.exists():
            return identificador
        
def TitularArquivo(texto: str):
    resposta = quint.GerarResposta(prompt=f"Identifique o tema central deste texto e o resuma em uma linha de 3 a 5 palavras. Texto: {texto}")
    return {"TÍTULO": resposta}

def Conversar(prompt: str):
    resposta = quint.GerarResposta(prompt=f"{prompt}")
    return {
        "USUÁRIO": prompt,
        "QUINT": resposta
        }
