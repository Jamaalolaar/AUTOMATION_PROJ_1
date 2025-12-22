from Folder_Sorter_OOP import Directory_Manager, File_Manager
from Config_Manager import ConfigManager
from Logger_Manager import LoggerManager
from Command_Line import parse_cli_arguments


def extract_overrides(args):
    return {
        key: value
        for key, value in vars(args).items()
        if value is not None and key != "command"
    }

def main():
    
    Config = ConfigManager()
    Logger = LoggerManager(Config)
    DM = Directory_Manager(Logger)
    FM = File_Manager(Config, Logger, DM)
    extensions = Config.config_data
    args = parse_cli_arguments()
    overrides = extract_overrides(args)
    Config.load_overrides(overrides) #Load CLI overrides into config manager

    
    if __name__ == "__main__":
        try:
            Sorter = FM
            if args.command == "sort":
                if args.target:
                    Sorter.base_path = Sorter.base_path / args.target
                else: pass
                print(Sorter.base_path)
                Sorter.fold_file_by_extension(Sorter.base_path)
            elif args.command == "unsort":
                if args.target:
                    Sorter.base_path = Sorter.base_path / args.target
                else: pass
                print(Sorter.base_path)
                Sorter.unfold_files(Sorter.base_path)
                
            #Sorter.fold_file_by_extension()
            #Sorter.directory.delete_empty(Sorter.base_path)
            #Sorter.rename_file(input("Enter the name of the file to be renamed: "))
            #Sorter.unfold_files(Sorter.base_path)
            print("CLI arguments", args)

        except Exception as e:
            Logger.log_error(f"Critical error: {e}")
main()