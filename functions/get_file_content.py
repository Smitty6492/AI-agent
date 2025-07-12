# functions/get_file_content.py
import os

MAX_FILE_PREVIEW_SIZE = 2000  # or whatever limit you're told to use

def get_file_content(working_directory, file_path):
    try:
        abs_path = os.path.abspath(os.path.join(working_directory, file_path))
        working_dir_abs = os.path.abspath(working_directory)

        # Guard: Ensure path is within working_directory
        if not abs_path.startswith(working_dir_abs):
            return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'

        # Guard: Ensure it's a file
        if not os.path.isfile(abs_path):
            return f'Error: "{file_path}" is not a file'

        # Read and potentially truncate
        with open(abs_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
            if len(content) > MAX_FILE_PREVIEW_SIZE:
                return content[:MAX_FILE_PREVIEW_SIZE] + "\n[Output truncated]"
            return content

    except Exception as e:
        return f"Error: {str(e)}"
