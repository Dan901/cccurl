import socket
from typing import List

from cccurl.socket_utils import receive, send
from cccurl.url_parser import parse_url

OUTBOUND = ">"
INBOUND = "<"


def get(url: str, headers: List[str], verbose: bool):
    _handle_request(url, method="GET", headers=headers, verbose=verbose)


def delete(url: str, headers: List[str], verbose: bool):
    _handle_request(url, method="DELETE", headers=headers, verbose=verbose)


def post(url: str, headers: List[str], data: str, verbose: bool):
    _handle_request(url, method="POST", headers=headers, data=data, verbose=verbose)


def put(url: str, headers: List[str], data: str, verbose: bool):
    _handle_request(url, method="PUT", headers=headers, data=data, verbose=verbose)


def _handle_request(
    url: str, method: str, headers: List[str], verbose: bool, data: str = None
):
    host, port, path = parse_url(url)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    _send_request(
        method=method,
        headers=headers,
        verbose=verbose,
        data=data,
        path=path,
        host=host,
        sock=sock,
    )
    _receive_response(verbose=verbose, sock=sock)


def _send_request(
    method: str,
    headers: List[str],
    verbose: bool,
    data: str,
    path: str,
    host: str,
    sock: socket.socket,
):
    encoded_data = data.encode() if data else None
    if data:
        headers.append(f"Content-Length: {len(encoded_data)}")
    request_headers = "\r\n".join(headers) + "\r\n" if headers else ""
    request = (
        f"{method} {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "Accept: */*\r\n"
        "Connection: close\r\n"
        f"{request_headers}"
        "\r\n"
    )
    if verbose:
        formatted_request = _append_to_each_line(request, OUTBOUND)
        print(f"{formatted_request}", end="")
    send(sock, request.encode())
    if data:
        send(sock, encoded_data)


def _receive_response(verbose: bool, sock: socket.socket):
    response_headers, content = receive(sock)
    if verbose:
        formatted_headers = _append_to_each_line(response_headers, INBOUND)
        print(f"{formatted_headers}", end="")
    print(f"{content}", end="")


def _append_to_each_line(text: str, prefix: str) -> str:
    return "".join(f"{prefix} {line}" for line in text.splitlines(keepends=True))
