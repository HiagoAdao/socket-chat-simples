import pytest
from unittest.mock import patch, MagicMock
from client import iniciar_cliente

@patch("client.socket.socket")
@patch("builtins.input")
def test_iniciar_cliente_sair_via_input(mock_input, mock_socket):
    mock_sock_instance = MagicMock()
    mock_socket.return_value = mock_sock_instance
    
    mock_input.return_value = "sair"
    
    iniciar_cliente()
    
    mock_sock_instance.connect.assert_called_once_with(("localhost", 8080))
    mock_input.assert_called_once_with("> ")
    mock_sock_instance.sendall.assert_not_called()
    mock_sock_instance.close.assert_called_once()

@patch("client.socket.socket")
@patch("builtins.input")
def test_iniciar_cliente_servidor_desconecta(mock_input, mock_socket):
    mock_sock_instance = MagicMock()
    mock_socket.return_value = mock_sock_instance
    
    mock_input.return_value = "Olá Servidor"
    
    # recv voltando em branco simulando quebra
    mock_sock_instance.recv.return_value = b""
    
    iniciar_cliente()
    
    mock_input.assert_called_once_with("> ")
    mock_sock_instance.sendall.assert_called_once()
    mock_sock_instance.recv.assert_called_once_with(1024)
    mock_sock_instance.close.assert_called_once()

@patch("client.socket.socket")
@patch("builtins.input")
def test_iniciar_cliente_ciclo_completo(mock_input, mock_socket):
    mock_sock_instance = MagicMock()
    mock_socket.return_value = mock_sock_instance
    
    mock_input.side_effect = ["Mensagem Cliente", "sair"]
    
    msg_json = b'{"remetente": "Servidor", "conteudo": "Recebido"}'
    mock_sock_instance.recv.return_value = msg_json
    
    iniciar_cliente()
    
    assert mock_input.call_count == 2
    mock_sock_instance.sendall.assert_called_once()
    mock_sock_instance.recv.assert_called_once_with(1024)
    mock_sock_instance.close.assert_called_once()
