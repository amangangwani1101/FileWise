import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import os
import random


# Import the backend functions from your backend module
# Replace 'your_backend_module' with the actual name of your backend module
import backend

# Create the main window
root = tk.Tk()
root.title("File Organizer")

# Set the initial directory path to None
directory_path = None

def browse_directory():
    global directory_path
    directory_path = filedialog.askdirectory()

def classify_files():
    if directory_path:
        # Check if the selected directory already contains unique_data_folder
        unique_folder = os.path.join(directory_path, "unique_data_folder")
        if os.path.exists(unique_folder):
            messagebox.showinfo("Directory Already Segregated", "The chosen directory is already segregated.")
            return
        else:
            # Call the backend function to classify and create the table
            mean = backend.calculate_folder_mean(directory_path)
            backend.classify_files_and_create_table(directory_path, mean)

            messagebox.showinfo("Directory Segregated", "Files inside the directory have been segregated based on their type.")
    else:
        messagebox.showinfo("No Directory Selected", "Please select a directory to segregate its files.")


def get_free_disk_space():

    if directory_path:
        # Call the backend function to get free disk space in GB
        free_space_gb = backend.get_free_space(directory_path)
        messagebox.showinfo("Free Disk Space", f"Free disk space in the selected directory: {free_space_gb:.6f} GB")
    else:
        messagebox.showinfo("No Directory Selected", "Please select a directory to get free disk space.")

def get_utilized_disk_space():

    if directory_path:
        # Call the backend function to get free disk space in GB
        free_space_gb = backend.get_utilized_space(directory_path)
        messagebox.showinfo("Free Disk Space", f"Free disk space in the selected directory: {free_space_gb:.6f} GB")
    else:
        messagebox.showinfo("No Directory Selected", "Please select a directory to get free disk space.")

def search_file():
    def search():
        # Get the file name entered by the user
        file_name = search_entry.get()

        # Call the backend function to search for the file
        result = backend.search_file(directory_path, file_name)

        if not result:
            # If no result is found, show a message box
            messagebox.showinfo("Not Found", "File not found in the directory.")
        else:
            # Display the search results in a new dialog box with a resizable table
            search_result_window = tk.Toplevel(root)
            search_result_window.title("Search Results")

            # Create a table to show the search results
            search_table = ttk.Treeview(search_result_window)
            search_table["columns"] = ("File Name", "File Type", "File Size", "Folder")
            search_table.heading("#0", text="", anchor=tk.W)
            search_table.heading("File Name", text="File Name", anchor=tk.W)
            search_table.heading("File Type", text="File Type", anchor=tk.W)
            search_table.heading("File Size", text="File Size", anchor=tk.W)
            search_table.heading("Folder", text="Folder", anchor=tk.W)

            # Insert the search results into the table
            for item in result:
                search_table.insert("", tk.END, values=item)

            # Resize the columns to fit the content
            for column in search_table["columns"]:
                search_table.heading(column, command=lambda _col=column: sort_table(search_table, _col, False))
                # Set random initial width for each column
                random_width = random.randint(100, 200)
                search_table.column(column, minwidth=0, width=random_width)

            # Pack the table in the search_result_window
            search_table.pack(expand=True, fill='both')

    # Create a new dialog box for user input
    search_window = tk.Toplevel(root)
    search_window.title("Search File")

    # Create a label and an entry for the user to enter the file name
    search_label = tk.Label(search_window, text="Enter File Name:")
    search_label.pack()
    search_entry = tk.Entry(search_window)
    search_entry.pack()

    # Create a button to perform the search
    search_button = tk.Button(search_window, text="Search", command=search)
    search_button.pack()



