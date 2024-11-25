import os
import shutil
from datetime import datetime
from pathlib import Path

def get_extension():
    """Prompt the user for the file extension."""
    extension = input("Enter the file extension (e.g., mp3 or mp4): ").strip()
    if not extension.startswith("."):
        extension = f".{extension}"
    return extension

def get_folder(prompt, default):
    while True:
        folder = input(prompt).strip() or default
        path = Path(folder)
        if path.exists():
            return path.resolve()
        else:
            print(f"The specified {default} '{folder}' does not exist. Please try again.")

def get_source_folder():
    """Prompt the user for the source folder."""
    return get_folder("Enter the source folder path (leave blank to use the current directory): ", "current directory")

def get_destination_folder():
    """Prompt the user for the destination folder."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    default_name = f"CopiedFiles_{timestamp}"
    return get_folder(f"Enter the destination folder path (leave blank to create a new folder '{default_name}' in the current directory): ", default_name)

def check_write_permission(folder):
    """Check if the folder is writable."""
    test_file = folder / "PermissionTest.tmp"
    try:
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
    except IOError:
        print(f"Write permission denied for '{folder}'. Please check permissions.")
        exit(1)

def copy_files_with_extension(extension, source_folder, destination_folder):
    """Copy all files with the specified extension."""
    print(f"\nCopying files with extension '{extension}' from '{source_folder}' to '{destination_folder}'...")
    files_copied = 0

    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith(extension.lower()):
                source_file = Path(root) / file
                destination_file = destination_folder / file
                try:
                    shutil.copy2(source_file, destination_file)
                    print(f"Copied: {source_file} to {destination_file}")
                    files_copied += 1
                except IOError as e:
                    print(f"Failed to copy {source_file}: {e}")

    if files_copied == 0:
        print(f"No files with extension '{extension}' found in '{source_folder}'.")
    else:
        print(f"Successfully copied {files_copied} files to '{destination_folder}'.")

if __name__ == "__main__":
    # Get user inputs
    file_extension = get_extension()
    source = get_source_folder()
    destination = get_destination_folder()

    # Check write permissions for the destination
    check_write_permission(destination)

    # Copy files
    copy_files_with_extension(file_extension, source, destination)