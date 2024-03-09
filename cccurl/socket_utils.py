import socket

from cccurl.errors import CONNECTION_CLOSED, MISSING_CONTENT_LENGTH

BUFFER_SIZE = 4096


def send_request(socket: socket.socket, request: str) -> tuple[str, str]:
    socket.sendall(request.encode())
    response = _receive_response(socket)
    return response


def _receive_response(socket: socket.socket) -> tuple[str, str]:
    response = bytearray()
    headers_received = False
    while True:
        data = socket.recv(BUFFER_SIZE)
        if not data:
            raise ValueError(CONNECTION_CLOSED)
        response.extend(data)
        if not headers_received:
            headers, sep, rest = response.partition(b"\r\n\r\n")
            if sep:
                headers_received = True
                content_length = _parse_content_length(headers)
                content = bytearray(rest)
                headers.extend(sep)
        if headers_received and len(response) >= content_length:
            break
    return headers.decode(), content.decode()


def _parse_content_length(headers: bytearray) -> int:
    for header in headers.split(b"\r\n"):
        name, sep, value = header.partition(b": ")
        if name.lower() == b"content-length":
            return int(value)
    raise ValueError(MISSING_CONTENT_LENGTH)
