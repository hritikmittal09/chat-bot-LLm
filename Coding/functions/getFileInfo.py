import os
from google.genai import types



 
 
def get_files_info(working_directory= ".", directory=None):
    """List files in a directory. Returns file names, sizes, and is_dir flags."""
    ...
    abs_working_dir = os.path.abspath(working_directory)
 
    if directory is None:
        directory = working_directory
 
    abs_directory = os.path.abspath(directory)
 
    if not abs_directory.startswith(abs_working_dir):
        return f'Error: "{directory}" is not a directory'
 
    final_response = ""
 
    contents = os.listdir(abs_directory)
    for content in contents:
        content_path = os.path.join(abs_directory, content)
        is_dir = os.path.isdir(content_path)
        size = os.path.getsize(content_path)
        final_response += f"- {content}: file_size={size} bytes, is_dir={is_dir}\n"
 
    return final_response

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to..."
            ),
        },
    ),
)