def show_large_files():
    if not directory_path:
        messagebox.showinfo("No Directory Selected", "Please select a directory first.")
        return

    # Call the backend function to get the large file list
    large_file_list = backend.get_large_files()

    if not large_file_list:
        messagebox.showinfo("No Large Files", "No large files found in the directory.")
    else:
        # Display the large_file_list in a new dialog box with a table
        large_file_window = tk.Toplevel(root)
        large_file_window.title("Large Files")

        # Create a table to show the large file list
        large_file_table = ttk.Treeview(large_file_window)
        large_file_table["columns"] = ("File Name", "File Type", "File Size", "Folder")
        large_file_table.column("#0", width=0, stretch=tk.NO)
        large_file_table.column("File Name", anchor=tk.W, width=150)
        large_file_table.column("File Type", anchor=tk.W, width=100)
        large_file_table.column("File Size", anchor=tk.W, width=100)
        large_file_table.column("Folder", anchor=tk.W, width=200)
        large_file_table.heading("#0", text="")
        large_file_table.heading("File Name", text="File Name")
        large_file_table.heading("File Type", text="File Type")
        large_file_table.heading("File Size", text="File Size")
        large_file_table.heading("Folder", text="Folder")

        # Insert the large file list into the table
        for item in large_file_list:
            large_file_table.insert("", tk.END, values=item)

        for column in large_file_table["columns"]:
            large_file_table.heading(column, command=lambda _col=column: sort_table(large_file_table, _col, False))
            # Set random initial width for each column
            random_width = random.randint(100, 200)
            large_file_table.column(column, minwidth=0, width=random_width)

        # Pack the table in the search_result_window
        large_file_table.pack(expand=True, fill='both')

def add_file():
    def add():
        file_path = filedialog.askopenfilename()    
        #file_path = file_path[1:-1]
        if not file_path:
            messagebox.showinfo("No File Selected", "Please select a file.")
            return
        print(file_path)
        # Call the backend function to add the file
        result = backend.add_file(directory_path, file_path)
        # Show the result in a message box
        if result is not None:
            choice = messagebox.askquestion("File Added", "File successfully added to the directory.\nDo you want to see its location?")
            if choice == 'yes':
                # Open the file's location in the default file explorer
                if os.path.exists(file_path):
                    os.startfile(os.path.dirname(file_path))
                else:
                    messagebox.showerror("File Not Found", "The file location is not available.")
        else:
            messagebox.showerror("Error", "Failed to add the file to the directory.")

    # Create a file dialog for the user to browse and select a file
    add_file_window = tk.Toplevel(root)
    add_file_window.title("Add File")

    file_label = tk.Label(add_file_window, text="Please select a file:")
    file_label.pack()


    # Create a button to add the file
    add_button = tk.Button(add_file_window, text="Add", command=add)
    add_button.pack()

def delete_file():
    def delete_by_file_type():
        # Define the file types and their corresponding extensions
        file_types = {
            "image": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
            "video": [".mp4", ".avi", ".mkv", ".mov", ".flv"],
            "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
            "text": [".txt", ".doc", ".docx", ".pdf", ".csv"]
        }

        # Create a sub-dialog box to choose the file type
        file_type_choice = simpledialog.askstring("Delete By File Type", "Choose the file type to delete (Image/Video/Audio/Text):")

        if file_type_choice not in file_types:
            messagebox.showerror("Invalid Choice", "Invalid file type choice.")
            return

        # Create a sub-dialog box to choose the file extension within the selected file type
        file_extension_choice = simpledialog.askstring("Delete By File Type", f"Choose the file extension to delete for {file_type_choice}:")

        # Confirm deletion
        confirm_delete = messagebox.askyesno("Confirm Delete", f"All {file_type_choice} files with extension {file_extension_choice} will be deleted. Confirm?")

        if confirm_delete:
            # Call the backend function to perform the delete operation
            print(file_extension_choice)
            result = backend.delete_files_by_type(directory_path,file_extension_choice)

            if result:
                messagebox.showinfo("Deletion Successful", f"All {file_type_choice} files with extension {file_extension_choice} have been deleted.")
            else:
                messagebox.showerror("Error", "Failed to delete files.")

    def delete_by_file_name():
        # Create a sub-dialog box to enter the file name to be deleted
        file_name_choice = simpledialog.askstring("Delete By File Name", "Enter the file name to delete:")

        # Confirm deletion
        confirm_delete = messagebox.askyesno("Confirm Delete", f"All files with the name '{file_name_choice}' will be deleted. Confirm?")

        if confirm_delete:
            # Call the backend function to perform the delete operation
            result = backend.delete_files_by_name(directory_path, file_name_choice)
            # Show the result in a message box
            if result:
                messagebox.showinfo("Files Deleted", f"All files with the name '{file_name_choice}' have been deleted.")
            else:
                messagebox.showinfo("No Files Deleted", f"No files found with the name '{file_name_choice}' in the directory.")

    def delete_duplicate_folder():
        # Create a sub-dialog box to choose the delete option (delete folder or compress folder)
        delete_option = int(simpledialog.askstring("Delete Duplicate Folder", "Choose an option (1 : Delete Folder / 2 : Compress Folder):"))

        if delete_option == 1:
            # Confirm deletion
            confirm_delete = messagebox.askyesno("Confirm Delete", "The duplicate_data_folder will be deleted. Confirm?")
            if confirm_delete:
                # Call the backend function to delete the duplicate_data_folder
                result = backend.delete_duplicate_folder(directory_path,1)

                if result:
                    messagebox.showinfo("Deletion Successful", "The duplicate_data_folder has been deleted.")
                else:
                    messagebox.showerror("Error", "Failed to delete the duplicate_data_folder.")
        elif delete_option == 2:
            # Confirm compression
            confirm_compress = messagebox.askyesno("Confirm Compression", "The duplicate_data_folder will be compressed. Confirm?")
            if confirm_compress:
                # Call the backend function to compress the duplicate_data_folder
                duplicate_folder = os.path.join(directory_path, "duplicate_data_folder")
                result = backend.compress_duplicate_folder(duplicate_folder)

                if result:
                    messagebox.showinfo("Compression Successful", "The duplicate_data_folder has been compressed.")
                else:
                    messagebox.showerror("Error", "Failed to compress the duplicate_data_folder.")
        else:
            messagebox.showerror("Invalid Choice", "Invalid delete option choice.")
            return

    # Create a top-level window for the delete options
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Files")

    # Create buttons for the delete options
    delete_by_file_type_button = tk.Button(delete_window, text="Delete by File Type", command=delete_by_file_type)
    delete_by_file_type_button.pack()

    delete_by_file_name_button = tk.Button(delete_window, text="Delete by File Name", command=delete_by_file_name)
    delete_by_file_name_button.pack()

    delete_duplicate_folder_button = tk.Button(delete_window, text="Delete Duplicate Folder", command=delete_duplicate_folder)
    delete_duplicate_folder_button.pack()

