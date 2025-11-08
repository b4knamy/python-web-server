
import settings
import socket
from core.exceptions.exceptions import BaseError, InternalServerError
from core.http.request import RequestResolver
from routes.urls import router



server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((settings.SERVER_HOST, settings.SERVER_PORT))

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


if __name__ == '__main__':
    main()
