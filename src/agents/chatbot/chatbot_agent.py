import aiosqlite
from langchain_core.messages import AIMessageChunk, HumanMessage, AIMessage
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.constants import START, END
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from src.agents.chatbot.chatbot_nodes import chatbot_node, rename_session_node
from src.agents.chatbot.chatbot_state import State
from src.agents.chatbot.chatbot_tools import tools

def rename_session_condition(state: State):
    if state["session_name"] == "New session" and len([message for message in state["messages"] if isinstance(message, HumanMessage) or isinstance(message, AIMessage)]) > 4:
        return "rename_session"
    return END

async def chatbot_graph():
    memory = AsyncSqliteSaver(conn=(await aiosqlite.connect("db/db.sqlite3")))
    return (
        StateGraph(State)
        .add_node("chatbot", chatbot_node)
        .add_node("rename_session", rename_session_node)
        .add_node("tools", ToolNode(tools=tools))
        .add_edge(START, "chatbot")
        .add_conditional_edges("chatbot", tools_condition)
        .add_conditional_edges("chatbot", rename_session_condition)
        .add_edge("tools", "chatbot")
        .compile(checkpointer=memory)
    )