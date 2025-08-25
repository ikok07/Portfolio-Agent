from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from src.agents.chatbot.chatbot_nodes import chatbot_node
from src.agents.chatbot.chatbot_state import State
from src.agents.chatbot.chatbot_tools import tools

memory = MemorySaver()

graph = (
    StateGraph(State)
    .add_node("chatbot", chatbot_node)
    .add_node("tools", ToolNode(tools=tools))
    .add_edge(START, "chatbot")
    .add_conditional_edges("chatbot", tools_condition)
    .add_edge("tools", "chatbot")
    .compile(checkpointer=memory)
)