from dataclasses import dataclass, asdict
import socket
from contextlib import closing
import time

__all__ = ["tcp_check", "udp_check", "CheckResult"]


# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'


@dataclass
class CheckResult:
    """
    Result of TCP and UDP connectivity check.
    """
    status: int         # 1 for success, 0 for failure
    resp_time: float    # Response time in s, or 0 if failed
    error: str          # Error description or empty string if success
    family: object      # socket.AF_INET or socket.AF_INET6 (or None)
    sockaddr: object    # Tuple (ip, port) or None
    namelookup_time: float = 0.0
    connect_time: float = 0.0

    def as_dict(self):
        return asdict(self)

    def __str__(self):
        status_str = f"{GREEN}Success{RESET}" if self.status else f"{RED}Failure{RESET}"
        error_str = f"{RED}{self.error}{RESET}" if self.error else f"{GREEN}-{RESET}"
        return (
            f"{BOLD}{CYAN}Status        :{RESET} {status_str}\n"
            f"{BOLD}{CYAN}Name lookup ms:{RESET} {YELLOW}{self.namelookup_time if self.status else 'N/A'}{RESET}\n"
            f"{BOLD}{CYAN}Connect ms    :{RESET} {YELLOW}{self.connect_time if self.status else 'N/A'}{RESET}\n"
            f"{BOLD}{CYAN}Response ms   :{RESET} {YELLOW}{self.resp_time if self.status else 'N/A'}{RESET}\n"
            f"{BOLD}{CYAN}Error         :{RESET} {error_str}\n"
            f"{BOLD}{CYAN}Family        :{RESET} {self.family}\n"
            f"{BOLD}{CYAN}Sockaddr      :{RESET} {self.sockaddr}\n"
        )


def format_socket_error(exc: Exception) -> str:
    """
    Returns a human-readable description of socket exceptions.
    """
    if isinstance(exc, socket.timeout):
        return "Connection timed out"
    if isinstance(exc, socket.gaierror):
        return f"Address-related error: {exc}"
    if isinstance(exc, socket.herror):
        return f"Host-related error: {exc}"
    if isinstance(exc, OSError):
        return f"OS/socket error: {exc}"
    return str(exc)


def tcp_check(host: str, port: int, timeout: int = 10) -> CheckResult:
    """
    Perform a TCP connectivity check for an IPv4/IPv6 address or domain.

    Args:
        host (str): Hostname or IP address.
        port (int): TCP port to check.
        timeout (int, optional): Timeout in seconds. Defaults to 3.

    Returns:
        CheckResult: The result of the check.
    """
    port = int(port)
    last_err = ''
    start = time.time()
    try:
        infos = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)
        dns_time = (time.time() - start)
    except (socket.gaierror, socket.herror, OSError) as e:
        # Couldn't resolve or connect — return as failure
        return CheckResult(0, 0, format_socket_error(e), None, None)

    # Try all addresses for the host (IPv4/IPv6, etc)
    for family, socktype, proto, canonname, sockaddr in infos:
        try:
            with closing(socket.socket(family, socket.SOCK_STREAM, proto)) as sock:
                sock.settimeout(timeout)
                connect_start = time.time()
                res = sock.connect_ex(sockaddr)
                connect_time = (time.time() - connect_start)
                elapsed = (time.time() - start)
                if res == 0:
                    return CheckResult(1, elapsed, '', family, sockaddr, dns_time, connect_time)
                else:
                    last_err = 'Port is unreachable'
        except (socket.timeout, socket.gaierror, socket.herror, OSError) as e:
            last_err = format_socket_error(e)
            continue
    return CheckResult(0, 0, last_err or 'Port is unreachable', None, None)


def udp_check(host: str, port: int, timeout: int = 10, payload: bytes = b"", hex_payload: str = None) -> CheckResult:
    """
    Perform a UDP connectivity check for an IPv4/IPv6 address or domain.

    Args:
        host (str): Hostname or IP address.
        port (int): UDP port to check.
        timeout (int, optional): Timeout in seconds. Defaults to 3.
        payload (bytes, optional): Payload to send. Defaults to b"".
        hex_payload (str, optional): Hex payload to send. Defaults to b"".

    Returns:
        CheckResult: The result of the check.
    """
    port = int(port)
    last_err = ''
    if hex_payload:
        try:
            payload = bytes.fromhex(hex_payload)
        except ValueError:
            return CheckResult(0, 0, "Invalid hex payload", None, None)
    try:
        start_dns = time.time()
        infos = socket.getaddrinfo(host, port, 0, socket.SOCK_DGRAM)
        dns_time = (time.time() - start_dns) * 1000
    except (socket.gaierror, socket.herror, OSError) as e:
        # Couldn't resolve or connect — return as failure
        return CheckResult(0, 0, format_socket_error(e), None, None)

    # Try all addresses for the host (IPv4/IPv6, etc)
    for family, socktype, proto, canonname, sockaddr in infos:
        try:
            with closing(socket.socket(family, socket.SOCK_DGRAM, proto)) as sock:
                sock.settimeout(timeout)
                start = time.time()
                # Try to send zero bytes (safe for most UDP services)
                sock.sendto(payload, sockaddr)
                # Try to receive a response (will succeed if service answers, e.g. DNS/ntp)
                sock.recvfrom(1024)
                elapsed = (time.time() - start) * 1000
                return CheckResult(1, elapsed, '', family, sockaddr, dns_time)
        except (socket.timeout, socket.gaierror, socket.herror, OSError) as e:
            last_err = format_socket_error(e)
            continue
    return CheckResult(0, 0, last_err or 'Port is unreachable', None, None)
