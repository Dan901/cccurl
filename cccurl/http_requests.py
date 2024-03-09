import socket
from cccurl.errors import INVALID_URL, PROTOCOL_NOT_SUPPORTED

from cccurl.socket_utils import send_request
from cccurl.url_parser import parse_host, parse_protocol

OUTBOUND = ">"
INBOUND = "<"


def get(url: str, verbose: bool = False):
    _handle_request(url, "GET", verbose)


def delete(url: str, verbose: bool = False):
    _handle_request(url, "DELETE", verbose)


def _handle_request(url: str, method: str, verbose: bool):
    protocol, remaining = parse_protocol(url)
    if protocol != "http":
        raise ValueError(PROTOCOL_NOT_SUPPORTED)
    if not remaining:
        raise ValueError(INVALID_URL)
    host, port, remaining = parse_host(remaining)
    request = (
        f"{method} {remaining} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "Accept: */*\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    if verbose:
        formatted_request = _append_to_each_line(request, OUTBOUND)
        print(f"{formatted_request}", end="")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    headers, content = send_request(s, request)
    if verbose:
        formatted_headers = _append_to_each_line(headers, INBOUND)
        print(f"{formatted_headers}", end="")
    print(f"{content}", end="")


def _append_to_each_line(text: str, prefix: str) -> str:
    return "".join(f"{prefix} {line}" for line in text.splitlines(keepends=True))
