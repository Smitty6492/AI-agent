import os, sys, traceback

from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import (
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
    
    )
from functions.call_function import call_function
from functions.get_files_info import (
    schema_get_files_info, schema_get_file_content,
    schema_run_python_file, schema_write_file
)



load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

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

#--------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py <prompt> [--verbose]")
        sys.exit(1)

    verbose = "--verbose" in sys.argv
    user_prompt = " ".join(arg for arg in sys.argv[1:] if arg != "--verbose")

    if verbose:
        print("Hello from ai‑agent!")
        print(f'User prompt: "{user_prompt}"')

    # --- conversation state ---
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    for turn in range(20):                       # hard cap to avoid loops
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,               # always pass full history
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[available_functions],
                ),
            )
        except Exception as e:
            print(f"Fatal LLM error: {e}")
            traceback.print_exc()
            sys.exit(1)

        # --- add ALL candidate messages to the conversation -------------
        for cand in response.candidates:         # usually 1, but spec says list
            messages.append(cand.content)

        # If the top candidate has plain text, we're done -----------------
        top = response.candidates[0]
        if top.content.parts and top.content.parts[0].text:
            final_text = top.content.parts[0].text
            print("Final response:\n" + final_text)
            if verbose:
                meta = response.usage_metadata
                print(f"\nPrompt tokens:   {meta.prompt_token_count}")
                print(f"Response tokens: {meta.candidates_token_count}")
            break  # conversation finished

        # Otherwise the top candidate contains a function call -----------
        # helper to pull out any function‑call parts
        fc_parts = [
            part.function_call
            for part in top.content.parts
            if getattr(part, "function_call", None) is not None
        ]

        if fc_parts:                   # we have at least one function call
            fc_part = fc_parts[0]      # take the first
            tool_resp = call_function(fc_part, verbose=verbose)
            messages.append(tool_resp)
            if verbose:
                print(f"-> {tool_resp.parts[0].function_response.response}")
        else:
            # no function call → treat as plain text
            final_text = top.content.parts[0].text
            print("Final response:\n" + final_text)
            break
    else:
        print("Reached maximum iterations (20) without finishing.")

#-------------------------------------------------
if __name__ == "__main__":
    main()
