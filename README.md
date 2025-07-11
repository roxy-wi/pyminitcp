# pyminitcp

![PyPI version](https://img.shields.io/pypi/v/pyminitcp)
![Build status](https://github.com/roxy-wi/pyminitcp/actions/workflows/ci.yml/badge.svg)
![Python versions](https://img.shields.io/pypi/pyversions/pyminitcp)
![License](https://img.shields.io/pypi/l/pyminitcp)

A tiny, dependency-free Python library for TCP connectivity checks with IPv4/IPv6 and DNS support.

## Features

- Checks TCP connectivity for IPv4, IPv6, or domain names
- UDP check with custom payload (hex-encoded for raw protocols)
- Distinguishes between address families automatically
- Returns name lookup, connect and response time, and detailed error info

## Usage

```python
from pyminitcp import tcp_check

result = tcp_check('google.com', 443)
print(result.as_dict())
```

## Result
```python
{
  "status": 1,
  "resp_time": 10.468006134033203,
  "error": "",
  "family": 2,
  "sockaddr": [
    "74.125.205.139",
    80
  ]
}
```

```python
from pyminitcp import udp_check

result = udp_check('8.8.8.8', 53, hex_payload='1234010000010000000000000000010001')
print(result.as_dict())
```

## Result
```python
{
  "status": 1,
  "resp_time": 113.9225959777832,
  "error": "",
  "family": 2,
  "sockaddr": [
    "8.8.8.8",
    53
  ]
}
```

## CLI Usage

```sh
pyminitcp google.com 443
pyminitcp 8.8.8.8 53 --timeout 1
pyminitcp --json example.com 80
```

### UDP check with custom payload (e.g. DNS query)

```shell
pyminitcp --udp --hex-payload aabb0100000100000000000006676f6f676c6503636f6d0000010001 8.8.8.8 53
```
This sends a minimal DNS A query for google.com to 8.8.8.8 UDP:53.

### Root zone DNS query

```shell
pyminitcp --udp --hex-payload 1234010000010000000000000000010001 8.8.8.8 53
```
This sends a minimal DNS query for the root zone (".") to Google DNS.

