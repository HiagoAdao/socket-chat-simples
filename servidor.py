import socket
from logging import Logger
from protocolo import ChatMessage
from logger import configurar_logger, obter_logger

def iniciar_servidor() -> None:
    log_servidor: Logger = obter_logger("Servidor")

    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind(("localhost", 8080))
    servidor_socket.listen(1)

    log_servidor.info("Escutando porta 8080...")

    client_socket, endereco = servidor_socket.accept()
    log_servidor.info(f"Conectado com {endereco}")

    while True:
        dados: bytes = client_socket.recv(1024)
        if not dados:
            log_servidor.info("Conexão encerrada pelo cliente.")
            break

        msg_recebida = ChatMessage.decodificar(dados)
        obter_logger(msg_recebida.remetente).info(msg_recebida.conteudo)

        texto: str = input("> ")
        if texto.lower() == 'sair':
            break

        msg_envio = ChatMessage(remetente="Servidor", conteudo=texto)
        client_socket.sendall(msg_envio.codificar())

    client_socket.close()
    servidor_socket.close()

if __name__ == "__main__":
    configurar_logger()
    iniciar_servidor()