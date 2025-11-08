# ===============================================
# Servidor Web do Zero em Python (com explicações)
# ===============================================
import settings
import socket  # Módulo da biblioteca padrão para comunicação em rede (TCP/UDP)
from core.exceptions.exceptions import BaseError, InternalServerError
from core.http.request import RequestResolver
from routes.urls import router


# ----------------------------
# CRIANDO E CONFIGURANDO O SOCKET
# ----------------------------

# Criamos um socket TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Permite reusar o mesmo endereço e porta rapidamente (sem "Address already in use")
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Ligamos (bind) o socket ao endereço e porta definidos acima
server_socket.bind((settings.SERVER_HOST, settings.SERVER_PORT))

# Colocamos o socket em modo de escuta (listen)
# O parâmetro (5) define quantas conexões podem ficar na fila de espera
server_socket.listen(5)


def main():

    print(
        f"Running server at http://{settings.SERVER_HOST}:{settings.SERVER_PORT}")

    while True:
        client_conn, client_addr = server_socket.accept()
        data = client_conn.recv(1024)

        if not data:
            client_conn.close()
            continue

        try:
            request_resolver = RequestResolver(data, router)
            response = request_resolver.resolve()
        except BaseError as error:

            response = error.to_json()

        client_conn.sendall(response.send())
        client_conn.close()


# (nunca chega aqui porque o loop é infinito)
if __name__ == '__main__':
    main()
