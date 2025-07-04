from dataclasses import dataclass, asdict
import socket
from contextlib import closing
import time

__all__ = ["tcp_check", "TcpCheckResult"]


@dataclass
class TcpCheckResult:
    """
    Result of TCP connectivity check.
    """
    status: int         # 1 for success, 0 for failure
    resp_time: float    # Response time in ms, or '' if failed
    error: str          # Error description or empty string if success
    family: object      # socket.AF_INET or socket.AF_INET6 (or None)
    sockaddr: object    # Tuple (ip, port) or None

    def as_dict(self):
        return asdict(self)


def format_socket_error(exc: Exception) -> str:
    """
    Returns a human-readable description of socket exceptions.
    """
    if isinstance(exc, socket.timeout):
        return "Connection timed out"
    if isinstance(exc, socket.gaierror):
        return f"Address-related error (gaierror): {exc}"
    if isinstance(exc, socket.herror):
        return f"Host-related error (herror): {exc}"
    if isinstance(exc, OSError):
        return f"OS/socket error: {exc}"
    return str(exc)


def tcp_check(host: str, port: int, timeout: int = 3) -> TcpCheckResult:
    """
    Universal TCP connectivity check for IPv4/IPv6 addresses or domains.
    Returns TcpCheckResult dataclass.
    """
    port = int(port)
    last_err = ''
    # Try all addresses for the host (IPv4/IPv6, etc)
    for family, socktype, proto, canonname, sockaddr in socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM):
        try:
            with closing(socket.socket(family, socket.SOCK_STREAM, proto)) as sock:
                sock.settimeout(timeout)
                start = time.time()
                res = sock.connect_ex(sockaddr)
                elapsed = (time.time() - start) * 1000
                if res == 0:
                    return TcpCheckResult(1, elapsed, '', family, sockaddr)
                else:
                    last_err = 'Port is unreachable'
        except (socket.timeout, socket.gaierror, socket.herror, OSError) as e:
            last_err = format_socket_error(e)
            continue
    return TcpCheckResult(0, '', last_err or 'Port is unreachable', None, None)
