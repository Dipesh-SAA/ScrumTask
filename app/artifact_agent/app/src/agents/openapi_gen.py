import json
import re
import shutil
from pathlib import Path
import yaml
from app.artifact_agent.app.src.llm.loader import llm
import subprocess

# BASE_DIR = Path(__file__).resolve().parents[1]
# YML_FILE = BASE_DIR / "document/yml" / "openapi.yml"
# # OUTPUT_ROOT = BASE_DIR / "generated_outputs"
# OUTPUT_ROOT = Path(r"C:\inetpub\wwwroot\VibeOp\VibeOPAPIs\Files")

# def clean_json_response(text: str) -> dict:
#     text = str(text).strip()
#     text = re.sub(r"```(?:json)?\s*", "", text, flags=re.IGNORECASE)
#     text = re.sub(r"```", "", text)

#     start = text.find("{")
#     end = text.rfind("}")

#     if start == -1 or end == -1:
#         raise ValueError("No valid JSON found in AI response.")

#     return json.loads(text[start:end + 1])


# def read_yaml_file() -> tuple[str, dict]:
#     if not YML_FILE.exists():
#         raise FileNotFoundError(
#             f"YAML file not found at: {YML_FILE}"
#         )

#     yaml_content = YML_FILE.read_text(encoding="utf-8")
#     yaml_data = yaml.safe_load(yaml_content)

#     if not isinstance(yaml_data, dict):
#         raise ValueError("Invalid YAML file.")

#     return yaml_content, yaml_data


# def get_backend(yaml_data: dict) -> str:
#     backend = yaml_data.get("x-backend")

#     if not backend:
#         raise ValueError(
#             "x-backend missing in YAML. Example: x-backend: python, .net, java, node, c, sqlserver"
#         )

#     backend = str(backend).lower().strip()
#     backend = re.sub(r"\s+", " ", backend)

#     backend_mapping = {
#         "python": "python",
#         "fastapi": "python",

#         ".net": ".net",
#         ".net core": ".net",
#         "dotnet": ".net",
#         "dotnet core": ".net",
#         "c#": ".net",
#         "csharp": ".net",
#         "asp.net": ".net",
#         "asp.net core": ".net",
#         "aspnetcore": ".net",

#         "java": "java",
#         "spring": "java",
#         "spring boot": "java",

#         "node": "node",
#         "nodejs": "node",
#         "express": "node",

#         "c": "c",

#         "sql": "sql",
#         "sqlserver": "sql",
#         "mssql": "sql",
#         "tsql": "sql",
#         "t-sql": "sql",

#         "postgres": "postgresql",
#         "postgresql": "postgresql",

#         "mysql": "mysql",
#         "oracle": "oracle",
#         "react": "react",
#         "angular": "angular",
#         "vue": "vue",
#         "nextjs": "nextjs",
#         "angular": "angular",
#         "ng": "angular",
#         "angularjs": "angular"
#     }

#         # "frontend": "frontend",
#         # "front end": "frontend",
#         # "react": "frontend",
#         # "reactjs": "frontend",
#         # "react.js": "frontend",
#         # "web": "frontend",
#         # "webpage": "frontend",
#         # "website": "frontend",
#         # "ui": "frontend",


#     if backend not in backend_mapping:
#         raise ValueError(f"Unsupported x-backend: {backend}")

#     return backend_mapping[backend]


# def read_prompt_files_by_backend(backend: str) -> tuple[str, str]:
#     prompt_root = BASE_DIR / "document" / "code_generator_document"

#     backend_folder = backend.replace(".", "")

#     constitution_file = prompt_root / backend_folder / "constitution.md"
#     specification_file = prompt_root / backend_folder / "specification.md"

#     if not constitution_file.exists():
#         raise FileNotFoundError(
#             f"Constitution file not found: {constitution_file}"
#         )

#     if not specification_file.exists():
#         raise FileNotFoundError(
#             f"Specification file not found: {specification_file}"
#         )

#     constitution_content = constitution_file.read_text(encoding="utf-8")
#     specification_content = specification_file.read_text(encoding="utf-8")

#     return constitution_content, specification_content


# def detect_language(file_name: str) -> str:
#     ext = Path(file_name).suffix.lower()

#     language_map = {
#     # Python
#     ".py": "python",

#     # .NET
#     ".cs": "csharp",

#     # SQL
#     ".sql": "sql",

