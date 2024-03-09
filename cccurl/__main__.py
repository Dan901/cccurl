import argparse

from cccurl.http_requests import delete, get, post, put


def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    url = args.url
    method = args.request
    if not method or method == "GET":
        get(url, headers=args.header, verbose=args.verbose)
    if method == "DELETE":
        delete(url, headers=args.header, verbose=args.verbose)
    if method == "POST":
        post(url, headers=args.header, data=args.data, verbose=args.verbose)
    if method == "PUT":
        put(url, headers=args.header, data=args.data, verbose=args.verbose)


def create_arg_parser():
    parser = argparse.ArgumentParser(
        prog="cccurl",
        description=(
            "curl clone focused on making HTTP requests. "
            "Supported methods are GET, DELETE, POST and PUT."
        ),
    )
    parser.add_argument(
        "url",
        help="HTTP URL to make the request to.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Prints the request and response headers.",
    )
    parser.add_argument(
        "-X",
        "--request",
        help="Change the method to use.",
        choices=["GET", "DELETE", "POST", "PUT"],
    )
    parser.add_argument(
        "-d",
        "--data",
        help="Data to send in the body of the request.",
    )
    parser.add_argument(
        "-H",
        "--header",
        help="Add a header to the request.",
        action="append",
    )
    return parser


if __name__ == "__main__":
    main()
