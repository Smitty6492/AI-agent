import os
from google.genai import types

# 1. The schema declaration (separate, at module level)
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

#----- New Content --------------------
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a single text file in the working directory tree.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to working directory.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file (optionally with CLI args) that lives inside the working directory, returning its stdout / stderr.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Python file to run, relative to working directory.",
            ),
            "arguments": types.Schema(
                type=types.Type.STRING,
                description="Optional command‑line argument string to pass to the script.",
                nullable=True,
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text to a file (creating or overwriting). Fails if path is outside working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path (relative) for the file to create or overwrite.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The entire text content to write into the file.",
            ),
        },
    ),
)
#-----------------------

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

#2. The actual function implementation
def get_files_info(working_directory, directory=None):
    try:
        directory = directory or "."
        
        # Create absolute paths
        full_path = os.path.abspath(os.path.join(working_directory, directory))
        working_dir_abs = os.path.abspath(working_directory)

        # Guard: Directory must be inside the working directory
        if not full_path.startswith(working_dir_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Guard: Must be a directory
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        # List and describe files
        output = []
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            try:
                size = os.path.getsize(item_path)
                is_dir = os.path.isdir(item_path)
                output.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as e:
                output.append(f"- {item}: Error getting info: {str(e)}")

        return "\n".join(output)

    except Exception as e:
        return f"Error: {str(e)}"        