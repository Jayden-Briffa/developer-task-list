import userInterface
import controllers
import helpers

"""
This file tests controllers functions, their validations, and their interactions with the model.
Out of scope for this file:
- Fine-grained model tests, e.g., whether taskIdsByCategory is updated correctly when a task is inserted. These are tested in test_tasksModel.py
- User interface tests, e.g., whether the correct prompts are printed to the screen. These are tested manually
"""


# Views
def testViewAllTasksByCategory(monkeypatch, dummyModel):
    monkeypatch.setattr(
        userInterface, "outputTasksByCategory", helpers.mockOutputTask
    )  # Return task given to outputTask instead of printing to screen
    actualOutputTasksByCategory = controllers.viewAllTasksByCategory(dummyModel)

    for category, ids in dummyModel._taskIdsByCategory.items():
        assert category in actualOutputTasksByCategory, (
            f"Expected category {category!r} to be present in the output.\n"
            f"expected={category!r}\n"
            f"actual={list(actualOutputTasksByCategory.keys())!r}"
        )

        # Fail if the expected task id cannot be found in the category
        for expectedTaskId in ids:
            assert any(
                task.id == expectedTaskId
                for task in actualOutputTasksByCategory[category]
            ), (
                f"Expected task id {expectedTaskId!r} to be present in category {category!r}.\n"
                f"expected={expectedTaskId!r}\n"
                f"actual={[task.id for task in actualOutputTasksByCategory[category]]!r}"
            )


def testViewTaskById(monkeypatch, dummyModel):
    userInputs = ["1"]
    monkeypatch.setattr(
        userInterface, "getUserInput", helpers.mockGetUserInputFactory(iter(userInputs))
    )
    monkeypatch.setattr(
        userInterface, "outputTask", helpers.mockOutputTask
    )  # Return task given to outputTask instead of printing to screen

    expectedTaskToOutput = dummyModel._tasksById[userInputs[0]]

    result = controllers.viewTaskById(dummyModel)

    helpers.assertTaskHasSameValues(result, expectedTaskToOutput.__dict__)


def testViewTaskByName(monkeypatch, dummyModel):
    userInputs = ["TaSk1"]
    monkeypatch.setattr(
        userInterface, "getUserInput", helpers.mockGetUserInputFactory(iter(userInputs))
    )
    monkeypatch.setattr(userInterface, "outputTask", helpers.mockOutputTask)

    expectedTaskToOutput = next(
        iter(dummyModel.selectTasksByNames([userInputs[0]]).values())
    )

    result = controllers.viewTaskByName(dummyModel)

    helpers.assertTaskHasSameValues(result, expectedTaskToOutput.__dict__)


# createTask
def executeCreateTaskTestCase(
    monkeypatch, dummyModel, expectedTask: dict[str, str], userInputs: list[str]
):
    monkeypatch.setattr(userInterface, "outputTask", helpers.mockOutputTask)
    monkeypatch.setattr(
        userInterface, "getUserInput", helpers.mockGetUserInputFactory(iter(userInputs))
    )

    outputtedNewTask = controllers.createTask(dummyModel)
    helpers.assertTaskHasSameValues(outputtedNewTask, expectedTask)

    actualNewTask = dummyModel._tasksById[expectedTask["id"]]
    helpers.assertTaskHasSameValues(actualNewTask, expectedTask)


def testCreateTaskNormal(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "4",
        "name": ["Task4"],
        "description": ["Description4"],
        "deadline": ["01/01/2026"],
        "category": ["Category1"],
        "status": ["3"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeCreateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testCreateTaskExtremeLower(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "4",
        "name": ["AaA"],
        "description": [""],
        "deadline": [""],
        "category": ["AaA", "yes"],
        "status": ["0"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeCreateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testCreateTaskExtremeUpper(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "4",
        "name": ["A" * 32],
        "description": ["A" * 255],
        "deadline": ["01/01/2026"],
        "category": ["Category1"],
        "status": ["Completed"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeCreateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testCreateTaskMinimumFields(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "4",
        "name": ["TaskNameAa"],
        "description": [""],
        "deadline": [""],
        "category": ["", "yes"],
        "status": ["2"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeCreateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testCreateTaskExtremeLowerInvalid(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "4",
        "name": ["Aa", "AaAaA"],
        "description": [""],
        "deadline": [""],
        "category": ["Aa", "AaAaA", "yes"],
        "status": ["4"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeCreateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testCreateTaskExtremeUpperInvalid(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "4",
        "name": ["A" * 33, "A" * 32],
        "description": ["A" * 256, "A" * 255],
        "deadline": ["01/01/2026"],
        "category": ["Aa", "AaAaA", "yes"],
        "status": ["1"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeCreateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testCreateTaskDuplicateName(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "4",
        "name": ["Task1", "Task4"],
        "description": ["Description4"],
        "deadline": ["01/01/2026"],
        "category": ["Category1"],
        "status": ["3"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeCreateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testCreateTaskDontConfirmCategory(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "4",
        "name": ["AaAaA"],
        "description": [""],
        "deadline": [""],
        "category": ["AaAaA", "no", "AaAaAa", "yes"],
        "status": ["In progress"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeCreateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


# updateTask
def executeUpdateTaskTestCase(
    monkeypatch, dummyModel, expectedTask: dict[str, str], userInputs: list[str]
):
    monkeypatch.setattr(userInterface, "outputTask", helpers.mockOutputTask)
    monkeypatch.setattr(
        userInterface, "getUserInput", helpers.mockGetUserInputFactory(iter(userInputs))
    )

    outputtedNewTask = controllers.updateTask(dummyModel)
    helpers.assertTaskHasSameValues(outputtedNewTask, expectedTask)

    actualNewTask = dummyModel._tasksById[expectedTask["id"]]
    helpers.assertTaskHasSameValues(actualNewTask, expectedTask)


def testUpdateTaskNormal(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": ["3"],
        "name": ["Task3"],
        "description": ["Description3"],
        "deadline": ["01/01/2026"],
        "category": ["Category1"],
        "status": ["3"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeUpdateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testUpdateTaskExtremeLower(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": ["3"],
        "name": ["AaA"],
        "description": [""],
        "deadline": [""],
        "category": ["AaA", "yes"],
        "status": ["0"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeUpdateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testUpdateTaskExtremeUpper(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": ["3"],
        "name": ["A" * 32],
        "description": ["A" * 255],
        "deadline": ["01/01/2026"],
        "category": ["Category1"],
        "status": ["Completed"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeUpdateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testUpdateTaskMinimumFields(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": ["3"],
        "name": ["TaskNameAa"],
        "description": [""],
        "deadline": [""],
        "category": ["", "yes"],
        "status": ["2"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeUpdateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testUpdateTaskExtremeLowerInvalid(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": ["3"],
        "name": ["Aa", "AaAaA"],
        "description": [""],
        "deadline": [""],
        "category": ["Aa", "AaAaA", "yes"],
        "status": ["4"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeUpdateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testUpdateTaskExtremeUpperInvalid(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": ["3"],
        "name": ["A" * 33, "A" * 32],
        "description": ["A" * 256, "A" * 255],
        "deadline": ["01/01/2026"],
        "category": ["Aa", "AaAaA", "yes"],
        "status": ["1"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeUpdateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testUpdateTaskDontConfirmCategory(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": ["3"],
        "name": ["AaAaA"],
        "description": [""],
        "deadline": [""],
        "category": ["AaAaA", "no", "AaAaAa", "yes"],
        "status": ["In progress"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeUpdateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


# deleteTask
def testDeleteTask(monkeypatch, dummyModel):
    userInputs = ["3", "yes"]
    monkeypatch.setattr(
        userInterface, "getUserInput", helpers.mockGetUserInputFactory(iter(userInputs))
    )
    monkeypatch.setattr(userInterface, "outputTask", helpers.mockOutputTask)

    taskToDelete = dummyModel._tasksById[userInputs[0]]

    controllers.deleteTask(dummyModel)

    assert (
        dummyModel._tasksById.get(taskToDelete.id) is None
    ), f"Expected task {taskToDelete.id!r} to be deleted.\n"


def testDeleteTaskDontConfirm(monkeypatch, dummyModel):
    userInputs = ["3", "no"]
    monkeypatch.setattr(
        userInterface, "getUserInput", helpers.mockGetUserInputFactory(iter(userInputs))
    )
    monkeypatch.setattr(userInterface, "outputTask", helpers.mockOutputTask)

    taskToNotDelete = dummyModel._tasksById[userInputs[0]]

    controllers.deleteTask(dummyModel)

    assert (
        dummyModel._tasksById.get(taskToNotDelete.id) is not None
    ), f"Expected task {taskToNotDelete.id!r} to remain in the model.\n"
