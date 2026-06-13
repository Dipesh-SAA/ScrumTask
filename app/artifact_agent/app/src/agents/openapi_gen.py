import json
import re
import shutil
from pathlib import Path
import yaml
from app.artifact_agent.app.src.llm.loader import llm
# from app.artifact_agent.app.src.prompt.prompt import build_prompt, PROMPT_TEMPLATE

BASE_DIR = Path(__file__).resolve().parents[1]

YML_FILE = BASE_DIR / "document/yml" / "openapi.yml"
CONSTITUTION_FILE = BASE_DIR / "document/code_generator_document" / "constitution.md"
SPECIFICATION_FILE = BASE_DIR / "document/code_generator_document" / "specification.md"
# OUTPUT_ROOT = BASE_DIR / "generated_outputs" / "ai_generated"
OUTPUT_ROOT = BASE_DIR / "generated_outputs" 

def clean_json_response(text: str) -> dict:
    text = str(text).strip()
    text = re.sub(r"```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No valid JSON found in AI response.")

    return json.loads(text[start:end + 1])


# def read_yaml_file() -> tuple[str, dict]:
#     if not YML_FILE.exists():
#         raise FileNotFoundError(f"YAML file not found at: {YML_FILE}")

#     yaml_content = YML_FILE.read_text(encoding="utf-8")
#     yaml_data = yaml.safe_load(yaml_content)

#     if not isinstance(yaml_data, dict):
#         raise ValueError("Invalid YAML file.")

#     return yaml_content, yaml_data

def read_yaml_file() -> tuple[str, dict, str, str]:
    if not YML_FILE.exists():
        raise FileNotFoundError(
            f"YAML file not found at: {YML_FILE}"
        )

    if not CONSTITUTION_FILE.exists():
        raise FileNotFoundError(
            f"Constitution file not found at: {CONSTITUTION_FILE}"
        )

    if not SPECIFICATION_FILE.exists():
        raise FileNotFoundError(
            f"Specification file not found at: {SPECIFICATION_FILE}"
        )

    yaml_content = YML_FILE.read_text(encoding="utf-8")

    yaml_data = yaml.safe_load(yaml_content)

    if not isinstance(yaml_data, dict):
        raise ValueError("Invalid YAML file.")

    constitution_content = CONSTITUTION_FILE.read_text(
        encoding="utf-8"
    )

    specification_content = SPECIFICATION_FILE.read_text(
        encoding="utf-8"
    )

    return (
        yaml_content,
        yaml_data,
        constitution_content,
        specification_content
    )


def get_backend(yaml_data: dict) -> str:
    backend = yaml_data.get("x-backend")

    if not backend:
        raise ValueError(
            "x-backend missing in YAML. Example: x-backend: python or x-backend: c#"
        )

    return str(backend).lower().strip()
def detect_language(file_name: str) -> str:
    ext = Path(file_name).suffix.lower()

    language_map = {
        ".py": "python",
        ".cs": "csharp",
        ".c": "c",
        ".sql": "sql",
        ".java": "java",
        ".js": "javascript",
        ".ts": "typescript",
        ".json": "json",
        ".yml": "yaml",
        ".yaml": "yaml",
        ".xml": "xml",
        ".md": "markdown",
        ".txt": "text",
    }

    if Path(file_name).name.lower() == "makefile":
        return "makefile"

    return language_map.get(ext, "text")


def normalize_files(files: dict) -> dict:
    normalized = {}

    for file_name, file_value in files.items():
        if isinstance(file_value, dict):
            normalized[file_name] = {
                "language": file_value.get("language", detect_language(file_name)),
                "content": file_value.get("content", "")
            }
        else:
            normalized[file_name] = {
                "language": detect_language(file_name),
                "content": str(file_value)
            }

    return normalized

def format_files_for_api(files: dict) -> dict:
    formatted_files = {}

    for file_name, file_value in files.items():
        if isinstance(file_value, dict):
            content = file_value.get("content", "")
            language = file_value.get("language") or detect_language(file_name)
        else:
            content = file_value
            language = detect_language(file_name)

        formatted_files[file_name] = {
            "language": language,
            "content": str(content)
        }

    return formatted_files
    
def build_code_generation_prompt(
    yaml_content: str,
    constitution_content: str,
    specification_content: str,
    backend: str
) -> str:
    return f"""
constitution:    
{constitution_content}

specification:
{specification_content}

OpenAPI YAML:
{yaml_content}

backend:
{backend}

CRITICAL RULES:
- Generate source code only.
- Do not generate YAML.
- Do not generate OpenAPI again.
- Use x-backend from YAML.
- If x-backend is python or fastapi, generate Python FastAPI files.
- If x-backend is c#, csharp, .net, asp.net, or aspnetcore, generate C# ASP.NET Core files.
- Return ONLY valid JSON.
- No markdown.
- No explanation.
- JSON must contain a top-level "files" object.

Return format exactly:
{{
  "backend": "{backend}",
  "files": {{
    "relative/path/file.ext": "file content here"
  }}
}}

"""

