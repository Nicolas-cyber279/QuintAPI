import requests

class Quint:
    def __init__(self, model="llama3.2", host="http://localhost:11434"):
        self.model = model
        self.host = host

    def gerar_resposta(self, prompt):
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )

            response.raise_for_status()

            data = response.json()

            return data["response"]

        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                "Não foi possível conectar ao Ollama. "
                "Verifique se o Ollama está em execução."
            )

        except requests.exceptions.Timeout:
            raise RuntimeError(
                "O Ollama demorou demais para responder."
            )

        except requests.exceptions.HTTPError as erro:
            raise RuntimeError(
                f"O Ollama retornou um erro HTTP: {erro}"
            )

        except (KeyError, ValueError):
            raise RuntimeError(
                "A resposta recebida do Ollama está em formato inválido."
            )

        except Exception as erro:
            raise RuntimeError(
                f"Erro inesperado no backend: {erro}"
            )