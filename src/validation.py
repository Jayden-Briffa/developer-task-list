import datetime
from TasksModel import TasksModel
from Task import Task


def isPositiveInteger(userInput: str) -> bool:
    try:
        castedInput = int(userInput)

        if castedInput < 0:
            return False

        return True

    except ValueError:
        return False


def validateExistingTaskId(userInput: str, model: TasksModel) -> str | Task:
    if not isPositiveInteger(userInput):
        return "Task id must be a positive integer"

    taskById = model.selectTasksByIds(ids=[userInput]).get(userInput)
    if not taskById:
        return f"Given task id: {userInput} does not exist"

    return taskById


def validateExistingTaskName(userInput: str, model: TasksModel) -> str | None:
    errMsg = validateTaskName(userInput)
    if errMsg:
        return errMsg

    taskByName = model.selectTasksByNames([userInput]).get(userInput)
    if not taskByName:
        return f"Given task name: {userInput} does not exist"

    return None


def validateTaskName(userInput: str) -> str | None:
    if userInput == "":
        return "Task name cannot be empty"
    elif len(userInput) < 3 or len(userInput) > 32:
        return "Task name length must be between 3 and 32 characters long (inclusive)"

    return None


def validateTaskDescription(userInput: str) -> str | None:
    if len(userInput) > 256:
        return (
            "Task description length must be less than or equal to 256 characters long"
        )

    return None


def validateTaskDeadline(userInput: str) -> str | None:
    if not datetime.datetime.strptime(userInput, "%d/%m/%Y"):
        return "Task deadline must be in the format DD/MM/YYYY"


def validateTaskCategory(userInput: str) -> str | None:
    if len(userInput) < 3 or len(userInput) > 16:
        return (
            "Task category length must be between 3 and 16 characters long (inclusive)"
        )

    return None