# def build_code_generation_prompt(yaml_content: str ,constitution_content: str ,specification_content: str , backend: str) -> str:
#     return f"""

# specification:
# {specification_content}

# specification
# {constitution_content}

# OpenAPI YAML:
# {yaml_content}

# """


def validate_generated_files(files: dict, backend: str):
    file_names = list(files.keys())

    if backend in ["c#", "csharp", "asp.net", "aspnetcore"]:
        invalid_files = [
            file for file in file_names
            if file.endswith(".py") or file == "requirements.txt"
        ]

        if invalid_files:
            raise ValueError(
                f"Wrong code generated. Expected C#, but got Python files: {invalid_files}"
            )

    if backend in ["python", "fastapi"]:
        invalid_files = [
            file for file in file_names
            if file.endswith(".cs") or file.endswith(".csproj")
        ]

        if invalid_files:
            raise ValueError(
                f"Wrong code generated. Expected Python, but got C# files: {invalid_files}"
            )

def clean_name(name: str) -> str:
    name = str(name).lower().strip()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_") or "generated_api"


def get_unique_output_dir(base_dir: Path) -> Path:
    output_dir = base_dir
    counter = 1

    while output_dir.exists():
        output_dir = Path(f"{base_dir}_{counter}")
        counter += 1

    return output_dir


def save_generated_files(
    files: dict,
    backend: str,
    yaml_data: dict
) -> tuple[str, list[str]]:

    backend_folder = backend.replace("#", "sharp").replace(" ", "_")

    api_title = yaml_data.get("info", {}).get(
        "title",
        "generated_api"
    )

    api_folder = clean_name(api_title)

    output_dir = OUTPUT_ROOT / backend_folder / api_folder

    # Remove old generated folder completely
    if output_dir.exists():
        shutil.rmtree(output_dir)

    # Create fresh folder
    output_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []

    for relative_path, content in files.items():

        file_path = output_dir / relative_path

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if isinstance(content, dict):
            content = content.get("content", "")

        file_path.write_text(
            str(content),
            encoding="utf-8"
        )

        saved_files.append(str(file_path))

    return str(output_dir), saved_files
# def save_generated_files(files: dict, backend: str, yaml_data: dict) -> tuple[str, list[str]]:
#     backend_folder = backend.replace("#", "sharp").replace(" ", "_")

#     api_title = yaml_data.get("info", {}).get("title", "generated_api")
#     api_folder = clean_name(api_title)

#     output_dir = OUTPUT_ROOT / backend_folder / api_folder
#     output_dir = get_unique_output_dir(output_dir)

#     output_dir.mkdir(parents=True, exist_ok=True)

#     saved_files = []

#     for relative_path, content in files.items():
#         file_path = output_dir / relative_path
#         file_path.parent.mkdir(parents=True, exist_ok=True)

#         # file_path.write_text(str(content), encoding="utf-8")

#         if isinstance(content, dict):
#             content = content.get("content", "")

#         file_path.write_text(str(content), encoding="utf-8")

#         saved_files.append(str(file_path))

#     return str(output_dir), saved_files
# def save_generated_files(files: dict, backend: str) -> tuple[str, list[str]]:
#     output_dir = OUTPUT_ROOT / backend.replace("#", "sharp").replace(" ", "_")

#     if output_dir.exists():
#         shutil.rmtree(output_dir)

#     output_dir.mkdir(parents=True, exist_ok=True)

#     saved_files = []

#     for relative_path, content in files.items():
#         file_path = output_dir / relative_path
#         file_path.parent.mkdir(parents=True, exist_ok=True)

#         file_path.write_text(str(content), encoding="utf-8")

#         saved_files.append(str(file_path))

#     return str(output_dir), saved_files


async def openapi_code_gen():
    # yaml_content, yaml_data = read_yaml_file()
    yaml_content, yaml_data, constitution_content, specification_content = read_yaml_file()
    backend = get_backend(yaml_data)

    prompt = build_code_generation_prompt(
        yaml_content=yaml_content,
        constitution_content=constitution_content,
        specification_content=specification_content,
        backend=backend
    )

    response = await llm.ainvoke(prompt)

    raw_text = getattr(response, "content", response)

    parsed = clean_json_response(raw_text)

    files = parsed.get("files")
    files = normalize_files(files)
    if not isinstance(files, dict):
        raise ValueError("AI response must contain files object.")

    validate_generated_files(files, backend)

    # generated_dir, saved_files = save_generated_files(files, backend)
    generated_dir, saved_files = save_generated_files(files, backend, yaml_data)

    return {
        "status": "success",
        "message": "Code generated successfully from YAML using AI.",
        "yaml_file": str(YML_FILE),
        "backend": backend,
        "generated_dir": generated_dir,
        "files": files,
        "saved_files": saved_files
    }