from cccurl.errors import INVALID_URL, PROTOCOL_NOT_SUPPORTED


def parse_url(url) -> tuple[str, int, str]:
    protocol, remaining = _parse_protocol(url)
    if protocol != "http":
        raise ValueError(PROTOCOL_NOT_SUPPORTED)
    if not remaining:
        raise ValueError(INVALID_URL)
    return _parse_host(remaining)


def _parse_protocol(url) -> tuple[str, str]:
    parts = url.split("://")
    if len(parts) != 2:
        raise ValueError(INVALID_URL)
    protocol, remaining = parts
    return protocol, remaining


def _parse_host(remaining) -> tuple[str, int, str]:
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
