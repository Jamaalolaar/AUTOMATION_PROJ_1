# Cryptium Manager

A powerful command-line tool for automating file management and organization on your local machine.

## Overview

Cryptium Manager is a Python-based file automation utility that scans directories, organizes files by extension into categorized folders, renames, moves, deletes files, and maintains detailed activity logs. It's perfect for keeping your file system organized with minimal manual effort.

## Features

- **File Organization**: Automatically sort files into folders based on their extension
- **File Operations**: Move, rename, delete, and search for files
- **Extension Mapping**: Built-in mapping of 26+ file extension types to categories (Images, Documents, Videos, Audio, Excel, PDFs, etc.)
- **Activity Logging**: Separate info and error loggers that write to disk for audit trails
- **CLI Commands**: 8 subcommands for various file management operations
- **Custom Configuration**: JSON-based configuration for custom extension mappings and logging
- **Zero Dependencies**: No external dependencies beyond Python 3.10+

## Architecture

### Key Components

- **`Logger_Manager`** — Configures separate info and error loggers written to disk
- **`Directory_Manager`** — Directory traversal, creation, existence checks, and deleting empty directories
- **`File_Manager`** — File operations (search, move, rename, delete) and extension-based sorting
- **`Config_Manager`** — Loads and manages JSON configuration files
- **`Command_Line`** — CLI argument parser with 8 subcommands
- **`Commands_Map`** — Maps CLI commands to File_Manager operations

### Supported Commands

- `sort` — Organize files into folders by extension
- `unsort` — Extract files back to parent directory
- `rename` — Rename files interactively
- `find` — Search for files by name
- `delete` — Remove files (with confirmation)
- `move` — Move files to a destination
- `delete_empty_dirs` — Clean up empty folders
- `create` — Create new folders

## Installation

### Using `uv` (Recommended)

```bash
# Clone or navigate to the project
cd Projects/AUTOMATION_PROJ_1

# Create a virtual environment and install
uv sync

# Or install directly
uv pip install -e .
```

### Using `pip`

```bash
# Navigate to the project
cd Projects/AUTOMATION_PROJ_1

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

## Usage

### As a Command-Line Tool

After installation, use the `cryptium` command:

```bash
# Sort files in a directory
cryptium sort /path/to/directory

# Find a file
cryptium find /path/to/directory filename.txt

# Rename files interactively
cryptium rename /path/to/directory

# Delete files
cryptium delete /path/to/directory filename.txt

# Move files
cryptium move /source/path /destination/path

# View all available commands
cryptium --help
```

### As a Python Module

```python
from cryptium_package.Folder_Sorter_OOP import File_Manager, Directory_Manager
from cryptium_package.Logger_Manager import Logger_Manager

# Initialize components
logger = Logger_Manager('logs', 'info', 'error')
dir_manager = Directory_Manager()
file_manager = File_Manager(r"C:\path\to\source", None, logger, dir_manager)

# Use built-in default extension mapping
file_manager.sort_files_by_extension()

# Or provide custom mapping
custom = {'.md': 'Markdown', '.py': 'Python'}
file_manager = File_Manager(r"C:\path\to\source", custom, logger, dir_manager)
file_manager.sort_files_by_extension()
```

## Configuration

The project uses a `config_file.json` for configuration:

```json
{
  "base_path": "C:\\Users\\YourUser\\Documents",
  "log_file_info": "log_info.txt",
  "log_file_error": "log_error.txt",
  "log_file_config": "log_config.txt",
  "extensions": {
    ".jpg": "Images",
    ".pdf": "Documents",
    ".xlsx": "Excel",
    ".mp4": "Videos"
  }
}
```

You can customize the extension mappings to suit your needs.

## Design Principles

- **Composition over Inheritance**: `File_Manager` receives `Directory_Manager` and `Logger_Manager` instances, keeping responsibilities separate and making testing easier
- **Extensible**: Custom extension mappings override defaults without losing built-in mappings
- **Safe Operations**: File deletion requires confirmation by default

## Requirements

- Python 3.10 or higher
- No external package dependencies

## License

Created by Jamaldeen Mukadam

