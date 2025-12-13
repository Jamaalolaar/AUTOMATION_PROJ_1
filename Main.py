from Folder_Sorter_OOP import Directory_Manager, File_Manager
from Config_Manager import ConfigManager
from Logger_Manager import LoggerManager

def main():
    """
    Orchestrates the FolderSorter workflow 
    """
    Config = ConfigManager()
    Logger = LoggerManager(Config)
    DM = Directory_Manager(Logger)
    FM = File_Manager(Config, Logger, DM)
    extensions = ConfigManager().config_data
    if __name__ == "__main__":
        try:
            Sorter = FM
            Sorter.fold_file_by_extension()
            #Sorter.directory.delete_empty(Sorter.base_path)
            #Sorter.rename_file(input("Enter the name of the file to be renamed: "))
            #Sorter.unfold_files(Sorter.base_path)

        except Exception as e:
            Logger.log_error(f"Critical error: {e}")
main()