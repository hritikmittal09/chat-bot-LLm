import os
from google.genai import types  # ✅ add this
def write_file(working_directory, file_path, content):
     
    """Write content to a file. Creates directories if needed."""
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path   = os.path.abspath(os.path.join(working_directory, file_path))
 
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: "{file_path}" is not in the working dir'
 
    try:
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
 
 
def make_dir(working_directory, dir_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_dir_path    = os.path.abspath(os.path.join(working_directory, dir_path))
 
    if not abs_dir_path.startswith(abs_working_dir):
        return f'Error: "{dir_path}" is not in the working dir'
 
    try:
        os.makedirs(abs_dir_path, exist_ok=True)
        return f'Successfully created directory "{dir_path}"'
    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file. Creates parent directories automatically if they don't exist. Overwrites if file already exists.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write into the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

schema_make_dir = types.FunctionDeclaration(
    name="make_dir",
    description="Creates a directory. Creates nested directories if needed. No error if already exists.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "dir_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to create, relative to working directory.",
            ),
        },
        required=["dir_path"],
    )
)
