from Folder_Sorter_OOP import Directory_Manager, File_Manager, Path
from Config_Manager import ConfigManager
from Logger_Manager import LoggerManager
from Command_Line import parse_cli_arguments
import argparse

Config = ConfigManager()
Logger = LoggerManager(Config)
DM = Directory_Manager(Logger)
Cryptium = File_Manager(Config, Logger, DM)
args = parse_cli_arguments()

def rename_cmd(args):
    Cryptium.rename_file(args.file_name, args.new_name)
def sort_cmd(args):
    if args.target:
        Cryptium.base_path = Cryptium.base_path / args.target
    else: pass
    print(Cryptium.base_path)
    Cryptium.fold_file_by_extension(Cryptium.base_path)
def unsort_cmd(args):
    if args.target:
        Cryptium.base_path = Cryptium.base_path / args.target
    else: pass
    print(Cryptium.base_path)
    Cryptium.unfold_files(Cryptium.base_path)
def find_cmd(args):
    Cryptium.find_file(args.file_name, Path(args.target)    if args.target else None)
def delete_cmd(args):
    Cryptium.delete_file(args.file_name, Path(args.target)  if args.target else None)
def move_cmd(args):
    Cryptium.move_file(args.file_name, args.destination)
def delete_empty_dirs_cmd(args):    
    if args.target:
        Cryptium.base_path = Cryptium.base_path / args.target
    else: pass  
    Cryptium.directory.delete_empty(Cryptium.base_path)
def create_folder_cmd(args):
    if args.parent:
        if Path(args.parent).is_dir():
            parent_path = Path(args.parent)
        else:
            parent_path = Cryptium.base_path / args.parent
    else:
        parent_path = Cryptium.base_path
    Cryptium.directory.create_dir(parent_path / args.folder_name)

