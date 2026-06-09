import os
from google.genai import types

MAX_FILES = 50
MAX_CHARS_PER_FILE = 5000


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


def get_folder_content(working_directory, folder_path):
    """Recursively reads all text files from a folder and returns their contents."""
    abs_working_dir = os.path.abspath(working_directory)
    abs_folder_path = os.path.abspath(os.path.join(working_directory, folder_path))
    
    if not abs_folder_path.startswith(abs_working_dir):
        return f'Error: "{folder_path}" is not in the working directory'
    
    if not os.path.isdir(abs_folder_path):
        return f'Error: "{folder_path}" is not a directory'
    
    files_data = []
    file_count = 0
    
    try:
        for root, dirs, files in os.walk(abs_folder_path):
            for file in files:
                if file_count >= MAX_FILES:
                    files_data.append(f"\n[Limit reached: Only first {MAX_FILES} files shown]")
                    break
                
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, abs_folder_path)
                
                # Try to read text files only
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(MAX_CHARS_PER_FILE)
                        if len(content) >= MAX_CHARS_PER_FILE:
                            content += f"\n[... File truncated at {MAX_CHARS_PER_FILE} characters]"
                        files_data.append(f"\n--- FILE: {relative_path} ---\n{content}")
                        file_count += 1
                except Exception as e:
                    files_data.append(f"\n--- FILE: {relative_path} ---\n[Error reading file: {e}]")
            
            if file_count >= MAX_FILES:
                break
    
    except Exception as e:
        return f"Error: {e}"
    
    if not files_data:
        return f"No files found in folder: {folder_path}"
    
    return "".join(files_data)

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


schema_get_folder_content = types.FunctionDeclaration(
    name="get_folder_content",
    description="Recursively reads all text files from a folder and returns their contents. Useful when you need to analyze or process multiple files from a folder.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "folder_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the folder to read files from, relative to working directory. Can be a nested path.",
            ),
        },
        required=["folder_path"],
    ),
)

