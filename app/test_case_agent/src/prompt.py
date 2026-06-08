from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DOCUMENT_DIR = BASE_DIR / "document"


PROMPT_TEMPLATE = """

CONSTITUTION:
{constitution}

USER PROMPT:
{user_prompt}

SPECIFICATION:
{specification}

user_story:
{user_story}

task:
{task}

Your work is to read the user input, constitution file, specification file,
and user prompt, then respond strictly according to those documents.

Return ONLY valid JSON.
Do not return markdown.
Do not return code fences.
Do not return explanations.
Do not return text before or after the JSON.
"""


def load_document(name: str) -> str:
    return (DOCUMENT_DIR / name).read_text(encoding="utf-8")


def build_prompt(user_story: str,task: str) -> str:
    return PROMPT_TEMPLATE.format(
        constitution=load_document("constitution.md"),
        specification=load_document("specification.md"),
        user_prompt=load_document("user_prompt.md"),
        user_story=user_story,
        task=task
    )
