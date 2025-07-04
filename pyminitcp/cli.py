import argparse
from pyminitcp import tcp_check

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'


def main():
    parser = argparse.ArgumentParser(
        description="Simple TCP connectivity checker (IPv4/IPv6/domain)"
    )
    parser.add_argument("host", help="Host to check (IP or domain)")
    parser.add_argument("port", type=int, help="TCP port number to check")
    parser.add_argument("-t", "--timeout", type=int, default=3, help="Timeout in seconds (default: 3)")
    parser.add_argument("-j", "--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()

    result = tcp_check(args.host, args.port, args.timeout)

    if args.json:
        import json
        print(json.dumps(result.as_dict(), indent=2, default=str))
    else:
        status_str = f"{GREEN}Success{RESET}" if result.status else f"{RED}Failure{RESET}"
        error_str = f"{RED}{result.error}{RESET}" if result.error else f"{GREEN}-{RESET}"

        print(f"{BOLD}{CYAN}Check type  :{RESET} TCP")
        print(f"{BOLD}{CYAN}Host        :{RESET} {args.host}")
        print(f"{BOLD}{CYAN}Port        :{RESET} {args.port}")
        print(f"{BOLD}{CYAN}Status      :{RESET} {status_str}")
        print(f"{BOLD}{CYAN}Response ms :{RESET} {YELLOW}{result.resp_time if result.status else 'N/A'}{RESET}")
        print(f"{BOLD}{CYAN}Error       :{RESET} {error_str}")
        print(f"{BOLD}{CYAN}Family      :{RESET} {result.family}")
        print(f"{BOLD}{CYAN}Sockaddr    :{RESET} {result.sockaddr}")


if __name__ == "__main__":
    main()
