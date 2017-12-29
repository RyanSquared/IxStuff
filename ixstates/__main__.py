"Set values for, and start, the Tornado app. "
# pylint: disable=invalid-name
import argparse
import socket
import tornado.log
from tornado.ioloop import IOLoop
from ixstates.tornado_app import make_server


def is_socket_addr(address):
    "Check if an address is valid IPv4 or IPv6"
    try:
        socket.inet_pton(socket.AF_INET, address)
        return address
    except socket.error:  # not a valid address
        try:
            socket.inet_pton(socket.AF_INET6, address)
        except socket.error:
            raise argparse.ArgumentTypeError(
                "Not a valid host address", address)
    return address


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ixstates",
        description="Set values for, and start, the Tornado app.")
    parser.add_argument(
        "--port", "-p", help="Server port", type=int,
        default=5000)
    parser.add_argument(
        "--bind", "-b", help="Server bind address", type=is_socket_addr,
        default="0.0.0.0")
    parser.add_argument(
        "--certfile", help="TLS Certificate File (PEM), requires --keyfile")
    parser.add_argument(
        "--keyfile", help="TLS Private Key File (PEM), requires --certfile")
    parser.add_argument("-v", help="Enable Tornado verbose logging",
                        action="store_true")
    args = parser.parse_args()
    if args.v is not None:
        tornado.log.enable_pretty_logging()

    if args.certfile and args.keyfile:  # Both exist
        tls_options = {
            "certfile": args.certfile,
            "keyfile": args.keyfile}
    elif args.certfile or args.keyfile:  # Either exist, but not both
        parser.print_usage()
        raise SystemExit()
    else:
        tls_options = None

    if tls_options is None:
        http_server = make_server()
    else:
        http_server = make_server(ssl_options=tls_options)

    http_server.bind(args.port)
    http_server.start(0)
    IOLoop.instance().start()
