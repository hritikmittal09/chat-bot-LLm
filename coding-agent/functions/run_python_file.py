import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
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