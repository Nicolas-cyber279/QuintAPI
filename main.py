import requests
from fastapi import FastAPI
from modeloDeLinguagem import Quint

api = FastAPI()
quint = Quint(model="llama3.2")

@api.get("/")
def LerRaís():
    return {"Chave": "Valor"}


def Conversa(prompt: str | None = None):
    requisitar = requests.post(f"http://localhost:8000/conversas/respostas/{prompt}", timeout=120)
    
    @api.get(f"/conversas/respostas/{prompt}")
    def LerResposta(resposta: str | None = "Nada ainda, aguarde..."):
        resposta = quint.gerar_resposta(prompt)
        return {"USUÁRIO": prompt, "RESPOSTA": resposta}
    