from langchain.utilities import RequestsWrapper, BashProcess
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)

# load the tools


tools = load_tools(["requests", "terminal"], llm=llm)

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

if __name__ == "__main__":
    while True:
        question = input("Ask a question: ")
        response = agent(question)
        print(response)
