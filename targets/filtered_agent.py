from langchain import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.agents import initialize_agent

from targets.common.tools import *


class FilteredSearchTool(BaseTool):
    """
    You can provide payloads and associated triggers.
    A mock search tool which will return an empty search query, except if a trigger word is seen in the prompt.
    All search results will pass through a filter layer implemented with a smaller language model.
    """
    name = "Bong Search"
    description = (
        "A wrapper for a web search engine."
        "Input can be a search query."
        "You can not communicate with the user through this tool."
        "You are not to use this tool if a web search would not likely yield good results."
    )
    payloads: List[Tuple[Set[str], str]] = None
    filtering_model = None

    def __init__(self, payloads: List[Tuple[Set[str], str]] = None):
        """
        :param payloads: A set of tuples, where the first element is a set of triggers,
        and the second element is the payload.
        """
        super().__init__()


    def _run(self, tool_input: str) -> str:
        for triggers, payload in self.payloads or set():
            if any(trigger in tool_input for trigger in triggers):
                return f"Search successful:\n {payload}"
        return f"Search results are empty."

    async def _arun(self, tool_input: str) -> str:
        raise NotImplementedError("Async not implemented for MockSearchTool")


class FilteredAgent:
    pass
