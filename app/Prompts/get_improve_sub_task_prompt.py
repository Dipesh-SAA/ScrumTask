from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate


PROMPT_INPUT_DIR = Path(__file__).resolve().parent / "input_file_improve_subtask"


def read_prompt_file(filename: str) -> str:
    return PROMPT_INPUT_DIR.joinpath(filename).read_text(encoding="utf-8").strip()


SYSTEM_PROMPT = read_prompt_file("system_prompt.md")
CONSTITUTION = read_prompt_file("constitution.md")
SPECIFICATION = read_prompt_file("specification.md")


IMPROVE_SUB_TASK_PROMPT = ChatPromptTemplate.from_template("""
{system_prompt}

CONSTITUTION:
{constitution}

SPECIFICATION:
{specification}

USER STORY:
{user_story}

SUBTASK ID:
{subtask_id}

SUBTASK:
{subtask}
""").partial(
    system_prompt=SYSTEM_PROMPT,
    constitution=CONSTITUTION,
    specification=SPECIFICATION,
)
