import os

def get_files_info(working_directory, directory="."):
    path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(path, directory))
    if not os.path.commonpath([path, target_path]) == path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    contents = os.listdir(target_path)
    result = ""
    for f in contents:
        file_path = os.path.join(target_path, f)
        size = os.path.getsize(file_path)
        is_dir = os.path.isdir(file_path)
        result += f"\n- {f}: file_size={size} bytes, is_dir={is_dir}"
    return result

