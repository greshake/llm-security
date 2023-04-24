from abc import ABC

from rich.prompt import Prompt
from rich.console import Console

from scenarios.common.chat_app import ChatMLApp


class Scenario:
    name = "Scenario"
    description = "A scenario is a test."
    target = "None"

    def __init__(self, console=None, interactive=False, verbose=False):
        self.interactive = interactive
        self.verbose = verbose
        self.console = console or Console()

    def prompt_user(self, prompt: str, default: str) -> str:
        if self.interactive:
            return Prompt.ask(prompt, default=default)
        else:
            return default

    def print(self, message, role=None) -> None:
        colors = {
            "user": "green",
            "system": "blue",
            "assistant": "red",
            "app": "red",
        }
        color = colors.get((role or "").lower(), "white")
        if role:
            self.console.print(f"[bold {color}]{role}[/bold {color}]: {message}")
        else:
            self.console.print(message)

    def log(self, message) -> None:
        if self.verbose:
            self.console.log(message)

    def run(self) -> bool:
        # Print summary, call _run(), and print result.
        self.console.print(f"[bold blue]Scenario: {self.name}[/bold blue]")
        self.console.print(f"[bold blue]Description: {self.description}[/bold blue]")
        self.console.print(f"[bold blue]Target: {self.target}[/bold blue]")
        self.console.print(f"[bold blue]Interactive: {self.interactive}[/bold blue]")

        failed = False
        try:
            self._run()
        except AssertionError as e:
            self.console.print(f"[bold red]Error: {e}[/bold red]")
            failed = True

        if not failed:
            self.console.print(f"[bold green]Scenario {self.name} PASS[/bold green]")
        else:
            self.console.print(f"[bold red]Scenario {self.name} FAIL[/bold red]")

        while self.interactive:
            self.prompt_user("User Input: ", default="")

        return not failed

    def _run(self) -> bool:
        raise NotImplementedError("Scenario._run() not implemented.")


class ChatMLAppScenario(Scenario, ABC):
    model = "gpt-3.5-turbo"

    def __init__(self, tools=None, **kwargs):
        super().__init__(**kwargs)
        self.app = ChatMLApp(self, model=self.model, tools=tools)

    def prompt_user(self, prompt: str, default: str) -> str:
        if self.interactive:
            return self.app.ask(Prompt.ask(prompt, default=default))
        else:
            return self.app.ask(default)
