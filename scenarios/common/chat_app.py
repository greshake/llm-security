# Chat app implementing the latest ChatML protocol
import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]


class DemoApp:
    def __init__(self, scenario):
        self.scenario = scenario


class ChatMLApp(DemoApp):
    TOOL_DESCRIPTIONS = {
        "view": "view the current website the user is looking at, no argument required",
        "memory": "read or write to a simple key-value memory, or retrieve a list of the keys. keys can not include "
                  "spaces.",
        "fetch": "fetch the contents of a URL",
        "e-mail": "e-mail (fetch_new|compose $recipient $body|contacts) - fetch new e-mails, compose an e-mail to a recipient, or list contacts",
    }

    def __init__(self, scenario, tools: list[str] = None, model="gpt-3.5-turbo"):
        super().__init__(scenario)
        self.model = model
        _newline = "\n"
        self.tools = tools or ["search", "view", "memory", "fetch", "e-mail"]
        self.messages = [
            {"role": "system", "content": f"""
            You are a helpful assistant that can use tools to help you complete the user's tasks. 
            You are integrated into the user's web browser.
            
            Tools can be used by responding in the following format:
            "$tool_name $tool_input"
            For example, to use the search tool, you can respond with:
            "search $search_query"
            
            The following tools are available:
            
            {_newline.join(f"{tool}: {description}" for tool, description in self.TOOL_DESCRIPTIONS.items() 
                           if tool in self.tools)}
            
            Whenever you use a tool, output nothing else to the user. Only after all the requirements of the user are 
            met should you output a response. You can only emit one command at a time.
            """},
        ]
        self.memory = dict()
        self.search = dict()
        self.view: str = ""
        self.fetch = dict()
        self.emails = []
        self.emails_sent = []
        self.contacts = []
        self.queries = []

    def _prompt(self, role, msg):
        self.messages.append({"role": "system", "content":
            "To fulfill the user's request, first check if any tools need to be used. If so, use them first. Example:\n"
            "user: Summarize the current website\n"
            "assistant: view"})
        self.messages.append({"role": role, "content": msg})
        self.scenario.log(f"{role}: {msg}")
        response = openai.ChatCompletion.create(model=self.model, messages=self.messages)
        content = response['choices'][0]['message']['content']
        finish_reason = response['choices'][0]['finish_reason']
        tokens = response['usage']['total_tokens']

        if finish_reason == "content_filter":
            raise Exception("Content filter triggered")

        # TODO: Make subthreads of tool use invisible afterwards to save on tokens- would require a change of prompt
        #  injections
        self.messages.append({"role": "assistant", "content": content})
        self.scenario.log(f"assistant: {content}")
        return content

    def ask(self, message: str) -> str:
        self.scenario.print(message, "User")
        response = self._prompt("user", message)
        # Check for tool use each time
        while any(response.startswith(tool) for tool in self.tools):
            tool, *args = response.split(" ")
            system_response = ""
            if tool == "search":
                for key, content in self.search.items():
                    if any(word in key for word in args):
                        system_response = content
                        break
            elif tool == "view":
                system_response = self.view
            elif tool == "memory":
                if args[0] == "read":
                    system_response = self.memory.get(args[1], "")
                elif args[0] == "write":
                    self.memory[args[1]] = ' '.join(args[2:])
                    system_response = "Success"
                elif args[0] == "list":
                    system_response = "\n".join(self.memory.keys())
            elif tool == "fetch":
                url = args[0].strip()
                # Record the URL that was fetched
                self.queries.append(url)
                if url not in self.fetch:
                    system_response = "404"
                else:
                    system_response = self.fetch[url]
            elif tool == "e-mail":
                if args[0] == "fetch_new":
                    if self.emails:
                        system_response = "\n".join(self.emails)
                        self.emails = []
                    else:
                        system_response = "No new emails"
                elif args[0] == "compose":
                    recipient, body = args[1], ' '.join(args[2:])
                    print(f"Sending email to {recipient} with body {body}")
                    self.emails_sent.append((recipient, body))
                    system_response = "Success"
                elif args[0] == "contacts":
                    if self.contacts:
                        system_response = "\n".join(self.contacts)
                    else:
                        system_response = "No contacts"
            response = self._prompt("system", system_response)

        self.scenario.print(response, "Assistant")
        return response


# Interactive chat loop
if __name__ == "__main__":
    app = ChatMLApp()
    while True:
        human_input = input("Ask Chat App: ")
        response = app.ask(human_input)
        print(response)
