import os
import shutil
from datetime import datetime

def get_extension():
    """Prompt the user for the file extension."""
    extension = input("Enter the file extension (e.g., mp3 or mp4): ").strip()
    if not extension.startswith("."):
        extension = f".{extension}"
    return extension

def get_source_folder():
    """Prompt the user for the source folder."""
    source_folder = input("Enter the source folder path (leave blank to use the current directory): ").strip()
    if not source_folder:
        source_folder = os.getcwd()
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist!")
        exit(1)
    return source_folder

def get_destination_folder():
    """Prompt the user for the destination folder."""
    destination_folder = input("Enter the destination folder path (leave blank to create a new folder in the current directory): ").strip()
    if not destination_folder:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        destination_folder = os.path.join(os.getcwd(), f"CopiedFiles_{timestamp}")
        os.makedirs(destination_folder, exist_ok=True)
    elif not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    return destination_folder

def check_write_permission(folder):
    """Check if the folder is writable."""
    try:
        test_file = os.path.join(folder, "PermissionTest.tmp")
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
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_folder, file)
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
