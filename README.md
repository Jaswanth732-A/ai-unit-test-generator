# AI Unit Test Generator

A simple AI-powered application that generates unit tests from source code.

The application uses OpenAI tool calling to:

1. Select a suitable testing framework.
2. Generate unit tests.
3. Save the original code and generated tests into separate files.

## Supported Languages

The current version supports:

- Python with pytest
- Java with JUnit
- C++ with GoogleTest
- JavaScript with Jest
- TypeScript with Jest
- C# with xUnit

## How It Works

```text
User enters language, module name, and source code
                    ↓
OpenAI selects the testing framework
                    ↓
OpenAI generates unit tests
                    ↓
The application saves both files
```

For example, if the user enters:

```text
Language: Python
Module name: calculator
```

The application creates:

```text
generated_output/
├── calculator.py
└── test_calculator.py
```

## Project Structure

```text
ai-unit-test-generator/
├── src/
│   └── unit_test_generator/
│       ├── __init__.py
│       ├── agent.py
│       ├── prompts.py
│       └── tools.py
├── tests/
├── examples/
├── generated_output/
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Main Files

### `agent.py`

Connects to OpenAI and manages the tool-calling workflow.

### `tools.py`

Contains the Python tools used by the agent:

- Select a testing framework
- Build source and test filenames
- Save source code and generated tests

### `prompts.py`

Contains the prompts and instructions sent to OpenAI.

## Setup

### 1. Clone the repository

```powershell
git clone YOUR_REPOSITORY_URL
cd ai-unit-test-generator
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install the project

```powershell
python -m pip install -e ".[dev]"
```

### 5. Create the environment file

Copy `.env.example`:

```powershell
Copy-Item .env.example .env
```

Add your OpenAI API key to `.env`:

```text
OPENAI_API_KEY=your-openai-api-key
```

Do not commit the `.env` file.

## Run the Application

From the project root:

```powershell
python -m unit_test_generator.agent
```

The application will ask for:

```text
Enter programming language:
Enter module or class name:
Paste the source code:
```

Enter `END` on a separate line after pasting the source code.

## Example

```text
Enter programming language: Python
Enter module or class name