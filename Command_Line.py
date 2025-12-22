import argparse

def parse_cli_arguments():
    parser = argparse.ArgumentParser(prog="Cryptium Manager",description="Cryptium Manager, a tool to manage files and folders.")
    parser.add_argument("--v","--version", action="version", version="Cryptium Manager 1.0.0")
    subparsers = parser.add_subparsers(dest="command", required="True")
    sort_parser = subparsers.add_parser("sort")
    sort_parser.add_argument("--dry-run", action="store_true", help="Simulate the actions without making any changes.")
    sort_parser.add_argument("--target", type=str)
    #metavar
    return parser.parse_args()