
import os


LIMIT = 10000
def get_file_content(working_directory, file_path):
    working_path = os.path.abspath(working_directory)
    file_dir_path = os.path.normpath(os.path.join(working_path, file_path))
    common_path = os.path.commonpath([working_path, file_dir_path]) 
    if not common_path == working_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    file = os.path.join(working_path, file_path)
    if not os.path.isfile(file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    with open(file, "r") as f:
        return f.read(LIMIT)
