import pytest
from unittest.mock import patch, MagicMock
from server import iniciar_servidor

@patch("server.socket.socket")
@patch("builtins.input")
def test_iniciar_servidor_conexao_encerrada_pelo_cliente(mock_input, mock_socket):
    mock_sock_instance = MagicMock()
    mock_socket.return_value = mock_sock_instance
    
    mock_client_socket = MagicMock()
    mock_sock_instance.accept.return_value = (mock_client_socket, ("127.0.0.1", 12345))
    
    # Cliente quebra conexão -> recv volta vazio
    mock_client_socket.recv.return_value = b""
    
    iniciar_servidor()
    
    mock_sock_instance.bind.assert_called_once_with(("localhost", 8080))
    mock_sock_instance.listen.assert_called_once_with(1)
    mock_sock_instance.accept.assert_called_once()
    mock_client_socket.recv.assert_called_once_with(1024)
    mock_client_socket.sendall.assert_not_called()
    mock_client_socket.close.assert_called_once()
    mock_sock_instance.close.assert_called_once()

@patch("server.socket.socket")
@patch("builtins.input")
def test_iniciar_servidor_sair_pelo_input(mock_input, mock_socket):
    mock_sock_instance = MagicMock()
    mock_socket.return_value = mock_sock_instance
    
    mock_client_socket = MagicMock()
    mock_sock_instance.accept.return_value = (mock_client_socket, ("127.0.0.1", 12345))
    
    msg_json = b'{"remetente": "Cliente", "conteudo": "Ola"}'
    mock_client_socket.recv.side_effect = [msg_json, b""]
    
    # Servidor digita sair e fecha
    mock_input.return_value = "sair"
    
    iniciar_servidor()
    
    mock_client_socket.recv.assert_called_once_with(1024)
    mock_input.assert_called_once_with("> ")
    mock_client_socket.sendall.assert_not_called()

@patch("server.socket.socket")
@patch("builtins.input")
def test_iniciar_servidor_envia_msg_e_cliente_desconecta(mock_input, mock_socket):
    mock_sock_instance = MagicMock()
    mock_socket.return_value = mock_sock_instance
    
    mock_client_socket = MagicMock()
    mock_sock_instance.accept.return_value = (mock_client_socket, ("127.0.0.1", 12345))
    
    msg_json = b'{"remetente": "Cliente", "conteudo": "Ola"}'
    mock_client_socket.recv.side_effect = [msg_json, b""]
    
    mock_input.side_effect = ["Resposta servidor"]
    
    iniciar_servidor()
    
    assert mock_client_socket.recv.call_count == 2
    assert mock_input.call_count == 1
    mock_client_socket.sendall.assert_called_once()
    mock_client_socket.close.assert_called_once()
