import socket
from logging import Logger
from protocolo import ChatMessage
from logger import configurar_logger, obter_logger

def iniciar_cliente() -> None:
    log_cliente: Logger = obter_logger("Cliente")

    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect(("localhost", 8080))
    log_cliente.info("Conectado! (Digite 'sair' para encerrar)")

    while True:
        texto: str = input("> ")
        if texto.lower() == 'sair':
            break

        msg_envio = ChatMessage(remetente="Cliente", conteudo=texto)
        cliente_socket.sendall(msg_envio.codificar())
        
        dados: bytes = cliente_socket.recv(1024)
        if not dados:
            log_cliente.info("Conexão encerrada pelo servidor.")
            break

        msg_recebida = ChatMessage.decodificar(dados)
        obter_logger(msg_recebida.remetente).info(msg_recebida.conteudo)

    cliente_socket.close()

if __name__ == "__main__":
    configurar_logger()
    iniciar_cliente()
