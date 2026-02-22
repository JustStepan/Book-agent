from langgraph.graph import END, StateGraph
from langchain_core.messages import HumanMessage

from nodes import llm_node, should_continue, tool_node
from schema import BookAgentState


def create_book_agent_graph():
    workflow = StateGraph(BookAgentState)

    workflow.add_node("llm", llm_node)
    workflow.add_node("tool", tool_node)

    workflow.set_entry_point("llm")
    workflow.add_edge("tool", "llm")

    workflow.add_conditional_edges(
        source="llm",
        path=should_continue,
        path_map={"tool": "tool", "end": END},
    )

    return workflow.compile()


graph = create_book_agent_graph()

