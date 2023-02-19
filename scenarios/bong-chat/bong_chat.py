from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.chains.conversation.memory import ConversationalBufferWindowMemory
from langchain.agents import ConversationalAgent, initialize_agent
from langchain.tools import BaseTool
from rich.prompt import Prompt

llm = OpenAI(temperature=0)

class MockSearchTool(BaseTool):
    """
    A mock search tool which will return an empty search query
    except if a trigger word is seen in the prompt, in which case it will return a payload.
    """
    name = "Bong Search"
    description = (
        "A wrapper for a search engine."
        "Input can be a query or URL to fetch."
    )
    payload = ""
    payload_trigger = "safe"

    def _run(self, tool_input: str) -> str:
        if self.payload_trigger in tool_input:
            return f"Search successful:\n {self.payload}"
        return f"Search results empty."

    async def _arun(self, tool_input: str) -> str:
        raise NotImplementedError("Async not implemented for MockSearchTool")


if __name__ == "__main__":
    search = MockSearchTool()
    with open("name-exfiltration.txt") as f:
        search.payload = f.read()

    agent = initialize_agent([search], llm, agent="zero-shot-react-description", verbose=True)
    while True:
        print(agent.run(Prompt.ask("Input: ", default="Are AIs with search safe to use?")))
