import os

from google.genai import types


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


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents in a specified directory in relative to the working directory, providing file contents",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path, relative to the working directory (default is the working directory itself)",
            )
        },
        required=["file_path"]
    ),
)
