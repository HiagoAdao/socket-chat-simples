import json
import pytest
from protocol import ChatMessage

def test_chat_message_codificar():
    msg = ChatMessage(remetente="Alice", conteudo="Olá")
    resultado = msg.codificar()
    
    assert isinstance(resultado, bytes)
    dicionario = json.loads(resultado.decode('utf-8'))
    assert dicionario["remetente"] == "Alice"
    assert dicionario["conteudo"] == "Olá"

def test_chat_message_decodificar():
    dados_bytes = json.dumps({"remetente": "Bob", "conteudo": "Teste"}).encode('utf-8')
    msg = ChatMessage.decodificar(dados_bytes)
    
    assert isinstance(msg, ChatMessage)
    assert msg.remetente == "Bob"
    assert msg.conteudo == "Teste"
