import socket


def parse_http_request(request: bytes) -> dict:
    """Парсинг HTTP запроса"""
    request_str = request.decode('utf-8')
    lines = request_str.split('\r\n')
    start_line = lines[0].split(' ')
    method = start_line[0]
    path = start_line[1]
    version = start_line[2]
    host = lines[1]
    headers = []
    body_start = 0
    for i, line in enumerate(lines[2:], 1):
        if line == '':
            body_start = i + 1
            break
        headers.append(line)

    body = '\r\n'.join(lines[body_start:])

    return {
        'method': method,
        'path': path,
        'version': version,
        'host': host,
        'headers': headers,
        'body': body
    }


def http_response(status_code: int, body: str, content_type: str = 'text/html') -> bytes:
    """Формирование ответа"""
    status_messages = {200: 'OK', 404: 'Not Found'}
    status_message = status_messages.get(status_code, 'Unknown')
    response = f"HTTP/1.1 {status_code} {status_message}\r\n"
    response += f"Content-Type: {content_type}; charset=utf-8\r\n"
    response += f"Content-Length: {len(body.encode('utf-8'))}\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"
    response += body

    return response.encode('utf-8')


def handle_client(client_socket: socket.socket, address):
    """Обработка клиента"""

    request = b""
    while True:
        chunk = client_socket.recv(4096)
        request += chunk
        if b'\r\n\r\n' in request or not chunk:
            break

    if request:
        parsed = parse_http_request(request)
        if parsed['path'] == '/':
            body = f"<html><body>{parsed["method"]} {parsed["path"]} {parsed["version"]}<br>{parsed["host"]}<br>"
            print(
                f"{parsed["method"]} {parsed["path"]} {parsed["version"]}\n{parsed["host"]}")
            for header in parsed['headers']:
                body += f"{header}<br>"
                print(header)
            body += f"{parsed['body']}<br>"
            print(parsed['body'])
            body += "</p></body></html>"
            response = http_response(200, body)
        else:
            body = "<html><body><h1>404 Not Found</h1></body></html>"
            response = http_response(404, body)

        client_socket.send(response)
    client_socket.close()


def run_server(host: str = '127.0.0.1', port: int = 8080):
    """Запуск сервера"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"Server started on http://{host}:{port}")

    try:
        while True:
            client_socket, address = server.accept()
            handle_client(client_socket, address)
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.close()


if __name__ == '__main__':
    run_server()
