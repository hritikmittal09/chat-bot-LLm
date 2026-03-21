import os
from google.genai import types
 
MAX_CHARS = 10000
 
 
def get_file_content(working_directory, file_path):
    """Read and return the content of a file."""
    ...
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path   = os.path.abspath(os.path.join(working_directory, file_path))
 
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: "{file_path}" is not in the working dir'
 
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file'
 
    file_content_string = ""
 
    try:
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) >= MAX_CHARS:
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
    except Exception as e:
        return f"Error: {e}"
 
    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the full text content of a file. Truncated at 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to working directory.",
            ),
        },
        required=["file_path"],
    ),
)