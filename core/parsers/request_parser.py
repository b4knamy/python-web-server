def parse_http_request(request_data: bytes):
    """
    Recebe os bytes da requisição HTTP e retorna um dicionário com:
    - method (GET, POST, etc)
    - path (/index, /api, etc)
    - version (HTTP/1.1)
    - headers (dict)
    - body (string)
    """

    # 1. Converte de bytes -> string
    text = request_data.decode("utf-8", errors="ignore")

    # 2. Divide o cabeçalho e o corpo
    #    A requisição HTTP separa os dois com uma linha em branco (\r\n\r\n)
    parts = text.split("\r\n\r\n", 1)
    head = parts[0]
    body = parts[1] if len(parts) > 1 else ""

    # 3. Divide o cabeçalho em linhas
    lines = head.split("\r\n")

    # 4. Primeira linha: método, caminho, versão
    request_line = lines[0]
    method, path, version = request_line.split(" ")

    # 5. Cabeçalhos: as linhas seguintes até a linha em branco
    headers = {}
    for line in lines[1:]:
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key.lower()] = value

    # Retorna um dicionário com as partes da requisição
    return {
        "method": method,
        "path": path,
        "version": version,
        "headers": headers,
        "body": body,
    }
