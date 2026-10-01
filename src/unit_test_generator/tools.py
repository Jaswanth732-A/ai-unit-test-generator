"""Tools available to the unit-test agent."""

from pathlib import Path


FILE_PATTERNS = {
    "python": ("{name}.py", "test_{name}.py"),
    "java": ("{name}.java", "{name}Test.java"),
    "c++": ("{name}.cpp", "{name}_test.cpp"),
    "javascript": ("{name}.js", "{name}.test.js"),
    "typescript": ("{name}.ts", "{name}.test.ts"),
    "c#": ("{name}.cs", "{name}Tests.cs"),
}


def select_test_framework(language: str) -> str:
    """Select a common native testing framework."""

    frameworks = {
        "python": "pytest",
        "java": "JUnit 5",
        "c++": "GoogleTest",
        "javascript": "Jest",
        "typescript": "Jest",
        "c#": "xUnit",
    }

    normalized_language = language.strip().lower()

    return frameworks.get(
        normalized_language,
        f"Choose a native testing framework for {language}",
    )


def build_filenames(language: str,module_name: str) -> tuple[str, str]:
    """Create source and test filenames."""

    normalized_language = language.strip().lower()

    if normalized_language not in FILE_PATTERNS:
        raise ValueError(f"Unsupported language: {language}")
    source_pattern, test_pattern = FILE_PATTERNS[normalized_language]
    return (
        source_pattern.format(name=module_name),
        test_pattern.format(name=module_name),
    )


def save_code_files(language: str,module_name: str,source_code: str, generated_tests: str) -> dict[str, str]:
    """Save source code and generated tests in separate files."""

    source_filename, test_filename = build_filenames(language=language,module_name=module_name)

    project_root = Path(__file__).resolve().parents[2]
    output_directory = project_root / "generated_output"
    output_directory.mkdir(exist_ok=True)

    source_path = output_directory / source_filename
    test_path = output_directory / test_filename

    source_path.write_text(source_code, encoding="utf-8")
    test_path.write_text(generated_tests, encoding="utf-8")

    return {
        "source_file": str(source_path),
        "test_file": str(test_path),
    }