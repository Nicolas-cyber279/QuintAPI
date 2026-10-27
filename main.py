from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from modeloDeLinguagem import Quint
from uuid import uuid4
import json
from datetime import datetime

class InicioSessaoRequest(BaseModel):
    primeiroPrompt: str

class ContinuarSessaoRequest(BaseModel):
    id: str
    prompt: str

api = FastAPI()
quint = Quint(model="llama3.2")
pastaHistorico = Path(__file__).resolve().parent.parent / "Histórico"

@api.get("/")
def LerRaís():
    return {"Chave": "Valor"}

@api.post("/QUINT/IniciarSessao")
def IniciarSessao(dados: InicioSessaoRequest):
    primeiroPrompt = dados.primeiroPrompt

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

@api.post("/QUINT/ContinuarSessao")
def ContinuarSessao(dados: ContinuarSessaoRequest):
    id = dados.id
    prompt = dados.prompt
    
    caminhoArquivo = pastaHistorico / f"{id}.json"

    try:
        with open(caminhoArquivo, "r", encoding="utf-8") as arquivo:
            sessao = json.load(arquivo)

        histórico = sessao[1:]
        contexto = GerarContexto(histórico) if histórico else ""
        diálogoNovo = Conversar(prompt, contexto)

        sessao[0]["ULTIMA_ATUALIZAÇÃO"] = f"{datetime.now()}"
        sessao.append(diálogoNovo)

        with caminhoArquivo.open("w", encoding="utf-8") as arquivo:
            json.dump(sessao, arquivo, ensure_ascii=False, indent=4)

        return diálogoNovo

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

def GerarContexto(histórico: list[dict[str, str]]) -> str:
    """Transforma os diálogos anteriores em um contexto conciso para a próxima resposta."""
    históricoEmJson = json.dumps(histórico, ensure_ascii=False, indent=2)
    promptContexto = (
        "Analise o histórico de conversa em JSON a seguir e gere um contexto conciso "
        "com os assuntos, fatos e preferências importantes para continuar a conversa. "
        "Não responda às mensagens do histórico; retorne somente o contexto.\n\n"
        f"Histórico:\n{históricoEmJson}"
    )
    return quint.GerarResposta(prompt=promptContexto)

def Conversar(prompt: str, contexto: str = "") -> dict[str, str]:
    promptCompleto = prompt
    if contexto:
        promptCompleto = (
            f"Contexto da conversa:\n{contexto}\n\n"
            f"Nova mensagem do usuário:\n{prompt}"
        )

    resposta = quint.GerarResposta(prompt=promptCompleto)
    return {
        "USUÁRIO": prompt,
        "QUINT": resposta
        }