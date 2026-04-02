
import os


def write_file(working_directory, file_path, content):
    working_dir = os.path.abspath(working_directory)
    file = os.path.normpath(os.path.join(working_dir, file_path))
    common_path = os.path.commonpath([working_dir, file])
    # print(f"file: {file} from {file_path}, working_dir: {working_dir}, comon: {common_path},", common_path == working_dir)
    if common_path != working_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, 'w') as f:
        f.write(content)
        return f'Successfully wrote to "{file_path} ({len(content)} characters written)'

