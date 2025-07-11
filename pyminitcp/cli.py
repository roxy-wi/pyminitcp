import argparse

from pyminitcp import tcp_check, udp_check


def main():
    parser = argparse.ArgumentParser(
        description="Simple TCP/UDP connectivity checker (IPv4/IPv6/domain)"
    )
    parser.add_argument("host", help="Host to check (IP or domain)")
    parser.add_argument("port", type=int, help="TCP port number to check")
    parser.add_argument("-t", "--timeout", type=int, default=3, help="Timeout in seconds (default: 3)")
    parser.add_argument("--tcp", action="store_true", default=True, help="Do TCP check. By default")
    parser.add_argument("--udp", action="store_true", default='', help="Do UDP check")
    parser.add_argument("-p", "--payload", type=str, default=b'', help="Payload to send in UDP check")
    parser.add_argument("--hex-payload", type=str, default=None, help="Hex payload to send in UDP check")
    parser.add_argument("-j", "--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()

    if args.udp:
        result = udp_check(args.host, args.port, args.timeout, args.payload, args.hex_payload)
        check_type = 'udp'
    else:
        result = tcp_check(args.host, args.port, args.timeout)
        check_type = 'tcp'

    if args.json:
        import json
        print(json.dumps(result.as_dict(), indent=2, default=str))
    else:
        print(result)


if __name__ == "__main__":
    main()
