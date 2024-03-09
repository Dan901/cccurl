import argparse

from cccurl.http_requests import get


def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    url = args.url
    get(url)


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
    return parser


if __name__ == "__main__":
    main()