#     # React / Angular
#     ".ts": "typescript",
#     ".tsx": "typescript",
#     ".js": "javascript",
#     ".jsx": "javascript",
#     ".html": "html",
#     ".css": "css",
#     ".scss": "scss",

#     # Common
#     ".json": "json",
#     ".yml": "yaml",
#     ".yaml": "yaml",
#     ".xml": "xml",
#     ".md": "markdown",
#     ".txt": "text"
#     }

#     if Path(file_name).name.lower() == "makefile":
#         return "makefile"

#     return language_map.get(ext, "text")


# def normalize_files(files: dict) -> dict:
#     if not isinstance(files, dict):
#         raise ValueError("AI response must contain files object.")

#     normalized = {}

#     for file_name, file_value in files.items():
#         if isinstance(file_value, dict):
#             normalized[file_name] = {
#                 "language": file_value.get("language", detect_language(file_name)),
#                 "content": file_value.get("content", "")
#             }
#         else:
#             normalized[file_name] = {
#                 "language": detect_language(file_name),
#                 "content": str(file_value)
#             }

#     return normalized


# def format_files_for_api(files: dict) -> dict:
#     formatted_files = {}

#     for file_name, file_value in files.items():
#         if isinstance(file_value, dict):
#             content = file_value.get("content", "")
#             language = file_value.get("language") or detect_language(file_name)
#         else:
#             content = file_value
#             language = detect_language(file_name)

#         formatted_files[file_name] = {
#             "language": language,
#             "content": str(content)
#         }

#     return formatted_files


# def build_code_generation_prompt(
#     yaml_content: str,
#     constitution_content: str,
#     specification_content: str,
#     backend: str
# ) -> str:
#     return f"""
# constitution:
# {constitution_content}

# specification:
# {specification_content}

# OpenAPI YAML:
# {yaml_content}

# backend:
# {backend}

# Return format exactly:
# {{
#   "backend": "{backend}",
#   "files": {{
#     "relative/path/file.ext": {{
#       "language": "language_name",
#       "content": "file content here"
#     }}
#   }}
# }}
# """


# def validate_generated_files(files: dict, backend: str):
#     file_names = list(files.keys())

#     if backend == ".net":
#         invalid_files = [
#             file for file in file_names
#             if file.endswith(".py") or file == "requirements.txt"
#         ]

#         if invalid_files:
#             raise ValueError(
#                 f"Wrong code generated. Expected .NET, but got Python files: {invalid_files}"
#             )

#     if backend == "python":
#         invalid_files = [
#             file for file in file_names
#             if file.endswith(".cs") or file.endswith(".csproj")
#         ]

#         if invalid_files:
#             raise ValueError(
#                 f"Wrong code generated. Expected Python, but got C# files: {invalid_files}"
#             )


# def clean_name(name: str) -> str:
#     name = str(name).lower().strip()
#     name = re.sub(r"[^a-z0-9]+", "_", name)
#     return name.strip("_") or "generated_api"


# def save_generated_files(
#     files: dict,
#     backend: str,
#     yaml_data: dict
# ) -> tuple[str, list[str], str]:

#     backend_folder = backend.replace("#", "sharp").replace(" ", "_")

#     api_title = yaml_data.get("info", {}).get(
#         "title",
#         "generated_api"
#     )

#     api_folder = clean_name(api_title)

#     output_dir = OUTPUT_ROOT / backend_folder / api_folder

#     if output_dir.exists():
#         shutil.rmtree(output_dir)

#     output_dir.mkdir(parents=True, exist_ok=True)

#     saved_files = []

#     for relative_path, file_value in files.items():
#         file_path = output_dir / relative_path

#         file_path.parent.mkdir(
#             parents=True,
#             exist_ok=True
#         )

#         if isinstance(file_value, dict):
#             content = file_value.get("content", "")
#         else:
#             content = str(file_value)

#         file_path.write_text(
#             str(content),
#             encoding="utf-8"
#         )

#         saved_files.append(str(file_path))

#     zip_path = shutil.make_archive(
#         str(output_dir),
#         "zip",
#         str(output_dir)
#     )

#     return str(output_dir), saved_files, zip_path


# def validate_dotnet_project(project_dir: str) -> dict:
#     try:
#         restore = subprocess.run(
#             ["dotnet", "restore"],
#             cwd=project_dir,
#             capture_output=True,
#             text=True
#         )

