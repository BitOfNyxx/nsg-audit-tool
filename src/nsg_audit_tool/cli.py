import argparse
from importlib.metadata import PackageNotFoundError, version


def _package_version() -> str:
    try:
        return version("nsg-audit-tool")
    except PackageNotFoundError:
        return "unknown"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nsg-audit",
        description="Audit Azure Network Security Group rules for risky configurations.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"nsg-audit-tool {_package_version()}",
    )
    parser.add_argument(
        "--output-format",
        choices=["json", "csv", "markdown"],
        default="json",
        help="Output format for the audit report (default: json).",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    print(f"Selected output format: {args.output_format}")


if __name__ == "__main__":
    main()
