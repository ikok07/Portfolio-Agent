from typing import Annotated

from langgraph.graph import MessagesState

class State(MessagesState):
    user_id: Annotated[str, "The id of the user"]
    session_id: Annotated[str, "The id of the current session"]
    session_name: Annotated[bool, "The name of the session"]
    pass