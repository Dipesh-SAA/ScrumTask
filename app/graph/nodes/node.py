from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import json
import re
from app.Infrastrature.llm.loader import llm
from app.Prompts.get_prompt_template_constitution import CONSTITUTION_GENERATOR_PROMPT
from app.Prompts.get_improve_user_story import IMPROVE_USER_STORY_PROMPT
from app.Prompts.get_prompt_template_specification import SPECIFICATION_GENERATOR_PROMPT
from app.Prompts.get_prompt_template_task import TASK_GENERATOR_PROMPT
from app.Schema.State import InputState
from app.Infrastrature.embeddings.embedding_model import (generate_embedding, get_constitution_chunks, rank_chunks)
from app.Prompts.get_prompt_template_user_story import (
    USER_STORY_GENERATOR_PROMPT
)

BASE_DIR = Path(__file__).resolve().parents[3]
# CONSTITUTION_PATH = BASE_DIR / "AI  Agent Global Consitution (1).docx"
OUTPUT_DIR = BASE_DIR / "generated_md"


def save_markdown(filename: str, content: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.joinpath(filename).write_text(content.strip(), encoding="utf-8")


def parse_llm_json_response(text: str):
    text = str(text).strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:
        return json.loads(text[start:end + 1])

    raise ValueError("LLM response was not valid JSON")


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
    # Create embedding for user query
    user_vector = generate_embedding(state["user_input"])

    # Fetch chunks from Qdrant API
    chunks = get_constitution_chunks()

    # Retrieve top relevant chunks
    top_chunks = rank_chunks(
        user_vector=user_vector,
        chunks=chunks,
        top_k=5,
    )

    # Build context for prompt
    retrieved_context = "\n\n".join(
        [
            f"Heading: {chunk['heading']}\n\n{chunk['text']}"
            for chunk in top_chunks
        ]
    )

    # Debug (optional)
    # print("\nRetrieved Chunks:")
    for chunk in top_chunks:
        print(
            f"Score={chunk['score']:.4f} | Heading={chunk['heading']}"
        )

    formatted_messages = CONSTITUTION_GENERATOR_PROMPT.invoke(
        {
            "user_input": state["user_input"],
            "retrieved_context": retrieved_context,
        }
    )

    response = await llm.ainvoke(formatted_messages)

    save_markdown("constitution.md", response.content)

    return {
        "constitution": response.content
    }

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


#test case generation is the final step, it will take the constitution, user story and task to generate test cases. It will follow strict traceability rules to ensure that every test case is directly traceable to a User Story or Acceptance Criterion. It will not invent any values unless explicitly stated in the User Story. The generated test cases will be saved in a markdown file for further use.


async def improve_user_story_llm(user_story: str, instruction: str):
    formatted_messages = IMPROVE_USER_STORY_PROMPT.invoke(
        {
            "user_story": user_story,
            "instruction": instruction,
        }
    )

    response = await llm.ainvoke(formatted_messages)

    save_markdown("improve_user_story.md", response.content)

    return {
        "improve_user_story": parse_llm_json_response(response.content)
    }




# import asyncio

# async def test():
#     state = {
#         "user_input": "What are the core modules required for building an AI-native enterprise platform?"
#     }

#     result = await chat_constitution_llm(state)

#     print("\nRESULT:")
#     print(result["constitution"][:1000])

# asyncio.run(test())
