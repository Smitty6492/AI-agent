# functions/call_function.py
from google.genai import types  # from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

WORKING_DIR = "./calculator"

# Map function names (strings) to the real Python callables
_FUNCTION_TABLE = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(function_call_part: types.FunctionCall, verbose: bool = False) -> types.Content:
    """
    Executes one of our four sandbox functions based on the LLM's FunctionCall
    object, then wraps the result in a `types.Content` tool response so the
    model can see the output.
    """
    function_name = function_call_part.name
    fn = _FUNCTION_TABLE.get(function_name)

    # Show what we're about to do
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    # If the model referenced an unknown function, respond with an error
    if fn is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Inject the working directory and run the real function
    kwargs = dict(function_call_part.args)  # make a copy
    kwargs["working_directory"] = WORKING_DIR
    try:
        result_str = fn(**kwargs)
    except Exception as e:
        result_str = f"Error while running {function_name}: {e}"

    # Wrap the string result in the proper Content object
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result_str},
            )
        ],
    )
