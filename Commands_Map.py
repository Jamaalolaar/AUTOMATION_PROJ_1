from Folder_Sorter_OOP import Directory_Manager, File_Manager, Path
from Config_Manager import ConfigManager
from Logger_Manager import LoggerManager
from Command_Line import parse_cli_arguments
import argparse

Config = ConfigManager()
Logger = LoggerManager(Config)
DM = Directory_Manager(Logger)
Cryptium = File_Manager(Config, Logger, DM)
extensions = Config.config_data
args = parse_cli_arguments()
overrides = extract_overrides(args)
Config.load_overrides(overrides)

def rename_cmd():
    Cryptium.rename_file(args.file_name, args.new_name)
def sort_cmd():
    if args.target:
        Cryptium.base_path = Cryptium.base_path / args.target
    else: pass
    print(Cryptium.base_path)
    Cryptium.fold_file_by_extension(Cryptium.base_path)
def unsort_cmd():
    if args.target:
        Cryptium.base_path = Cryptium.base_path / args.target
    else: pass
    print(Cryptium.base_path)
    Cryptium.unfold_files(Cryptium.base_path)

