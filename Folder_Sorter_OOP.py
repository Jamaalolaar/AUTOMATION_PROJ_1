from pathlib import Path
import shutil
import logging
from Config_Manager import ConfigManager

class Logger_Manager:
    """
    Manages and configures separate loggers for info and error messages
    """
    def __init__(self, config):
        """
        Initialize Logger_Manager with separate info and error loggers

        self: Instance of Logger_Manager
        info_log_file: Path to the info log file
        error_log_file: Path to the error log file
        """
        self.config_data = config.config_data.get('log_files', {})
        info_log_file = self.config_data.get('log_files', {}).get('Info_log', 'Info Logs.log')
        error_log_file = self.config_data.get('log_files', {}).get('Error_log', 'Error logs.log')
        self.info_logger = self._setup_logger("info_logger", self.config_data.get('Info_log'))
        self.error_logger = self._setup_logger("error_logger",self.config_data.get('Error_log'))
    def _setup_logger(self, name, log_file):
        """
        Create and configure a logger that writes debug messages to a specified file

        self: Instance of Logger_Manager
        name: Name of the logger to create
        log_file: Path to the log file for storing log messages
        return: Configured logger instance
        return type: Logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        #Handler Creation
        handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger
    def log_info(self, message):
        """Logs info"""
        self.info_logger.info(message)
    def log_error(self, message):
        """Logs error"""
        self.error_logger.error(message)



class Directory_Manager:
    def __init__(self, logger):
        """Initialize"""
        self.logger = logger
    def create_dir(self, path):
        """Creates a directory and logs the action into the info log file. If an
        error is encountered, it logs the error into the error log file."""
        try:
            path.mkdir(parents=True, exist_ok=True)
            self.logger.log_info(f'A new directory {path} was succesfully created!')
        except Exception as e:
            self.logger.log_error(f'Failed to create directory: {path}')
                
                
    def exists(self, path):
        """Returns True if the directory exists, False otherwise"""
        return path.exists() and path.is_dir()
    def scan_all(self, path):
        """Recursively traverse through all files and directories in the given path.
        
        Args:
            path: A Path object representing the directory to scan
            
        Yields:
            Path objects for both files and directories found during traversal
        """
        for item in path.iterdir():
            yield item  # First yield the item itself (file or directory)
            if item.is_dir():
                # If it's a directory, recursively scan its contents
                yield from self.scan_all(item)
    def is_empty(self, path):
        """Checks if a directory is empty and returns True if it is, False otherwise"""
        return not any(path.iterdir())
            
    def delete_empty(self, path):
        """Deletes empty directories within the specified path and logs the deletions"""
        for folder in path.rglob("*"):
            if folder.is_dir() and self.is_empty(folder):
                folder.rmdir()
                self.logger.log_info(f'Deleted empty directory: {folder}')
                 

class File_Manager:
    """
    Handles file organization, movement, and extension management within a specified directory
    """
    # Default extensions mapping shared as a class-level constant. Use a copy in __init__ to
    # avoid accidental shared-mutable state between instances.
    EXTENSIONS_DEFAULT = {
        '.txt': 'Text Files',
        '.jpeg': 'Images',
        '.jpg': 'Images',
        '.png': 'Images',
    }
    def __init__(self, config, logger, directory):
        """Initializes File_Manager with config object, logger, and directory manager."""
        self.config = config
        base_path = config.get('base_path')
        extension_dict = self.config.get('extensions')
        self.base_path = Path(base_path)
        
        if extension_dict is None:
            self.extension_dict = dict(self.EXTENSIONS_DEFAULT)
        else:
            self.extension_dict = extension_dict
        self.logger = logger
        self.directory = directory
        
    def check_extensions(self):
        """Checks if the file path is a file and if all the extensions (file suffix) are present in the dictionary 'extension_dict'. If an
        unrecognized extension is detected, it also adds a new extension to the initialized extension_dict  by calling the add_new_extension function"""
        for file_path in self.base_path.iterdir():
            if file_path.is_file():
                ext = file_path.suffix
                if ext not in self.extension_dict:
                    response = input(f'Unrecognized extension {ext}! Do you want to assign a folder name to this extension? y/n: ')
                    if response == 'y':
                        self.add_new_extension(ext)
                    elif response == 'n':
                        self.extension_dict[ext] = 'Others'
        
    def move_file(self, src, dest):
        """Moves a single file from src to dst and logs the movement"""
        try:
            shutil.move(str(src), str(dest))
            self.logger.log_info(f'{src.name} was successfully moved to {dest}')
        except (shutil.Error, OSError) as e:
            self.logger.log_error(f'Failed to move {src.name} to {dest}: {e}')
        
    def fold_file_by_extension(self):
        """
        Move files based on their extensions into categorized folders and logs every movement and error .
        """
        for file_path in self.directory.scan_all(self.base_path):
            if file_path.is_file():
                try:
                    ext = file_path.suffix
                    if ext not in self.extension_dict:
                        self.add_new_extension(ext)
                    
                    folder_name = self.extension_dict.get(ext)
                    new_path = self.base_path / folder_name
                    
                    if not self.directory.exists(new_path):
                        self.directory.create_dir(new_path)
                    
                    dest_path = new_path / file_path.name
                    if dest_path.exists():
                        # Handle duplicate file names
                        base_name = file_path.stem
                        suffix = file_path.suffix
                        counter = 1
                        while dest_path.exists():
                            new_name = f"{base_name}_{counter}{suffix}"
                            dest_path = new_path / new_name
                            counter += 1
                    
                    self.move_file(file_path, dest_path)
                    self.logger.log_info(f'File was successfully {file_path.name} moved to {dest_path}') 
                except Exception as e:
                    self.logger.log_error(f"Error processing file {file_path}: {e}")
             
        self.directory.delete_empty(self.base_path)
    def find_file(self, file_name):
        """Searches for a file with the given name in the base_path and its subdirectories.
        Returns the Path object if found, otherwise returns None."""
        for file_path in self.directory.scan_all(self.base_path):
            if file_path.is_file() and file_path.stem == file_name:
                self.logger.log_info(f'File {file_name} found at {file_path}')
                return file_path
        print(f'File {file_name} not found in {self.base_path} or its subdirectories. Check file name and try again.')
        self.logger.log_info(f'File {file_name} not found in {self.base_path} or its subdirectories.')
        return None

    def add_new_extension(self, ext):
        """Adds a new extension and its folder name to the extension dictionary 'extension_dict' and logs it"""
        Folder_name = input(f'Enter the folder_name for {ext} files: ')
        self.extension_dict[ext] = Folder_name
        self.config.config_data['extensions'][ext] = Folder_name
        self.config.update_config(ext, Folder_name)
        self.logger.log_info(f'A new extension {ext} was added to the extensions dictionary!')

        
    def unfold_files(self, path):
        """Moves files from subdirectories back to the parent directory and deletes empty folders afterwards"""
        self.path = Path(path)
        for file_path in self.directory.scan_all(self.path):
            if file_path.is_file():
                source = file_path
                destination = self.path/file_path.name
                self.move_file(source, destination)
                self.logger.log_info(f"{self.path} was successfully unfolded")
            self.directory.delete_empty(self.path)
        self.directory.delete_empty(self.path)
    
    def rename_file(self, file_name):
        """Renames a file found by `file_name` (stem without suffix).

        Prompts the user for a new name 
        """
        old_path = self.find_file(file_name)
        if old_path is None:
            self.logger.log_error(f"Cannot rename: file '{file_name}' not found.")
            return

        try:
            # Ask user for a new name
            user_input = input(f"Enter the new name for the file {old_path.name} ").strip()
            if not user_input:
                self.logger.log_info("Rename cancelled: empty name provided.")
                return

            # Determine the new name and extension
            if Path(user_input).suffix:
                # User provided an extension
                new_name = Path(user_input).name
            else:
                # No extension provided; hence, keep the original extension
                new_name = f"{user_input}{old_path.suffix}"

            # Build the new full path using pathlib
            new_path = old_path.with_name(new_name) #'new_path = old_path.parent / new_name' also works well

            # If target (file name) exists, ask for a new name and restart the process
            candidate = new_path
            if candidate.exists():
                print("A file with that name already exists. Please provide a different name.")
                self.rename_file(file_name)
            else:
                self.move_file(old_path, candidate)
            
        
                

            shutil.move(str(old_path), str(candidate))
            self.logger.log_info(f"Renamed {old_path} -> {candidate}")
        except Exception as e:
            self.logger.log_error(f"Failed to rename {old_path}: {e}")
    
    def delete_file(self, file_name):
        """Deletes a specified file and logs the action"""
        file_path = self.find_file(file_name)
        if file_path is None:
            self.logger.log_error(f"Cannot delete: file '{file_name}' not found.")
            return
        elif file_path is not None:
            response = input(f"Are you sure you want to delete the file {file_path.name}? y/n ")
            if response.lower() != 'y':
                self.logger.log_info(f"Deletion of file {file_path.name} cancelled by user.")
                return
            else:
                try:
                    file_path.unlink()
                    self.logger.log_info(f"Deleted file: {file_path}")
                except Exception as e:
                    self.logger.log_error(f"Failed to delete {file_path}: {e}")

        

Config = ConfigManager()
Logger = Logger_Manager(Config)
DM = Directory_Manager(Logger)
extensions = ConfigManager().config_data
if __name__ == "__main__":
    try:
        # Create File_Manager instance
        Sorter = File_Manager(Config, Logger, DM)
        Sorter.fold_file_by_extension()
        #Sorter.directory.delete_empty(Sorter.base_path)
        #Sorter.rename_file(input("Enter the name of the file to be renamed: "))
        #Sorter.unfold_files(Sorter.base_path)

    except Exception as e:
        Logger.log_error(f"Critical error: {e}")

