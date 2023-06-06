import os
import sys
import importlib
import inspect
from pathlib import Path

from scenarios.common.scenario import ChatMLAppScenario


def find_subclasses(base_class, folder_path):
    subclasses = []
    sys.path.insert(0, folder_path)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                module_path = Path(root) / file
                relative_module_path = module_path.relative_to(folder_path).with_suffix("")
                module_name = str(relative_module_path).replace("/", ".").replace("\\", ".")

                if any(name in module_name for name in ["__init__", "common", "code-completion", "gpt3langchain", "puzzle"]):
                    continue

                try:
                    module = importlib.import_module(module_name)
                except ImportError as e:
                    print(f"Error importing module {module_name}: {e}")
                    continue

                for _, cls in inspect.getmembers(module, inspect.isclass):
                    if issubclass(cls, base_class) and cls != base_class:
                        subclasses.append(cls)

    sys.path.pop(0)
    return subclasses


def menu():
    scenarios = find_subclasses(ChatMLAppScenario, os.path.dirname(__file__))

    while True:
        print("Which scenario would you like to run?")
        print("0. Run all scenarios")
        for i, scenario in enumerate(scenarios):
            print(f"{i + 1}. {scenario.name}")
        print("q. Quit")
        choice = input("> ")
        if choice == "q":
            break
        elif choice == "0":
            results = []
            for scenario in scenarios:
                results.append(scenario(interactive=False).run())
            for scenario, result in zip(scenarios, results):
                print(f"{scenario.name} {'PASS' if result else 'FAIL'}")
        else:
            try:
                scenario = scenarios[int(choice) - 1]
            except IndexError:
                print("Invalid choice")
            else:
                scenario(interactive=True, verbose=True).run()


if __name__ == "__main__":
    menu()
