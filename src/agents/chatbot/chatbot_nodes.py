import os

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from src.agents.chatbot.chatbot_state import State
from src.agents.chatbot.chatbot_tools import tools

llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

def chatbot_node(state: State):

    additional_context = f"\n\n\n Additional context:\n User Id: {state["user_id"]}"

    return State(
        messages=[
            llm.invoke(
                [
                    SystemMessage(
                        content=os.getenv("CHATBOT_AGENT_SYSTEM_PROMPT") + additional_context
                    )
                ] + state["messages"]
            )
        ],
        user_id=state["user_id"]
    )