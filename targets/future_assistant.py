from langchain import OpenAI
from langchain.chains.conversation.memory import ConversationKGMemory, ConversationBufferMemory
from langchain.agents import initialize_agent
from langchain.python import PythonREPL

from targets.common.tools import *


class FutureAssistant:
    """
    In addition to Bong Chat's features, the assistant can also:
    - Execute Python in a REPL
    - Store data as memories between sessions if required
    - All optional tools for Bong Chat (search, current website, retrieve URL) are always available,
      but can be included with payloads.
    """

    def __init__(self,
                 note_memory: NoteMemory = None,
                 search_engine: PoisonedSearchTool = None,
                 current_website: PoisonedCurrentWebsiteTool = None,
                 retrieve_url: PoisonedRetrieveURLTool = None,
                 max_iterations: int = 3,
                 verbose=False):
        tools = []
        if note_memory:
            tools.append(note_memory)
        else:
            tools.append(NoteMemory())
        if search_engine:
            tools.append(search_engine)
        else:
            tools.append(PoisonedSearchTool())
        if current_website:
            tools.append(current_website)
        else:
            tools.append(PoisonedCurrentWebsiteTool())
        if retrieve_url:
            tools.append(retrieve_url)
        else:
            tools.append(PoisonedRetrieveURLTool())
        self.llm = OpenAI(temperature=0)
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.agent = initialize_agent(tools=tools,
                                      llm=self.llm,
                                      memory=self.memory,
                                      agent="conversational-react-description",
                                      verbose=verbose,
                                      max_iterations=max_iterations)

    def send(self, message: str) -> str:
        return self.agent(message)['output']
