import os
import shutil
import zipfile
import hashlib
import tkinter
from tkinter import messagebox
import time 
# This code is to hide the main tkinter window
root = tkinter.Tk()
root.withdraw()


#To get the amount in diffrent units

KB=1024
MB=1024*KB
GB=1024*MB
def get_free_space(path):
    print("Free Space is  = ",shutil.disk_usage('./myOS').free / GB,"GB")
    return shutil.disk_usage('./myOS').free / GB

def get_utilized_space(path):
    print("Utilized Space is  = ",shutil.disk_usage('./myOS').used / GB,"GB")
    return shutil.disk_usage('./myOS').used / GB

def get_file_hash(file_path, hash_algo='sha256', chunk_size=65536):
    """Compute the hash value of a file using the specified hashing algorithm."""
    hash_obj = hashlib.new(hash_algo)
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            hash_obj.update(data)
    return hash_obj.hexdigest()

def calculate_folder_mean(folder_path):
    """Calculate the mean value of folder size and the number of files inside the folder."""
    total_size = 0
    total_files = 0
    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            total_size += os.path.getsize(file_path)
            total_files += 1
    if total_files == 0:
        return 0
    return total_size / total_files


def search_file(directory_path, file_name):
    # Initialize the search results list
    search_results = []

    # Function to get the file type based on the file extension
    def get_file_type(file_extension):
        # Define the file types and their corresponding extensions
        file_types = {
            "image": ["jpg", "jpeg", "png", "gif", "bmp"],
            "video": ["mp4", "avi", "mkv", "mov", "flv"],
            "audio": ["mp3", "wav", "flac", "aac", "ogg"],
            "text": ["txt", "doc", "docx", "pdf", "csv"]
        }

        # Determine the file type based on the file extension
        for file_type, extensions in file_types.items():
            if file_extension.lower() in extensions:
                return file_type

        return "Unknown"

    # Function to search for files of a specific file type in a directory
    def search_by_file_type(folder_path, file_type):
        for root, _, files in os.walk(folder_path):
            for file in files:
                # Check if the file name matches the search query
                if file_name in file:
                    _, file_extension = os.path.splitext(file)
                    file_extension = file_extension[1:]  # Remove the dot from the extension
                    if get_file_type(file_extension) == file_type:
                        file_path = os.path.join(root, file)
                        file_size = os.path.getsize(file_path)
                        relative_folder = os.path.relpath(root, directory_path)
                        search_results.append((file, file_type, file_size, relative_folder))

    # Get the list of unique data folders (subfolders)
    unique_data_folders = os.listdir(os.path.join(directory_path, 'unique_data_folder'))

    # Search inside unique_data_folder for files with matching file type
    for unique_folder in unique_data_folders:
        unique_folder_path = os.path.join(directory_path, 'unique_data_folder', unique_folder)
        search_by_file_type(unique_folder_path, get_file_type(file_name.split(".")[-1]))

    # Get the list of duplicate data folders (subfolders)
    duplicate_data_folders = os.listdir(os.path.join(directory_path, 'duplicate_data_folder'))

    # Search inside duplicate_data_folder for files with matching file type
    for duplicate_folder in duplicate_data_folders:
        duplicate_folder_path = os.path.join(directory_path, 'duplicate_data_folder', duplicate_folder)
        search_by_file_type(duplicate_folder_path, get_file_type(file_name.split(".")[-1]))

    return search_results

large_files = []
def get_large_files():
    return large_files

