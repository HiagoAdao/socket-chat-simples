import json
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class ChatMessage:
    remetente: str
    conteudo: str

    def codificar(self) -> bytes:
        """Codifica a mensagem para bytes em formato JSON."""
        return json.dumps(asdict(self)).encode('utf-8')

    @staticmethod
    def decodificar(dados: bytes) -> 'ChatMessage':
        """Decodifica os bytes JSON para um objeto ChatMessage."""
        dicionario: dict = json.loads(dados.decode('utf-8'))
        return ChatMessage(**dicionario)
