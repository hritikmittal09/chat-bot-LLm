import os
def write_file(working_directory, file_path, content):
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