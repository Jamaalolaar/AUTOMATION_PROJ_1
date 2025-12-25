from Folder_Sorter_OOP import Directory_Manager, File_Manager, Path
from Config_Manager import ConfigManager
from Logger_Manager import LoggerManager
from Command_Line import parse_cli_arguments
import Commands_Map

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
            Cryptium = FM
            
            command_map = {
                "rename": rename_cmd,
                "sort": sort_cmd,
                "unsort": unsort_cmd,
            }
                
                
            #Cryptium.fold_file_by_extension()
            #Cryptium.directory.delete_empty(Cryptium.base_path)
            #Cryptium.rename_file(input("Enter the name of the file to be renamed: "))
            #Cryptium.unfold_files(Cryptium.base_path)

        except Exception as e:
            Logger.log_error(f"Critical error: {e}")
main()