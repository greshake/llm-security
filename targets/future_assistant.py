from langchain import OpenAI
from langchain.chains.conversation.memory import ConversationKGMemory, ConversationBufferMemory
from langchain.agents import initialize_agent
from langchain.python import PythonREPL

from targets.chat_app import ChatApp
from targets.common.tools import *


class FutureAssistant(ChatApp):
    """
    In addition to Chat App's features, the assistant can also store notes in its memory.
    """
    default_tools = [
        SearchTool,
        CurrentWebsiteTool,
        RetrieveURLTool,
        NoteMemory
    ]