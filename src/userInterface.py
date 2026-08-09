from Task import Task


# Remove case sensitivity
def formatAsUserInput(msg: str):
    return msg.strip().lower()


def validateMenuInput(userInput: str, choices: list):
    for i, choice in enumerate(choices):
        if userInput == str(i):
            return True

        if userInput == formatAsUserInput(choice):
            return True

    return False


def getUserInput(msg: str):
    return formatAsUserInput(input(msg))


def getMenuInput(title, choices: list[str]) -> str | None:
    bannerBuffer = "=" * 5
    print(bannerBuffer, title, bannerBuffer)

    for i, choice in enumerate(choices):
        print(f"{i}. {choice}")

    userChoice = getUserInput(f"Enter your choice (1-{len(choices)} or full phrase):")
    validatedChoice = validateMenuInput(userChoice, choices)

    if validatedChoice == "":
        return None

    return validatedChoice


def validateMenuInput(userInput: str, choices: list[str]) -> str:
    for i, choice in enumerate(choices):
        if userInput == i or userInput == formatAsUserInput(choice):
            return i

    return ""


def outputTasksByCategory(tasksByCategory: dict[str, Task]):
    bannerBuffer = "-" * 3
    lBuffer = ". "

    for category, tasks in tasksByCategory.items():
        print(bannerBuffer, category, bannerBuffer)

        for task in tasks:
            print(lBuffer, f"{task.name} (#{task.id}) @ {task.deadline}")


def outputTask(task: Task):
    bannerBuffer = "-" * 3

    print(bannerBuffer, task.name, f"(#{task.id})", bannerBuffer)
    print(task.description)
    print(f"[ Deadline: {task.deadline} ]")


def outputError(msg: str):
    bannerBuffer = "!"
    print(bannerBuffer, "ERROR:", msg, bannerBuffer)
