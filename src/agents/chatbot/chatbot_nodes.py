import os

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.types import Command
from tortoise.exceptions import DoesNotExist

from src.agents.chatbot.chatbot_state import State
from src.agents.chatbot.chatbot_tools import tools
from src.api.models.db import ChatbotSession

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

async def chatbot_node(state: State):
    additional_context = f"\n\n\n Additional context:\n User Id: {state["user_id"]}"

    return Command(
        update={"messages": await llm_with_tools.ainvoke(
            [
                SystemMessage(
                    content=os.getenv("CHATBOT_AGENT_SYSTEM_PROMPT") + additional_context
                )
            ] + state["messages"]
        )}
    )

async def rename_session_node(state: State):
    system_message = "Your main task is to analyze the current conversation and get back with a session title. It shouldn't be longer than 20-30 words and it should summarize the most important information discussed. The tone should be neutral. Respond only with the generated title. No explanation or further texts are required."

    response = (await llm.ainvoke(
        [
            SystemMessage(content=system_message),
        ] + state["messages"]
    )).content.replace('"', '')

    await ChatbotSession.filter(id=state["session_id"]).update(name=response)

    return Command(
        update={"session_name": response}
    )