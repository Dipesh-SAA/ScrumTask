# from app.Schema.State import InputState
# from langgraph.graph import StateGraph, START, END 
# from langgraph.checkpoint.memory import MemorySaver
# from app.graph.nodes.node import (
#     chat_constitution_llm,
#     chat_specification_llm,
#     chat_planning_llm,
#     chat_task_llm
# )

# def create_graph():

#     graph = StateGraph(InputState)

#     # Add Nodes
#     graph.add_node("constitution", chat_constitution_llm)
#     graph.add_node("specification", chat_specification_llm)
#     graph.add_node("planning", chat_planning_llm)
#     graph.add_node("task", chat_task_llm)

#     # Start Edge
#     graph.add_edge(START, "constitution")

#     # Flow Edges
#     graph.add_edge("constitution", "specification")
#     graph.add_edge("specification", "planning")
#     graph.add_edge("planning", "task")
#     graph.add_edge("task", END)
#     memory = MemorySaver() # Define memory
#     return graph.compile(checkpointer=memory)
   


from app.Schema.State import InputState

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.graph.nodes.node import (
    chat_constitution_llm,
    chat_specification_llm,
    # chat_planning_llm,
    chat_task_llm,
    chat_user_story_llm,
    chat_test_case_llm
)


def create_graph():

    graph = StateGraph(InputState)

    # Add nodes
    graph.add_node(
        "constitution",
        chat_constitution_llm
    )

    graph.add_node(
        "specification",
        chat_specification_llm
    )

    # graph.add_node(
    #     "planning",
    #     chat_planning_llm
    # )

    graph.add_node(
        "task",
        chat_task_llm
    )

    graph.add_node(
        "user_story",
        chat_user_story_llm
    )
    graph.add_node(
        "test_case",
        chat_test_case_llm
    )

    # Flow
    graph.add_edge(START, "constitution")

    graph.add_edge("constitution", "specification")

    graph.add_edge("specification", "user_story")

    # graph.add_edge("planning", "task")

    graph.add_edge("user_story", "task")

    graph.add_edge("task", "test_case")
    graph.add_edge("test_case", END)

    memory = MemorySaver()

    return graph.compile(
        checkpointer=memory
    )
