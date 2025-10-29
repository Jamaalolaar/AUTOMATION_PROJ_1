from pathlib import Path
import re
import shutil
import os
import time
import logging

#logging.basicConfig(level= logging.INFO, filename="File Sorter Logs.log", filemode = "w", format="%(asctime)s - %(levelname)s - %(message)s") ( The traditional way of creating logs)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

info_handler = logging.FileHandler('File Sorter Logs.log')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)


error_handler = logging.FileHandler('Error Logs.log')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

def file_type(extension, new_ext):
    patterns = {'.txt': 'Text Files', '.jpeg':'Images', '.jpg': 'Images', '.png': 'Images', '.doc': 'Word Documents', '.docx': 'Word Documents', '.ppt':
                'Powerpoint Documents', '.pptx': 'Powerpoint Documents', '.pdf': 'PDF Files', '.xlsx': 'Excel Documents', '.xls': 'Excel Documents'}
    if extension not in patterns and new_ext != None:
        patterns[extension] = new_ext
    return (patterns.get(extension))
        
def file_folder():
    extensions = []
    dir_path = Path(input("Input path..."))

    for file_path in dir_path.iterdir():
        ext = file_path.suffix
        try:
            new_path = Path(dir_path/file_type(ext,None))
        except Exception as e:
            logger.addHandler(error_handler)
            logger.error(f'An error occurred!!!{e}')
            print("File extension not recognized!!!")
            response = input(f"Do you want the system to recognize {ext} files? Type yes or no? ")
            if response == 'yes':
                folder_name = input("Enter the desired folder name for this type of file ")
            else:
                folder_name = 'Others'
            new_path = Path(dir_path/file_type(ext, folder_name))
            logger.info(f'A new folder {folder_name} was created')
                
        if not new_path.exists():
            new_path.mkdir(exist_ok=True)
        source = file_path
        destination = new_path/file_path.name
        shutil.move(str(source), str(destination))

        logger.addHandler(info_handler)
        logger.info(f"{source.name} successively moved to {new_path.name}")

def file_unfolder():
    dir_path = Path(input("Input path..."))
    for file_path in dir_path.iterdir():
        if file_path.is_dir():
            for file in file_path.iterdir():
                if file.is_file():
                    source = file
                    destination = dir_path/file.name
                    shutil.move(str(source), str(destination))
                
            file_path.rmdir()
                

    
    
file_folder()
