import os

def write_file(working_directory, file_path, content):
    # Get absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Check if file is outside of working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    # Create parent directories if needed
    try:
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        with open(abs_file_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {str(e)}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
