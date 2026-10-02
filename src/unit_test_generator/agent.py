"""OpenAI agent for generating unit tests."""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from unit_test_generator.tools import (
    save_code_files,
    select_test_framework,
    build_filenames
)
from unit_test_generator.prompts import (
    AGENT_INSTRUCTIONS,
    build_user_prompt,
)


load_dotenv()

MODEL = "gpt-5-nano"

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

TOOLS = [
    {
        "type": "function",
        "name": "select_test_framework",
        "description": (
            "Select the native unit-testing framework "
            "for a programming language."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                }
            },
            "required": ["language"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "save_code_files",
        "description": (
            "Save source code and generated unit tests "
            "into separate files."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                },
                "module_name": {
                    "type": "string",
                },
                "generated_tests": {
                    "type": "string",
                },
            },
            "required": [
                "language",
                "module_name",
                "generated_tests",
            ],
            "additionalProperties": False,
        },
        "strict": True,
    },
]

def execute_tool(tool_name: str,arguments: dict,original_source_code: str) -> str:
    """Execute the function requested by the model."""
    if tool_name == "select_test_framework":
        return select_test_framework(language=arguments["language"])

    if tool_name == "save_code_files":
        result = save_code_files(
            language=arguments["language"],
            module_name=arguments["module_name"],
            source_code=original_source_code,
            generated_tests=arguments["generated_tests"],
        )

        return json.dumps(result)

    raise ValueError(f"Unknown tool: {tool_name}")

def run_tool_loop(response,original_source_code: str):
    """Continue until OpenAI stops requesting tools."""
    current_response = response
    while True:
        tool_outputs = []
        for item in current_response.output:
            if item.type != "function_call":
                continue
            arguments = json.loads(item.arguments)
            result = execute_tool(
                tool_name=item.name,
                arguments=arguments,
                original_source_code=original_source_code,
            )
            tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": result,
                })
        if not tool_outputs:
            return current_response

        current_response = client.responses.create(
            model=MODEL,
            previous_response_id=current_response.id,
            input=tool_outputs,
            tools=TOOLS,
        )

def generate_unit_tests(language: str,module_name: str,source_code: str) -> str:
    """Generate tests and save both source and test files."""
    if not language.strip():
        raise ValueError("Language cannot be empty.")
    if not module_name.strip():
        raise ValueError("Module name cannot be empty.")
    if not source_code.strip():
        raise ValueError("Source code cannot be empty.")
    prompt = build_user_prompt(language=language,module_name=module_name,source_code=source_code)

    first_response = client.responses.create(
        model=MODEL,
        instructions=AGENT_INSTRUCTIONS,
        input=prompt,
        tools=TOOLS,
    )

    final_response = run_tool_loop(
    first_response,
    original_source_code=source_code,
    )

    return final_response.output_text

def get_user_input() -> tuple[str, str, str]:
    """Collect language, module name, and source code from the terminal."""
    language = input("Enter programming language: ").strip()
    module_name = input("Enter module or class name: ").strip()

    print("\nPaste the source code.")
    print("Type END on a separate line when finished:\n")

    source_lines = []

    while True:
        line = input()
        if line.strip() == "END":
            break
        source_lines.append(line)
    source_code = "\n".join(source_lines)
    return language, module_name, source_code

if __name__ == "__main__":
    language, module_name, source_code = get_user_input()

    result = generate_unit_tests(
        language=language,
        module_name=module_name,
        source_code=source_code,
    )

    print("\nAgent response:\n")
    print(result)