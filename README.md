# Socket Chat (Ping-Pong)

Um exemplo minimalista de comunicação Cliente-Servidor utilizando Sockets puros em Python, projetado para fins didáticos na disciplina de Computação Distribuída.

## 📌 Arquitetura

O chat funciona utilizando um modelo **Sequencial (Ping-Pong)** bloqueante:
- O **Cliente** inicia a conversa, conectando-se e enviando a primeira mensagem.
- O **Servidor** fica aguardando (`recv`), recebe a mensagem, registra no log a tela e então abre o próprio terminal (`input`) aguardando a digitação de uma resposta.
- O fluxo se repete alternadamente até que qualquer uma das partes digite `sair`.

Este modelo foi escolhido por ser intencionalmente simplificado (sem uso de concorrência ou *threads*) com o objetivo de demonstrar os conceitos mais básicos de redes TCP (`bind`, `listen`, `accept`, `connect`, `sendall` e `recv`).

## 📂 Estrutura de Arquivos

* **`protocol.py`**: Define o formato da mensagem trafegada pela rede. Utiliza `@dataclass` para modelar de forma semântica a classe `ChatMessage`, abstraindo a conversão do objeto Python para `bytes` em formato JSON e vice-versa. Segue as boas práticas de tipagem estrita do Python 3.12+.
* **`logger.py`**: Um módulo auxiliar que configura e fornece acesso à biblioteca nativa `logging` do Python. Padroniza a saída do terminal no formato `[HORARIO] [TIPO] Mensagem`.
* **`server.py`**: Aplicação que sobe a porta TCP `8080`, aceita uma conexão e gerencia as respostas do lado do servidor.
* **`client.py`**: Aplicação que se conecta na porta TCP `8080` de `localhost` e gerencia as mensagens do lado do cliente.

## 🚀 Como Executar

Para simular o chat interativo, abra **dois terminais** no diretório atual.

**Terminal 1 (rodar primeiro):**
```bash
python server.py
```

**Terminal 2:**
```bash
python client.py
```

### Exemplo de Interação
1. Ambos os terminais registrarão logs de inicialização, por exemplo: `[14:45:00] [Servidor] Conectado com ...`.
2. No terminal do cliente, você verá um prompt `> `. Digite algo como `Olá Servidor!` e pressione `Enter`.
3. Alterne para o terminal do servidor. A mensagem aparecerá registrada de forma estruturada: `[14:45:10] [Cliente] Olá Servidor!`.
4. Digite sua resposta no servidor e pressione `Enter`. O ciclo continua.
5. Para finalizar, basta digitar `sair` em qualquer um dos lados, e a conexão será encerrada graciosamente.
