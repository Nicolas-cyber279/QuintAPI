import requests
import json
import re
from pathlib import Path
from fastapi import FastAPI
from modeloDeLinguagem import Quint

api = FastAPI()
quint = Quint(model="llama3.2")

@api.get("/")
def LerRaís():
    return {"Chave": "Valor"}

@api.get("/QUINT/conversas/respostas")
def LerResposta(prompt: str):
    resposta = quint.GerarResposta(prompt)
    return {"USUÁRIO": prompt, "RESPOSTA": resposta}

def Conversa(prompt: str):
    url = "https://api.nicolasvaladares.pro/QUINT/conversas/respostas"
    requisitar = requests.get(url, params={"prompt":prompt})
    return requisitar.json()

def SalvarSessao(sessao: list):
    pastaHistorico = Path(__file__).resolve().parent.parent / "Histórico"
    pastaHistorico.mkdir(parents=True, exist_ok=True)

    nomeSessao = Conversa(f"Este é um prompt do início da sessão que você teve com o usuário: '{sessao[0]['USUÁRIO']}'\nFaça um resumo de uma linha, dê preferência para resumir usando de 3 a 5 palavras, com base no contexto dele para nomear o arquivo JSON que vai guardar a conversa. Responda só com o nome do arquivo, por favor.")
    nomeArquivo = f"{nomeSessao['RESPOSTA']}.json"
    caminhoArquivo = pastaHistorico / nomeArquivo
    
    try:
        with caminhoArquivo.open("w", encoding="utf-8") as arquivo:
            json.dump(sessao, arquivo, ensure_ascii=False, indent=4)

        return f"Obrigado por falar com o Q.U.I.N.T.\nSessão Salva em {caminhoArquivo}."
    
    except (OSError, TypeError) as erro:
        return f"Erro '{erro}' ao salvar a sessão"