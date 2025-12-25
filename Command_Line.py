import argparse
from pathlib import Path
def parse_cli_arguments():
    parser = argparse.ArgumentParser(prog="Cryptium Manager",description="Cryptium Manager, a tool to manage files and folders.")
    parser.add_argument("--v","--version", action="version", version="Cryptium Manager 1.0.0")
    subparsers = parser.add_subparsers(dest="command", required="True")
    sort_parser = subparsers.add_parser("sort")
    sort_parser.add_argument("--dry-run", action="store_true", help="Simulate the actions without making any changes.")
    sort_parser.add_argument("--target", type=str)

    unsort_parser = subparsers.add_parser("unsort")
    unsort_parser.add_argument("--dry-run", action="store_true", help="Simulate the actions without making any changes.")
    unsort_parser.add_argument("--target", type=str)

    rename_parser = subparsers.add_parser("rename")
    rename_parser.add_argument("file_name", type=str, help="Name of the file to be renamed (without extension).")
    rename_parser.add_argument("new_name", type=str, help="New name for the file (with or without extension).")

    find_parser = subparsers.add_parser("find")
    find_parser.add_argument("file_name", type=str, help="Name of the file to be found (without extension).")
    find_parser.add_argument("--target", type=str, help= "Directory to search in (relative to base path).")

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("file_name", type=str, help="Name of the file to be deleted (without extension).")
    delete_parser.add_argument("--target", type=str, help= "Directory to search in (relative to base path).")

    #metavar
    return parser.parse_args()