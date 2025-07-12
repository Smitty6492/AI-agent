# AI Agent Project

This project implements a simple AI coding assistant agent that can interact with the filesystem and execute Python code, powered by Google Gemini's language model API. It demonstrates how to integrate an LLM with real-world capabilities such as file management, code execution, and dynamic interaction via natural language prompts.

---

## Features

- **File operations:**  
  - List files and directories within a constrained working directory  
  - Read file contents  
  - Write or overwrite files safely  
- **Code execution:**  
  - Execute Python scripts within the working directory with argument passing and output capturing  
- **LLM integration:**  
  - Uses Google Gemini’s API for natural language understanding and function planning  
  - Supports function call schemas to guide the LLM in performing specific tasks securely  
  - Implements a feedback loop for multi-step interactions with the LLM  

---

## Project Structure

- `calculator/` — Contains a basic calculator app supporting infix expressions with operator precedence  
- `pkg/` — Supporting Python packages like the calculator logic and rendering module  
- `functions/` — Implementations of functions for file operations, code execution, and the function call handler  
- `main.py` — Entry point for the AI agent; accepts natural language prompts and uses the LLM to plan and execute tasks  

---

## Setup

1. Clone the repo:

    ```bash
    git clone https://github.com/your-username/ai-agent.git
    cd ai-agent
    ```

2. Create and activate a Python virtual environment:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate   # Linux/macOS
    .venv\Scripts\activate      # Windows PowerShell
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Add your Gemini API key to a `.env` file in the root directory:

    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

---

## Usage

Run the AI agent with a natural language prompt as a command line argument:

```bash
python main.py "list the contents of the pkg directory" --verbose
python main.py "read the contents of main.py"
python main.py "write 'hello world' to test.txt"
python main.py "run calculator/main.py '3 + 7 * 2'"