#         build = subprocess.run(
#             ["dotnet", "build"],
#             cwd=project_dir,
#             capture_output=True,
#             text=True
#         )

#         return {
#             "restore_success": restore.returncode == 0,
#             "restore_output": restore.stdout,
#             "restore_error": restore.stderr,
#             "build_success": build.returncode == 0,
#             "build_output": build.stdout,
#             "build_error": build.stderr
#         }

#     except FileNotFoundError as ex:
#         return {
#             "restore_success": False,
#             "restore_output": "",
#             "restore_error": str(ex),
#             "build_success": False,
#             "build_output": "",
#             "build_error": "dotnet SDK not found. Please install .NET SDK."
#         }

# import subprocess

# def validate_react_build(project_dir: str):
#     install_result = subprocess.run(
#         ["npm", "install"],
#         cwd=project_dir,
#         capture_output=True,
#         text=True,
#         shell=True
#     )

#     if install_result.returncode != 0:
#         return {
#             "status": "failed",
#             "step": "npm install",
#             "error": install_result.stderr
#         }

#     build_result = subprocess.run(
#         ["npm", "run", "build"],
#         cwd=project_dir,
#         capture_output=True,
#         text=True,
#         shell=True
#     )

#     if build_result.returncode != 0:
#         return {
#             "status": "failed",
#             "step": "npm run build",
#             "error": build_result.stderr
#         }

#     return {
#         "status": "success",
#         "step": "npm run build",
#         "message": "React project build completed successfully"
#     }

# async def openapi_code_gen():
#     yaml_content, yaml_data = read_yaml_file()

#     backend = get_backend(yaml_data)

#     constitution_content, specification_content = read_prompt_files_by_backend(
#         backend
#     )

#     prompt = build_code_generation_prompt(
#         yaml_content=yaml_content,
#         constitution_content=constitution_content,
#         specification_content=specification_content,
#         backend=backend
#     )

#     response = await llm.ainvoke(prompt)

#     raw_text = getattr(response, "content", response)

#     parsed = clean_json_response(raw_text)

#     files = parsed.get("files")
#     files = normalize_files(files)

#     validate_generated_files(files, backend)

#     generated_dir, saved_files, zip_file = save_generated_files(
#         files,
#         backend,
#         yaml_data
#     )

#     build_validation = None

#     if backend == ".net":
#         build_validation = validate_dotnet_project(generated_dir)

#         if not build_validation["build_success"]:
#             return {
#                 "status": "failed",
#                 "message": "Code generated, but .NET build failed.",
#                 "yaml_file": str(YML_FILE),
#                 "backend": backend,
#                 "generated_dir": str(generated_dir),
#                 "files": files,
#                 "saved_files": saved_files,
#                 "zip_file": str(zip_file),
#                 "build_validation": build_validation
#             }

#     elif backend == "react":
#         build_validation = validate_react_build(str(generated_dir))

#         if build_validation["status"] != "success":
#             return {
#                 "status": "failed",
#                 "message": "Code generated, but React build failed.",
#                 "yaml_file": str(YML_FILE),
#                 "backend": backend,
#                 "generated_dir": str(generated_dir),
#                 "files": files,
#                 "saved_files": saved_files,
#                 "zip_file": str(zip_file),
#                 "build_validation": build_validation
#             }
#     return {
#         "status": "success",
#         "message": "Code generated successfully from YAML using AI.",
#         "yaml_file": str(YML_FILE),
#         "backend": backend,
#         "generated_dir": generated_dir,
#         "files": files,
#         "saved_files": saved_files,
#         "zip_file": zip_file,
#         "build_validation": build_validation
#     }


import json
import re
import shutil
from pathlib import Path
import yaml
from app.artifact_agent.app.src.llm.loader import llm
import subprocess

BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = Path(__file__).resolve().parents[5]

YML_FILE = BASE_DIR / "document/yml" / "openapi.yml"
OUTPUT_ROOT = PROJECT_ROOT / "generated_outputs" / "artifact_agent"
# OUTPUT_ROOT = Path(r"C:\inetpub\wwwroot\VibeOp\VibeOPAPIs\Files")

def clean_json_response(text: str) -> dict:
    text = str(text).strip()
    text = re.sub(r"```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No valid JSON found in AI response.")

    return json.loads(text[start:end + 1])


