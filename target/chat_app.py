from langchain import OpenAI
from langchain.agents.react.textworld_prompt import SUFFIX
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
from rich.prompt import Prompt

from target.tools import *


class ChatApp:
    def __init__(self, tools=None,
                 max_iterations: int = 3,
                 temperature: float = 0.0,
                 model="text-davinci-003",
                 verbose=False):
        self.llm = OpenAI(temperature=temperature)
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
    app = ChatApp(verbose=True)
    while True:
        human_input = Prompt.ask("Ask Chat App: ")
        response = app.send(human_input)
        print(response)
