import os

def generate_git_commands(base_path="."):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file).replace("\\", "/")  # Fix Windows backslashes
            file_name = os.path.basename(file_path)

            print(f'git add "{file_path}"')
            print(f'git commit -m "added {file_name} file"')
        # for folder in dirs:
        #     folder_path = os.path.join(root, folder).replace("\\", "/")
        #     print(f'git add "{folder_path}"')
        #     print(f'git commit -m "added {folder} folder"')

if __name__ == "__main__":
    generate_git_commands(".")  # current directory
