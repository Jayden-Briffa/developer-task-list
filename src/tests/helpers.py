from Task import Task


def assertTaskHasSameValues(actualTask: Task, expectedTask: dict | Task):
    if type(expectedTask) == dict:
        expectedTask = Task(**expectedTask)

    assert actualTask is not None, (
        f"Expected a task object, but actual was None.\n"
        f"expected={expectedTask!r}\n"
        f"actual={actualTask!r}"
    )
    assert vars(actualTask) == vars(expectedTask), (
        f"Task mismatch:\n"
        f"expected={vars(expectedTask)!r}\n"
        f"actual={vars(actualTask)!r}"
    )


def mockGetUserInputFactory(answers):
    # Make the mock getUserInput compatible with original function parameters, but it doesn't need to use them
    def mockGetUserInput(prompt="", default="", format=True):
        return next(answers)

    return mockGetUserInput


def mockOutputTask(task: Task, pressEnter=True):
    return task


def mockOutputTasksByCategory(tasksByCategory: dict[str, Task]):
    return tasksByCategory


def mockOutputError(msg: str):
    print(f"ERROR: {msg}")


# Construct an expected task and a list of dummy inputs based on an inputted dict[str, list | str]
# Values in expectedTaskInputs which are strings instead of lists are added to expectedNewTask, but not userInputs
# Where confirmation is required for an action (ie, the answer is "yes"), the second to-last value in the list is added to expectedNewTask
def constructExpectedTaskAndUserInputs(expectedTaskInputs: dict[str, list[str] | str]):
    expectedTask = {}
    userInputs = []
    for key, val in expectedTaskInputs.items():
        if type(key) == str:
            expectedTask[key] = val

        if val[-1] == "yes":
            expectedTask[key] = val[-2]
        else:
            expectedTask[key] = val[-1]

        for newInput in val:
            userInputs.append(newInput)

    return expectedTask, userInputs