def show_infrequently_accessed_files():

    if directory_path:
        # Ask the user to enter the threshold in minutes
        threshold_minutes = simpledialog.askinteger("Threshold", "Enter the threshold in minutes:", initialvalue=5)
        if threshold_minutes is not None:
            # Call the backend function to get infrequently accessed files
            infrequently_accessed_files = backend.get_infrequently_accessed_files(directory_path, threshold_minutes)

            # Create a new window to show the table of infrequently accessed files
            infrequently_accessed_window = tk.Toplevel(root)
            infrequently_accessed_window.title("Infrequently Accessed Files")

            # Create a table to display the infrequently accessed files
            table = ttk.Treeview(infrequently_accessed_window)
            table["columns"] = ("Filename", "Filepath")
            table.column("#0", width=0, stretch=tk.NO)
            table.column("Filename", anchor="w", width=200)
            table.column("Filepath", anchor="w", width=400)
            table.heading("Filename", text="Filename")
            table.heading("Filepath", text="Filepath")

            # Insert the large file list into the table
            for item in infrequently_accessed_files:
                table.insert("", tk.END, values=item)

            for column in table["columns"]:
                table.heading(column, command=lambda _col=column: sort_table(table, _col, False))
                # Set random initial width for each column
                random_width = random.randint(100, 200)
                table.column(column, minwidth=0, width=random_width)

            # Pack the table in the search_result_window
            table.pack(expand=True, fill='both')
    else:
        messagebox.showinfo("No Directory Selected", "Please select a directory to view infrequently accessed files.")

# Create the main window with buttons for all the options
browse_button = tk.Button(root, text="Browse Directory", command=browse_directory)
browse_button.pack(pady=10)

browse_button = tk.Button(root, text="Free Space Of Disk", command=get_free_disk_space)
browse_button.pack(pady=10)

browse_button = tk.Button(root, text="Utilized Space Of Disk", command=get_utilized_disk_space)
browse_button.pack(pady=10)

classify_button = tk.Button(root, text="Classify Files", command=classify_files)
classify_button.pack(pady=10)

search_button = tk.Button(root, text="Search File", command=search_file)
search_button.pack(pady=10)

show_large_files_button = tk.Button(root, text="Show Large Files", command=show_large_files)
show_large_files_button.pack(pady=10)

add_file_button = tk.Button(root, text="Add File to Directory", command=add_file)
add_file_button.pack(pady=10)

delete_file_button = tk.Button(root, text="Delete File", command=delete_file)
delete_file_button.pack(pady=10)

delete_file_button = tk.Button(root, text="Infrequently Accessed Files", command=show_infrequently_accessed_files)
delete_file_button.pack(pady=10)

# Start the main event loop
root.mainloop()
