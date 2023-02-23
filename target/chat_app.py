from langchain import OpenAI
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


class Email:
    default_tools = [
        ReadEmailTool,
        SendEmailTool,
        ReadContactsTool,
        ComposeTool
    ]

    def __init__(self, tools=None,
                 max_iterations: int = 5,
                 temperature: float = 0.0,
                 model="text-davinci-003",
                 verbose=False):
        tools = tools or []
        for tool in self.default_tools:
            if not any(isinstance(t, tool) for t in tools):
                tools.append(tool())
        self.llm = OpenAI(temperature=temperature)
        self.agent = initialize_agent(tools=tools,
                                      llm=self.llm,
                                      agent="zero-shot-react-description",
                                      verbose=verbose,
                                      max_iterations=max_iterations)

    def run(self, message: str) -> str:
        return self.agent.run(message)


if __name__ == "__main__":
    app = ChatApp(verbose=True)
    while True:
        human_input = Prompt.ask("Ask Chat App: ")
        response = app.send(human_input)
        print(response)
