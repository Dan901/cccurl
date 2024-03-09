from cccurl.errors import INVALID_URL


def parse_protocol(url) -> tuple[str, str]:
    parts = url.split("://")
    if len(parts) != 2:
        raise ValueError(INVALID_URL)
    protocol, remaining = parts
    return protocol, remaining


def parse_host(remaining) -> tuple[str, int, str]:
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
    return host, int(port), remaining
