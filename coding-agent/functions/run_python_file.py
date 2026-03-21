import os
import subprocess
from google.genai import types






def run_python_file(working_directory, file_path, args=None):
    """Run a Python file and return its stdout and stderr output."""



    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path   = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: "{file_path}" is not in the working dir'

    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    try:
        cmd = ["python", abs_file_path] + (args or [])
        result = subprocess.run(
            cmd,
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True,
            text=True,
        )

        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}"
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"
        if not output:
            output = "File ran with no output"

        return output

    except subprocess.TimeoutExpired:
        return "Error: script timed out after 30 seconds"
    except Exception as e:
        return f"Error: {e}"



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python (.py) file and returns its stdout and stderr output. Times out after 30 seconds.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of CLI arguments to pass to the script.",
            ),
        },
        required=["file_path"],
    ),
)