from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from app.Infrastrature.llm.loader import llm
from app.Prompts.get_prompt_template_constitution import CONSTITUTION_GENERATOR_PROMPT
from app.Prompts.get_prompt_template_test_case import TEST_CASE_GENERATOR_PROMPT
from app.Prompts.get_prompt_template_specification import SPECIFICATION_GENERATOR_PROMPT
from app.Prompts.get_prompt_template_task import TASK_GENERATOR_PROMPT
from app.Schema.State import InputState

from app.Prompts.get_prompt_template_user_story import (
    USER_STORY_GENERATOR_PROMPT
)

BASE_DIR = Path(__file__).resolve().parents[3]
CONSTITUTION_PATH = BASE_DIR / "AI  Agent Global Consitution (1).docx"
OUTPUT_DIR = BASE_DIR / "generated_md"


def save_markdown(filename: str, content: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.joinpath(filename).write_text(content.strip(), encoding="utf-8")


def read_context_file(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        with ZipFile(path) as docx:
            document_xml = docx.read("word/document.xml")

        root = ET.fromstring(document_xml)
        namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        paragraphs = []

        for paragraph in root.findall(".//w:p", namespace):
            text = "".join(
                node.text or ""
                for node in paragraph.findall(".//w:t", namespace)
            )
            if text.strip():
                paragraphs.append(text)

        return "\n".join(paragraphs)

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="cp1252")


async def chat_constitution_llm(state: InputState):
    retrieved_context = read_context_file(CONSTITUTION_PATH)
    formatted_messages = CONSTITUTION_GENERATOR_PROMPT.invoke(
        {
            "user_input": state["user_input"],
            "retrieved_context": retrieved_context,
        }
    )
    response = await llm.ainvoke(formatted_messages)
    save_markdown("constitution.md", response.content)
    return {"constitution": response.content}


async def chat_specification_llm(state: InputState):
    formatted_messages = SPECIFICATION_GENERATOR_PROMPT.invoke(
        {
            "user_input": state["user_input"],
            "constitution": state["constitution"],
        }
    )
    response = await llm.ainvoke(formatted_messages)
    save_markdown("specification.md", response.content)
    return {"specification": response.content}


# async def chat_planning_llm(state: InputState):
#     formatted_messages = PLANNING_GENERATOR_PROMPT.invoke(
#         {
#             "constitution": state["constitution"],
#             "specification": state["specification"],
#         }
#     )
#     response = await llm.ainvoke(formatted_messages)
#     save_markdown("planning.md", response.content)
#     return {"planning": response.content}


# async def chat_task_llm(state: InputState):
#     formatted_messages = TASK_GENERATOR_PROMPT.invoke(
#         {
#             "constitution": state["constitution"],
#             "specification": state["specification"],
#             "planning": state["planning"],
#         }
#     )
#     response = await llm.ainvoke(formatted_messages)
#     save_markdown("task.md", response.content)
#     return {"task": response.content}

async def chat_user_story_llm(
    state: InputState
):

    formatted_messages = (
        USER_STORY_GENERATOR_PROMPT.invoke(
            {
                "user_input": state["user_input"],

                "constitution": state["constitution"],

                "specification": state["specification"],

                # "planning": state["planning"],

                # "task": state["task"]
            }
        )
    )

    response = await llm.ainvoke(
        formatted_messages
    )

    save_markdown("user_story.md", response.content)

    return {
        "user_story": response.content
    }





async def chat_task_llm(state: InputState):
    formatted_messages = TASK_GENERATOR_PROMPT.invoke(
        {
            "constitution": state["constitution"],
            "user_input": state["user_input"],
            "user_story": state["user_story"],
        }
    )
    response = await llm.ainvoke(formatted_messages)
    save_markdown("task.md", response.content)
    return {"task": response.content}



async def chat_test_case_llm(state: InputState):
    formatted_messages = TEST_CASE_GENERATOR_PROMPT.invoke(
        {
            "constitution": state["constitution"],
            "specification": state["specification"],
            "user_story": state["user_story"],
        }
    )
    response = await llm.ainvoke(formatted_messages)
    save_markdown("test_case.md", response.content)
    return {"test_case": response.content}
