from typing import Annotated

from langgraph.graph import MessagesState

class State(MessagesState):
    user_id: Annotated[str, "The id of the user"]
    pass