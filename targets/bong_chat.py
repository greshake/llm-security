from langchain import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
from rich.prompt import Prompt

from targets.common.tools import *


class BongChatApp:
    def __init__(self,
                 search_engine: PoisonedSearchTool = None,
                 current_website: PoisonedCurrentWebsiteTool = None,
                 retrieve_url: PoisonedRetrieveURLTool = None,
                 max_iterations: int = 3,
                 verbose=False):
        tools = []
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


if __name__ == "__main__":
    app = BongChatApp()
    while True:
        human_input = Prompt.ask("Ask Bong Chat: ")
        response = app.send(human_input)
        print(response)