def read_yaml_file() -> tuple[str, dict]:
    if not YML_FILE.exists():
        raise FileNotFoundError(
            f"YAML file not found at: {YML_FILE}"
        )

    yaml_content = YML_FILE.read_text(encoding="utf-8")
    yaml_data = yaml.safe_load(yaml_content)

    if not isinstance(yaml_data, dict):
        raise ValueError("Invalid YAML file.")

    return yaml_content, yaml_data


def get_backend(yaml_data: dict) -> str:
    backend = yaml_data.get("x-backend")

    if not backend:
        raise ValueError(
            "x-backend missing in YAML. Example: x-backend: python, .net, java, node, c, sqlserver"
        )

    backend = str(backend).lower().strip()
    backend = re.sub(r"\s+", " ", backend)

    backend_mapping = {
        "python": "python",
        "fastapi": "python",

        ".net": ".net",
        ".net core": ".net",
        ".netcore": ".net",
        "dotnet": ".net",
        "dotnet core": ".net",
        "dotnetcore": ".net",
        "c#": ".net",
        "csharp": ".net",
        "asp.net": ".net",
        "asp.net core": ".net",
        "asp.netcore": ".net",
        "aspnetcore": ".net",

        "java": "java",
        "spring": "java",
        "spring boot": "java",

        "node": "node",
        "nodejs": "node",
        "express": "node",

        "c": "c",

        "sql": "sql",
        "sqlserver": "sql",
        "mssql": "sql",
        "tsql": "sql",
        "t-sql": "sql",

        "postgres": "postgresql",
        "postgresql": "postgresql",

        "mysql": "mysql",
        "oracle": "oracle",
        "react": "react",
        "angular": "angular",
        "vue": "vue",
        "nextjs": "nextjs",
        "angular": "angular",
        "ng": "angular",
        "angularjs": "angular",

        # Next.js
        "next": "nextjs",
        "nextjs": "nextjs",
        "next.js": "nextjs",
        
        # node.js
        "node": "nodejs",
        "nodejs": "nodejs",
        "node.js": "nodejs",
        "express": "nodejs",
        "expressjs": "nodejs",
        
        # python flask
        "flask": "flask",
        "python flask": "flask",

    }

        # "frontend": "frontend",
        # "front end": "frontend",
        # "react": "frontend",
        # "reactjs": "frontend",
        # "react.js": "frontend",
        # "web": "frontend",
        # "webpage": "frontend",
        # "website": "frontend",
        # "ui": "frontend",


    if backend not in backend_mapping:
        raise ValueError(f"Unsupported x-backend: {backend}")

    return backend_mapping[backend]


def read_prompt_files_by_backend(backend: str) -> tuple[str, str]:
    prompt_root = BASE_DIR / "document" / "code_generator_document"

    backend_folder = backend.replace(".", "")

    constitution_file = prompt_root / backend_folder / "constitution.md"
    specification_file = prompt_root / backend_folder / "specification.md"

    if not constitution_file.exists():
        raise FileNotFoundError(
            f"Constitution file not found: {constitution_file}"
        )

    if not specification_file.exists():
        raise FileNotFoundError(
            f"Specification file not found: {specification_file}"
        )

    constitution_content = constitution_file.read_text(encoding="utf-8")
    specification_content = specification_file.read_text(encoding="utf-8")

    return constitution_content, specification_content


def detect_language(file_name: str) -> str:
    ext = Path(file_name).suffix.lower()

    language_map = {
    # Python
    ".py": "python",

    # .NET
    ".cs": "csharp",

    # SQL
    ".sql": "sql",

    # React / Angular
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".html": "html",
    ".css": "css",
    ".scss": "scss",

    # Common
    ".json": "json",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".xml": "xml",
    ".md": "markdown",
    ".txt": "text",
    # next.js
    "next": "nextjs",
    "nextjs": "nextjs",
    "next.js": "nextjs",
    
    # node.js
    ".js": "javascript",
    ".json": "json",
    ".md": "markdown",
    ".txt": "text"
    }

    if Path(file_name).name.lower() == "makefile":
        return "makefile"

    return language_map.get(ext, "text")


def normalize_files(files: dict) -> dict:
    if not isinstance(files, dict):
        raise ValueError("AI response must contain files object.")

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

