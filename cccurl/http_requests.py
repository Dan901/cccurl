INVALID_URL = "Invalid URL format"


def get(url: str):
    protocol, remaining = _parse_protocol(url)
    if protocol != "http":
        raise ValueError("Only HTTP protocol is supported")
    if not remaining:
        raise ValueError(INVALID_URL)
    host, port, remaining = _parse_host(remaining)
    print(f"connecting to {host}")
    print(f"Sending request GET {remaining} HTTP/1.1")
    print(f"Host: {host}")
    print("Accept: */*")


def _parse_protocol(url) -> tuple[str, str]:
    parts = url.split("://")
    if len(parts) != 2:
        raise ValueError(INVALID_URL)
    protocol, remaining = parts
    return protocol, remaining


def _parse_host(remaining) -> tuple[str, str, str]:
    parts = remaining.split("/", maxsplit=2)
    host = parts[0]
    remaining = "/" + (parts[1] if len(parts) > 1 else "")
    host_parts = host.split(":")
    if len(host_parts) > 2:
        raise ValueError(INVALID_URL)
    if len(host_parts) == 2:
        host, port = host_parts
    else:
        port = 80
    return host, port, remaining
