from typing import TypedDict, Annotated, Sequence
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class InputState(TypedDict):
    user_input: str

    messages: Annotated[
        Sequence[BaseMessage],
        add_messages
    ]

    retrieved_context: str

    constitution: str

    specification: str

    # planning: str

    task: str

    user_story: str
