# AUTOMATION_PROJ_1

This project automates file management on your local machine. It provides a small set of classes to scan directories, move files into categorized folders, rename and delete files, and keep an activity log.

Key components
- `Logger_Manager` — configures separate info and error loggers written to disk.
- `Directory_Manager` — directory traversal, creation, existence checks, and deleting empty directories.
- `File_Manager` — file operations (search, move, rename, delete) and extension-based sorting.

Default extension mapping
The `File_Manager` includes a built-in default mapping of file extensions to target folders. This mapping is defined as the class attribute `File_Manager.EXTENSIONS_DEFAULT`. When you instantiate `File_Manager` you can either:

- Pass `None` for the `extension_dict` argument to use the built-in defaults (recommended):

```python
Sorter = File_Manager(r"C:\path\to\source", None, logger_instance, directory_manager)
```

- Or provide your own mapping (it will be merged over the defaults so you can add or override entries):

```python
custom = {'.md': 'Markdown'}
Sorter = File_Manager(r"C:\path\to\source", custom, logger_instance, directory_manager)
```

Running the script
- Open the repository folder in VS Code or your terminal.
- Inspect and modify the `if __name__ == "__main__"` block in `Folder_Sorter_OOP.py` to point `base_path` at the folder you want to manage.
- Run the script with Python: `python Folder_Sorter_OOP.py`.

Notes
- The code uses composition: `File_Manager` receives a `Directory_Manager` and a `Logger_Manager` instance. This keeps responsibilities separate and makes testing easier.
- Be careful when using `git push --force` — it rewrites remote history and can cause problems for collaborators.

If you want, I can add a short example section with common command examples or create unit tests for the main behaviors.
