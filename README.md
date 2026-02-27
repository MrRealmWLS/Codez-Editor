# Codez Editor

A lightweight and intuitive code editor built with Python using CustomTkinter and Tkinter. Codez Editor provides a modern dark-themed interface with essential file management and editing capabilities.
![Image](https://github.com/MrRealmWLS/Codez-Editor/blob/9fa5ad56df48e17f581b7124a23c402f68f80c2a/image.png)
## Features

- Dark theme interface with purple accent colors
- File and folder explorer with tree view
- Tabbed document interface for multiple files
- Basic file operations (create, rename, delete files/folders)
- Syntax highlighting (through system defaults)
- Undo/redo functionality
- Copy/paste/cut shortcuts
- Workspace management

## Requirements

- Python 3.7 or higher
- Dependencies listed in `requirements.txt`

## Installation

1. Clone or download this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:

```bash
python main.py
```

2. Click "Open Folder" to select a directory as your workspace
3. Navigate through the file explorer to open files in tabs
4. Use the toolbar buttons to create new files or folders
5. Close tabs by clicking the '×' button on each tab or using Ctrl+W

## Controls

- **Ctrl+Z**: Undo
- **Ctrl+Y**: Redo
- **Ctrl+C**: Copy
- **Ctrl+V**: Paste
- **Ctrl+X**: Cut
- **Ctrl+W**: Close current tab

## Project Structure

- `main.py`: Main application file containing the GUI and all functionality
- `requirements.txt`: Python dependencies
- `assets/`: Directory for images and icons (if present)

## Dependencies

- customtkinter: Modern-looking tkinter widgets
- Pillow: Image processing for icons
- tkinter: Standard GUI toolkit for Python
- os, re: Standard Python libraries for file system operations

## License

This project is open source and available under the MIT License.
