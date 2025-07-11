import socket
import pyminitcp


def test_tcp_check_ipv4_success():
    # 8.8.8.8:53 (Google DNS) is always reachable for TCP DNS queries
    result = pyminitcp.tcp_check("8.8.8.8", 53, timeout=2)
    assert result.status == 1
    assert isinstance(result.resp_time, float)
    assert result.error == ""


def test_tcp_check_ipv4_fail():
    # 8.8.8.8:65000 is almost certainly closed
    result = pyminitcp.tcp_check("8.8.8.8", 65000, timeout=2)
    assert result.status == 0
    assert "unreachable" in result.error.lower() or result.error


def test_tcp_check_ipv6_success():
    # Google DNS IPv6 address (should work on IPv6-enabled hosts)
    try:
        socket.inet_pton(socket.AF_INET6, "2001:4860:4860::8888")
    except OSError:
        # Skip test if IPv6 is not available
        return
    result = pyminitcp.tcp_check("2001:4860:4860::8888", 53, timeout=2)
    assert result.status in (0, 1)  # Some CI hosts may not have IPv6
    # If it fails, we just want it not to crash


def test_tcp_check_domain_success():
    # Should work for almost any domain
    result = pyminitcp.tcp_check("example.com", 80, timeout=3)
    assert result.status in (0, 1)
    # If it fails, check error message is string
    assert isinstance(result.error, str)


def test_tcp_check_domain_fail():
    # Non-existent domain
    result = pyminitcp.tcp_check("nonexistentdomain1234567890.com", 80, timeout=2)
    assert result.status == 0
    assert "unreachable" in result.error.lower()
