import os
from functions.getFileInfo import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import make_dir, write_file

WORKING_DIR = "Calculartor"

tool_map = {
    "get_files_info":   get_files_info,
    "get_file_content": get_file_content,
    "run_python_file":  run_python_file,
    "make_dir":         make_dir,
    "write_file":       write_file,
}

def call_function(function_call, verbose=False):
    name = function_call.name
    args = dict(function_call.args)
    args["working_directory"] = WORKING_DIR  # ✅ inject once

    fn = tool_map.get(name)
    if fn is None:
        return f'Error: unknown function "{name}"'

    return fn(**args)  # ✅ call only once