def classify_files_and_create_table(dir_path, large_file_mean):
    """Classify files and create the table for large files."""
    global large_files  # Use the global large_files list
    files_by_hash = {}
    duplicate_files = {}

    unique_folder = os.path.join(dir_path, "unique_data_folder")
    duplicate_folder = os.path.join(dir_path, "duplicate_data_folder")
    if not os.path.exists(unique_folder):
        os.makedirs(unique_folder)
    if not os.path.exists(duplicate_folder):
        os.makedirs(duplicate_folder)

    for root, _, files in os.walk(dir_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_size = os.path.getsize(file_path)
            file_type = filename.split('.')[-1].lower()
            if file_size > large_file_mean:
                large_files.append((filename, file_type, file_size,file_path))


            
            file_type = filename.split('.')[-1].lower()
            if file_type in ['mp3', 'wav', 'ogg', 'flac']:
                file_type = 'audio'
            elif file_type in ['mp4', 'avi', 'mov', 'mkv']:
                file_type = 'video'
            elif file_type in ['txt', 'csv', 'doc', 'docx', 'pdf']:
                file_type = 'text'
            elif file_type in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                file_type = 'image'
            else:
                file_type = 'other'

            file_hash = get_file_hash(file_path)

            if file_hash in files_by_hash:
                duplicate_files.setdefault(file_hash, []).append(file_path)
            else:
                files_by_hash[file_hash] = (file_path, file_type)

    # Move files to respective folders
    for file_hash, (file_path, file_type) in files_by_hash.items():
        new_path = os.path.join(unique_folder, file_type, os.path.basename(file_path))
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        os.rename(file_path, new_path)

    for file_hash, file_paths in duplicate_files.items():
        for file_path in file_paths:
            file_type = file_path.split('.')[-1].lower()
            if file_type in ['mp3', 'wav', 'ogg', 'flac']:
                file_type = 'audio'
            elif file_type in ['mp4', 'avi', 'mov', 'mkv']:
                file_type = 'video'
            elif file_type in ['txt', 'csv', 'doc', 'docx', 'pdf']:
                file_type = 'text'
            elif file_type in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                file_type = 'image'
            else:
                file_type = 'other'

            new_path = os.path.join(duplicate_folder, file_type, os.path.basename(file_path))
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            os.rename(file_path, new_path)

    # Create the table for large files
    large_files_table_path = os.path.join(dir_path, "large_file.txt")
    with open(large_files_table_path, 'w') as table_file:
        table_file.write("File Name\tFile Type\tFile Size\tFile Path\n")
        for file_info in large_files:
            file_name, file_type, file_size,file_path = file_info
            sz=file_size/MB
            table_file.write(f"{file_name}\t{file_path}\t{sz}(MB)\n")
  #  get_large_files(large_files)
    return files_by_hash, duplicate_files, large_files

def show_results(large_files, files_by_hash, duplicate_files, searched_file_name, search_result):
    results_text = f"Search Results for '{searched_file_name}':\n\n"

    if search_result:
        results_text += f"File Found!\nFile Path: {search_result}\n"
    else:
        results_text += "File Not Found!\n"

    results_text += "\nLarge Files:\n"
    for file_info in large_files:
        file_name, file_path, file_type, file_size = file_info
        file_size=file_size/MB
        results_text += f"File Name: {file_name} | Path: {file_path} | Type: {file_type} | Size: {file_size} bytes\n"

    results_text += "\nFiles by Hash:\n"
    for hash_val, (file_path, file_type) in files_by_hash.items():
        results_text += f"Hash: {hash_val} | Type: {file_type} | Path: {file_path}\n"

    results_text += "\nDuplicate Files:\n"
    for hash_val, file_paths in duplicate_files.items():
        results_text += f"Hash: {hash_val} | Duplicates: {', '.join(file_paths)}\n"

    messagebox.showinfo("Search Results", results_text)


import os

def delete_files_by_type(dir_path, file_type):
    """Delete files with a given file extension (file type) from both unique and duplicate data folders."""
    unique_folder = os.path.join(dir_path, "unique_data_folder")
    duplicate_folder = os.path.join(dir_path, "duplicate_data_folder")
    deleted_count = 0
    if file_type in ['mp3', 'wav', 'ogg', 'flac']:
        file_ex = 'audio'
    elif file_type in ['mp4', 'avi', 'mov', 'mkv']:
        file_ex = 'video'
    elif file_type in ['txt', 'csv', 'doc', 'docx', 'pdf']:
        file_ex = 'text'
    elif file_type in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
        file_ex = 'image'
    else:
        file_ex = 'other'

    # Function to delete files from a folder
    def delete_files_from_folder(folder_path):
        nonlocal deleted_count
        for root, _, files in os.walk(folder_path):
            # If the folder name is the chosen file type, delete matching files
            if os.path.basename(root) == file_ex:
                for filename in files:
                    if filename.lower().endswith(file_type.lower()):
                        file_path = os.path.join(root, filename)
                        os.remove(file_path)
                        deleted_count += 1

    # Delete files from unique_data_folder
    delete_files_from_folder(unique_folder)

    # Delete files from duplicate_data_folder
    delete_files_from_folder(duplicate_folder)

    return deleted_count

def search_file_2(dir_path, file_name):
    """Search for files with a given file name in both unique and duplicate data folders."""
    unique_folder = os.path.join(dir_path, "unique_data_folder")
    duplicate_folder = os.path.join(dir_path, "duplicate_data_folder")
    found_files = []

    # Function to search for files in a folder
    def search_files_in_folder(folder_path):
        for root, _, files in os.walk(folder_path):
            for filename in files:
                if filename.lower() == file_name.lower():
                    found_files.append(os.path.join(root, filename))

    # Search for files in unique_data_folder
    search_files_in_folder(unique_folder)

    # Search for files in duplicate_data_folder
    search_files_in_folder(duplicate_folder)

    return found_files

def delete_files_by_name(dir_path, file_name):
    searched_file_path = search_file_2(dir_path, file_name)
    for searched_file in searched_file_path:
        if searched_file:
            os.remove(searched_file)
            print(f"File '{file_name}' deleted successfully from both unique_data_folder and duplicate_data_folder.")
            return 1
        else:
            print(f"File '{file_name}' not found in unique_data_folder and duplicate_data_folder.")
        return 0

def delete_duplicate_folder(dir_path,sub_option):
    duplicate_folder = os.path.join(dir_path, "duplicate_data_folder")
    if os.path.exists(duplicate_folder):
        if sub_option == 1:
            import shutil
            shutil.rmtree(duplicate_folder)
            print("duplicate_data_folder deleted successfully.")
            return 1
        elif sub_option == 2:
            compress_duplicate_folder(duplicate_folder)
            import shutil
            #shutil.rmtree(duplicate_folder)
            #print("duplicate_data_folder file_type folders compressed to zip and duplicate_data_folder deleted.")
            return 1
        else:
            return 0
    return 0

def compress_duplicate_folder(duplicate_folder):
    if not os.path.exists(duplicate_folder):
        print("Duplicate data folder does not exist.")
        return 0

    compressed_count = 0
    for file_type_folder in os.listdir(duplicate_folder):
        file_type_folder_path = os.path.join(duplicate_folder, file_type_folder)
        if os.path.isdir(file_type_folder_path):
            zip_file_path = os.path.join(duplicate_folder, f"{file_type_folder}.zip")
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(file_type_folder_path):
                    for filename in files:
                        file_path = os.path.join(root, filename)
                        relative_path = os.path.relpath(file_path, file_type_folder_path)
                        zipf.write(file_path, relative_path)
            shutil.rmtree(file_type_folder_path)
            print(f"'{file_type_folder}' folder compressed to '{file_type_folder}.zip'.")
            compressed_count += 1

    if compressed_count == 0:
        print("No duplicate data folders found for compression.")
        return 0

    return 1
def add_file(dir_path, file_path):
    unique_folder = os.path.join(dir_path, "unique_data_folder")

    file_type = os.path.splitext(os.path.basename(file_path))[1][1:].lower()
    file_hash = get_file_hash(file_path)
    print(file_type)
    if file_type in ['mp3', 'wav', 'ogg', 'flac']:
        file_type = 'audio'
    elif file_type in ['mp4', 'avi', 'mov', 'mkv']:
       file_type = 'video'
    elif file_type in ['txt', 'csv', 'doc', 'docx', 'pdf']:
       file_type = 'text'
    elif file_type in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
       file_type = 'image'
    else:
     file_type = 'other'
     
    file_type_folder = os.path.join(unique_folder, file_type)
    if not os.path.exists(file_type_folder):
        os.makedirs(file_type_folder)

    for root, _, files in os.walk(file_type_folder):
        for filename in files:
            unique_file_path = os.path.join(root, filename)
            if get_file_hash(unique_file_path) == file_hash:
                print("File already exists in unique_data_folder.")
                return none

    # If the file is not found in the specific file_type folder, add it to that folder
    file_name = os.path.basename(file_path)
    target_file_path = os.path.join(file_type_folder, file_name)
    shutil.copyfile(file_path, target_file_path)
    print(file_name)
    print("File added to unique_data_folder.")
    return file_name

def is_infrequently_accessed(file_path, threshold_minutes=5):
    """Check if a file is infrequently accessed (not accessed within threshold_minutes)."""
    if not os.path.exists(file_path):
        return False

    current_time = time.time()
    file_stat = os.stat(file_path)
    access_time = file_stat.st_atime

    # Calculate the number of minutes since last access
    minutes_since_access = (current_time - access_time) / 60

    return minutes_since_access > threshold_minutes

def get_infrequently_accessed_files(dir_path, threshold_minutes=5):
    """Get all infrequently accessed files in the directory with a specified threshold in minutes."""
    infrequently_accessed_files = []
    for root, _, files in os.walk(dir_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            if is_infrequently_accessed(file_path, threshold_minutes):
                infrequently_accessed_files.append((filename, file_path))
    return infrequently_accessed_files

if __name__ == "__main__":
    duplicate_files={}
    unique_files={}
    directory_path = "./myOS"
    large_file_mean = calculate_folder_mean(directory_path)
    #unique_files, duplicate_files, large_files=classify_files_and_create_table(directory_path, large_file_mean)
    alpha=True
    while True:
        print("-----------------------------------------------------------------")
        print("Enter 1 to get free space : ")
        print("Enter 2 to get utilized space : ")
        print("Enter 3 to get all the duplicate file : ")
        print("Enter 4 to get all the large file : ")
        print("Enter 5 to Search file : ")
        print("Enter 6 to delete file : ")
        print("Enter 7 to add file : ")
        print("Enter 0 to terminate : ")
        n=int(input())
        if n==0:
            break
        elif n==1:
            get_free_space(directory_path)
        elif n==2:
            get_utilized_space(directory_path)
        elif n==3:
            print("\nDuplicate Files:")
            for hash_val, file_paths in duplicate_files.items():
                print(f"Duplicates: {', '.join(file_paths)}")
        elif n==4:
            print("\nLarge Files:")
            for file_info in large_files:
                print(f"File Name: {file_info[0]} | Type: {file_info[1]}  | Size: {file_info[2]} bytes | Path: {file_info[3]}")
        elif n==5:
            searched_file_name = input("Enter the file name ")
            result = search_file(directory_path, searched_file_name)
            if(len(result)):
                print(f"File found")
            else:
                print("File not found.")
        elif n==6:
            delete_option = input("Choose a delete option:\n1. Delete files by file type\n2. Delete files by file name\n3. Delete duplicate_data_folder\nEnter option number (1, 2, or 3): ")
            if delete_option == "1":
                file_type = input("Enter the file type you want to delete (e.g., txt, jpg, pdf): ")
                delete_files_by_type(directory_path, file_type)
            elif delete_option == "2":
                file_name = input("Enter the file name you want to delete: ")
                delete_files_by_name(directory_path, file_name)
            elif delete_option == "3":
                delete_duplicate_folder(directory_path)
        elif n==7:
            file_path = input("Enter the file path you want to add to unique_data_folder: ")
            file_path = file_path[1:-1]
            if os.path.exists(file_path):
                add_file(directory_path, file_path)
            else:
                print("File found found.")


            
            

