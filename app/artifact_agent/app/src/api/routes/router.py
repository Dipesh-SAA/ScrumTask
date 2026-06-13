import shutil
import traceback
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel

from app.artifact_agent.app.src.agents.yml_agent import yml_code_gen
from app.artifact_agent.app.src.agents.openapi_gen import openapi_code_gen


router = APIRouter(tags=["code_generator"])


BASE_DIR = Path(__file__).resolve().parents[2]

YML_DIR = BASE_DIR / "document" / "yml"
YML_FILE = YML_DIR / "openapi.yml"

UPLOAD_DIR = BASE_DIR / "uploads"


class CodeGenRequest(BaseModel):
    task: str
    techstack: str
    instructions: str | None = None


@router.post("/generate-full-api")
async def generate_full_api(request: CodeGenRequest):
    try:

        yml_response = await yml_code_gen(
            task=request.task,
            techstack=request.techstack,
            instructions=request.instructions
        )

        if not YML_FILE.exists():
            raise FileNotFoundError(
                f"Agent 1 did not create YAML file at: {YML_FILE}"
            )

        generated_code = await openapi_code_gen()

        return {
            "status": "success",
            "message": "Agent 1 generated YAML, then Agent 2 generated source code from that YAML.",

            "yaml_used_by_agent_2": generated_code.get("yaml_file"),

            "code_saved_at": generated_code.get("generated_dir"),

            "generated_files": generated_code.get("saved_files"),

            "backend": generated_code.get("backend"),

            "generator": generated_code.get("generator")
        }

    except Exception as exc:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc