from Task import Task
from TasksModel import TasksModel
from prompt_toolkit import prompt
from typing import Callable


# Remove case sensitivity
def formatAsUserInput(msg: str):
    return msg.strip().lower()


def getValidatedUserInput(
    msg: str, validationFunc: Callable, model: TasksModel = None, default=""
) -> str | Task | None:
    while True:

        userInput = getUserInput(msg, default=default)
        if model:
            validationResult = validationFunc(userInput, model=model)
        else:
            validationResult = validationFunc(userInput)

        if type(validationResult) == str:
            outputError(validationResult)
            continue

        if model:
            return validationResult
        return userInput


def getUserInput(msg: str, format=True, default=""):
    userInput = prompt(msg, default=default)
    if format:
        return formatAsUserInput(userInput)

    return userInput


def pressEnterToContinue():
    getUserInput("\nPress enter to continue...")


# TODO: Frame as normalisation rather than validation
def validateMenuInput(userInput: str, choices: list[str]) -> str:
    for i, choice in enumerate(choices):
        castedI = str(i)
        if userInput == castedI or userInput == formatAsUserInput(choice):
            return castedI

    return ""


def getMenuInput(title, choices: list[str]) -> str | None:
    bannerBuffer = "=" * 5
    print(bannerBuffer, title, bannerBuffer)

    for i, choice in enumerate(choices):
        print(f"{i}. {choice}")

    userChoice = getUserInput(
        f"Enter your choice (0-{len(choices) - 1} or full phrase): "
    )
    validatedChoice = validateMenuInput(userChoice, choices)

    return validatedChoice


def outputTasksByCategory(tasksByCategory: dict[str, Task]):

    print()

    bannerBuffer = "-" * 3
    lBuffer = ". "

    for category, tasks in tasksByCategory.items():
        categoryLabel = category if category != "" else "<no output>"
        print(bannerBuffer, categoryLabel, bannerBuffer)

        for task in tasks:
            print(lBuffer, f"{task.name} (#{task.id}) @ {task.deadline}")

    pressEnterToContinue()


def outputTask(task: Task, pressEnter=True):

    print()

    bannerBuffer = "-" * 3
    category = task.category if task.category != "" else "<no output>"
    description = task.description if task.description != "" else "<no description>"
    deadline = task.deadline if task.deadline != "" else "<no deadline>"

    print(bannerBuffer, task.name, f"(#{task.id})", bannerBuffer)
    print(f"- Category: {category}")
    print(description)
    print(f"[ Deadline: {deadline} ]")

    if pressEnter:
        pressEnterToContinue()


def outputError(msg: str):
    bannerBuffer = "!"
    print(bannerBuffer, "ERROR:", msg, bannerBuffer)

    pressEnterToContinue()