Return format exactly:
{{
  "backend": "{backend}",
  "files": {{
    "relative/path/file.ext": {{
      "language": "language_name",
      "content": "file content here"
    }}
  }}
}}
"""


def validate_generated_files(files: dict, backend: str):
    file_names = list(files.keys())

    if backend == ".net":
        invalid_files = [
            file for file in file_names
            if file.endswith(".py") or file == "requirements.txt"
        ]

        if invalid_files:
            raise ValueError(
                f"Wrong code generated. Expected .NET, but got Python files: {invalid_files}"
            )

    if backend == "python":
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


def save_generated_files(
    files: dict,
    backend: str,
    yaml_data: dict
) -> tuple[str, list[str], str]:

    backend_folder = clean_name(backend.replace("#", "sharp"))

    api_title = yaml_data.get("info", {}).get(
        "title",
        "generated_api"
    )

    api_folder = clean_name(api_title)

    output_dir = OUTPUT_ROOT / backend_folder / api_folder

    if output_dir.exists():
        shutil.rmtree(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []

    for relative_path, file_value in files.items():
        file_path = output_dir / relative_path

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if isinstance(file_value, dict):
            content = file_value.get("content", "")
        else:
            content = str(file_value)

        file_path.write_text(
            str(content),
            encoding="utf-8"
        )

        saved_files.append(str(file_path))

    zip_path = shutil.make_archive(
        str(output_dir),
        "zip",
        str(output_dir)
    )

    return str(output_dir), saved_files, zip_path


def validate_dotnet_project(project_dir: str) -> dict:
    try:
        restore = subprocess.run(
            ["dotnet", "restore"],
            cwd=project_dir,
            capture_output=True,
            text=True
        )

        build = subprocess.run(
            ["dotnet", "build"],
            cwd=project_dir,
            capture_output=True,
            text=True
        )

        return {
            "restore_success": restore.returncode == 0,
            "restore_output": restore.stdout,
            "restore_error": restore.stderr,
            "build_success": build.returncode == 0,
            "build_output": build.stdout,
            "build_error": build.stderr
        }

    except FileNotFoundError as ex:
        return {
            "restore_success": False,
            "restore_output": "",
            "restore_error": str(ex),
            "build_success": False,
            "build_output": "",
            "build_error": "dotnet SDK not found. Please install .NET SDK."
        }

import subprocess

def validate_react_build(project_dir: str):
    install_result = subprocess.run(
        ["npm", "install"],
        cwd=project_dir,
        capture_output=True,
        text=True,
        shell=True
    )

    if install_result.returncode != 0:
        return {
            "status": "failed",
            "step": "npm install",
            "error": install_result.stderr
        }

    build_result = subprocess.run(
        ["npm", "run", "build"],
        cwd=project_dir,
        capture_output=True,
        text=True,
        shell=True
    )

    if build_result.returncode != 0:
        return {
            "status": "failed",
            "step": "npm run build",
            "error": build_result.stderr
        }

    return {
        "status": "success",
        "step": "npm run build",
        "message": "React project build completed successfully"
    }

async def openapi_code_gen():
    yaml_content, yaml_data = read_yaml_file()

    backend = get_backend(yaml_data)

    constitution_content, specification_content = read_prompt_files_by_backend(
        backend
    )

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

    validate_generated_files(files, backend)

    generated_dir, saved_files, zip_file = save_generated_files(
        files,
        backend,
        yaml_data
    )

    build_validation = None

    if backend == ".net":
        build_validation = validate_dotnet_project(generated_dir)

        if not build_validation["build_success"]:
            return {
                "status": "failed",
                "message": "Code generated, but .NET build failed.",
                "yaml_file": str(YML_FILE),
                "backend": backend,
                "generated_dir": str(generated_dir),
                "files": files,
                "saved_files": saved_files,
                "zip_file": str(zip_file),
                "build_validation": build_validation
            }

    elif backend == "react":
        build_validation = validate_react_build(str(generated_dir))

        if build_validation["status"] != "success":
            return {
                "status": "failed",
                "message": "Code generated, but React build failed.",
                "yaml_file": str(YML_FILE),
                "backend": backend,
                "generated_dir": str(generated_dir),
                "files": files,
                "saved_files": saved_files,
                "zip_file": str(zip_file),
                "build_validation": build_validation
            }
    return {
        "status": "success",
        "message": "Code generated successfully from YAML using AI.",
        "yaml_file": str(YML_FILE),
        "backend": backend,
        "generated_dir": generated_dir,
        "files": files,
        "saved_files": saved_files,
        "zip_file": zip_file,
        "build_validation": build_validation
    }
