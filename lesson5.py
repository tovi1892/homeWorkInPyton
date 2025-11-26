import os
#1
name = "my _new _folder"
#os.mkdir(name)

#3,4
folder_path = "Z:\יד תשפו\שמש שירה\py\my _new _folder"
new = "newr.txt"
full_file_path = os.path.join(folder_path, new)
os.makedirs(folder_path, exist_ok=True)
with open(full_file_path, "w") as file:
    file.write("This is some content for the new file.")
print(f"File '{new}' created successfully in '{folder_path}'.")
#5
file_to_delete = "new.txt"

if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"File '{file_to_delete}' deleted successfully.")
else:
    print(f"File '{file_to_delete}' does not exist.")

#6
list="Z:\יד תשפו\שמש שירה\py\my _new _folder"
if os.path.exists(list):
    print(f"Contents of {list}:{os.listdir('.')}")
else:
    print(f"Directory not found: {list}")
#7
print(f"The current working directory is: { os.getcwd()}")
#2
try:
    with open(full_file_path, "w") as file:
        file.write("This is some content for the new file.")
    print(f"File '{new}' created successfully in '{folder_path}'.")
except FileExistsError:
    print(f"File '{new}' already exists in '{folder_path}'.")
except Exception as e:
    print(f"An error occurred: {e}")

folder_path = "Z:\יד תשפו\שמש שירה\py\my _new _folder"

if os.path.isdir(folder_path) and not os.listdir(folder_path):
    try:
        os.rmdir(folder_path)
        print(f"Empty folder '{folder_path}' deleted successfully.")
    except OSError as e:
        print(f"Error deleting folder '{folder_path}': {e}")
else:
    print(f"Folder '{folder_path}' is not empty or does not exist.")

