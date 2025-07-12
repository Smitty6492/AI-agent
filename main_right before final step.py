import os, sys, traceback

from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import (
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
    available_functions,
    )
from functions.call_function import call_function




load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function‑call plan.  
You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths must be **relative to the working directory**.  
You never supply the working_directory argument—that is injected automatically for security reasons.
"""
#"Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""

def main():
    print("Hello from ai-agent!")

    # Define your prompt
    #prompt = "Tell me a fun fact about space."
    #prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    # Check if prompt is provided
    if len(sys.argv) < 2:
        print("Error: Please provide a prompt as a command-line argument.")
        sys.exit(1)

     # Determine if --verbose flag is present
    verbose = "--verbose" in sys.argv

    # Remove --verbose from the arguments if it exists
    args = [arg for arg in sys.argv[1:] if arg != "--verbose"]
    
    # Join all arguments as the prompt string
    #prompt = " ".join(sys.argv[1:])
    prompt = " ".join(args)
    
    # If verbose, print the prompt
    if verbose:
        print(f'User prompt: "{prompt}"')
    
    messages = [    
    types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    
    

    
    
    # Call the model with required parameters
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        #contents=prompt
        contents = messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt),
    )

    # --------------------------------------
    """
    if response.function_calls:
        # Gemini puts function calls in a list; take the first (or loop over them)
        function_call_part = response.function_calls[0]
        # `.name` is the function name, `.args` (already a dict) are the arguments
        print(f'Calling function: {function_call_part.name}({function_call_part.args})')
    else:
        # No function call – fall back to normal text response
        print("Response from Gemini:")
        print(response.text)    
    """
    if response.function_calls:
        fc_part = response.function_calls[0]  # you could loop, but one is fine for now

        # Dispatch and get a Content object describing the result
        tool_content = call_function(fc_part, verbose="--verbose" in sys.argv)

        # Ensure the function actually returned a response dict
        if not (
            tool_content.parts
            and tool_content.parts[0].function_response
            and tool_content.parts[0].function_response.response
        ):
            raise RuntimeError("Function did not return a proper function_response")

        if "--verbose" in sys.argv:
            print(f"-> {tool_content.parts[0].function_response.response}")

    else:
        # Normal text response
        print("Response from Gemini:")
        print(response.text)
    # --------------------------------------
    
    # Print the response text
    #print("Response from Gemini:")
    #print(response.text)
    
    # Print token usage 
    if verbose:
        usage = response.usage_metadata
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")

if __name__ == "__main__":
    main()
