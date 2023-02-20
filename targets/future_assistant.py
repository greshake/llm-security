from langchain import OpenAI
from langchain.chains.conversation.memory import ConversationKGMemory, ConversationBufferMemory
from langchain.agents import initialize_agent
from langchain.python import PythonREPL

from targets.bong_chat import BongChatApp
from targets.common.tools import *


class FutureAssistant(BongChatApp):
    """
    In addition to Bong Chat's features, the assistant can also store notes in its memory.
    """
    default_tools = [
        PoisonedSearchTool,
        PoisonedCurrentWebsiteTool,
        PoisonedRetrieveURLTool,
        NoteMemory
    ]