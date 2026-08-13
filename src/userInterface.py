from Task import Task
from TasksModel import TasksModel
from prompt_toolkit import prompt
from typing import Callable
from UserAbortException import UserAbortException


# Remove case sensitivity
def formatAsUserInput(msg: str):
    return msg.strip().lower()


def getValidatedUserInput(
    msg: str,
    validationFunc: Callable,
    model: TasksModel = None,
    default="",
    format=False,
) -> str | Task | None:
    while True:

        userInput = getUserInput(msg, default=default, format=format)
        if model:
            validationResult = validationFunc(userInput, model=model)
        else:
            validationResult = validationFunc(userInput)

        if type(validationResult) == str:
            outputError(validationResult)
            continue

        if model:
            if validationResult is None:
                return userInput

            return validationResult
        return userInput


def getUserInput(msg: str, format=True, default=""):
    # Force a space after the prompt message if it doesn't already have one
    if len(msg) > 0 and msg[-1] != " ":
        msg += " "

    userInput = prompt(msg, default=default)
    if userInput == "abort":
        raise UserAbortException()

    if format:
        return formatAsUserInput(userInput)

    return userInput


def pressEnterToContinue():
    getUserInput("\nPress enter to continue...")


def normaliseMenuInput(userInput: str, choices: list[str]) -> str:
    for i, choice in enumerate(choices):
        castedI = str(i)
        if userInput == castedI or userInput == formatAsUserInput(choice):
            return castedI

    return ""


def getMenuInput(title, choices: list[str], defaultInput="") -> str | None:
    bannerBuffer = "=" * 5
    print(bannerBuffer, title, bannerBuffer)

    for i, choice in enumerate(choices):
        print(f"{i}. {choice}")

    userChoice = getUserInput(
        f"Enter your choice (0-{len(choices) - 1} or full phrase): ",
        format=True,
        default=defaultInput,
    )
    normalisedChoice = normaliseMenuInput(userChoice, choices)

    return normalisedChoice


def getMenuChoiceInput(title, choices: list[str], defaultChoice="") -> str:
    defaultInput = ""
    if defaultChoice != "":
        for i, choice in enumerate(choices):
            if choice.lower() == defaultChoice.lower():
                defaultInput = str(i)
                break

    while True:
        normalisedIndex = getMenuInput(title, choices, defaultInput=defaultInput)
        if normalisedIndex != "":
            return choices[int(normalisedIndex)]

        if defaultChoice != "":
            return defaultChoice

        outputError(
            f"Invalid menu input. You must enter numbers (0-{len(choices) - 1}) or the full phrase"
        )


def outputTasksByCategory(tasksByCategory: dict[str, Task]):

    print()

    if not tasksByCategory:
        print("No tasks to display.")
        pressEnterToContinue()
        return

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
    print(f"- Status: {task.status}")
    print(description)
    print(f"[ Deadline: {deadline} ]")

    if pressEnter:
        pressEnterToContinue()


def outputError(msg: str):
    bannerBuffer = "!"
    print(bannerBuffer, "ERROR:", msg, bannerBuffer)

    pressEnterToContinue()


# Input collection functions for task attributes
TASK_STATUS_OPTIONS = [
    "Not started",
    "In progress",
    "Blocked",
    "Testing",
    "Completed",
]


def getConfirmedTaskCategory(model, default: str = "") -> str:
    from validation import validateTaskCategory

    while True:
        existingCategories = list(model.selectTasksByCategories().keys())
        print("Available categories:")
        if len(existingCategories) == 0:
            buffer = "-" * 3
            print(f"\n{buffer} No existing categories. {buffer}")
        else:
            for existingCategory in existingCategories:
                categoryLabel = (
                    existingCategory if existingCategory != "" else "<no output>"
                )
                print(f"- {categoryLabel}")

        print("Or enter a new category to create it.")

        category = getValidatedUserInput(
            "Enter the task category: ",
            validateTaskCategory,
            default=default,
        )
        existingCategory = any(
            storedCategory.lower() == category.lower()
            for storedCategory in model.selectTasksByCategories().keys()
        )
        if not existingCategory:
            print()
            print(
                f"This will create a new category. Are you sure you want to use the category '{category}'?"
            )
            confirmation = getUserInput("Only 'yes' will be accepted: ", format=False)
            if confirmation.lower() == "yes":
                break

        else:
            break

    return category


def getTaskStatusChoice(default: str = "Not started") -> str:
    return getMenuChoiceInput(
        "Select task status",
        TASK_STATUS_OPTIONS,
        defaultChoice=default,
    )
