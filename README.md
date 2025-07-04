# pyminitcp

![PyPI version](https://img.shields.io/pypi/v/pyminitcp)
![Build status](https://github.com/roxy-wi/pyminitcp/actions/workflows/ci.yml/badge.svg)
![Python versions](https://img.shields.io/pypi/pyversions/pyminitcp)
![License](https://img.shields.io/pypi/l/pyminitcp)

A tiny, dependency-free Python library for TCP connectivity checks with IPv4/IPv6 and DNS support.

## Features

- Checks TCP connectivity for IPv4, IPv6, or domain names
- Distinguishes between address families automatically
- Returns response time and detailed error info

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

## CLI Usage

```sh
pyminitcp google.com 443
pyminitcp 8.8.8.8 53 --timeout 1
pyminitcp --json example.com 80
```

