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
        assert category in actualOutputTasksByCategory

        # Fail if the expected task id cannot be found in the category
        for expectedTaskId in ids:
            assert any(
                task.id == expectedTaskId
                for task in actualOutputTasksByCategory[category]
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
    userInputs = ["task1"]
    monkeypatch.setattr(
        userInterface, "getUserInput", helpers.mockGetUserInputFactory(iter(userInputs))
    )
    monkeypatch.setattr(userInterface, "outputTask", helpers.mockOutputTask)

    expectedTaskToOutput = dummyModel._tasksById[
        dummyModel._taskIdsByName[userInputs[0]]
    ]

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
        "name": ["task4"],
        "description": ["description4"],
        "deadline": ["01/01/2026"],
        "category": ["category1"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeCreateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testCreateTaskExtremeLower(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "4",
        "name": ["a" * 3],
        "description": [""],
        "deadline": [""],
        "category": ["a" * 3],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeCreateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testCreateTaskExtremeUpper(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "4",
        "name": ["a" * 32],
        "description": ["a" * 255],
        "deadline": ["01/01/2026"],
        "category": ["category1"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeCreateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testCreateTaskMinimumFields(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "4",
        "name": ["a" * 10],
        "description": [""],
        "deadline": [""],
        "category": [""],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeCreateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testCreateTaskExtremeLowerInvalid(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "4",
        "name": ["a" * 2, "a" * 5],
        "description": [""],
        "deadline": [""],
        "category": ["a" * 2, "a" * 5, "yes"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeCreateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testCreateTaskExtremeUpperInvalid(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "4",
        "name": ["a" * 33, "a" * 32],
        "description": ["a" * 256, "a" * 255],
        "deadline": ["01/01/2026"],
        "category": ["a" * 2, "a" * 5, "yes"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeCreateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testCreateTaskDontConfirmCategory(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "4",
        "name": ["a" * 5],
        "description": [""],
        "deadline": [""],
        "category": ["a" * 5, "no", "a" * 5, "yes"],
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
        "id": "3",
        "name": ["task3"],
        "description": ["description3"],
        "deadline": ["01/01/2026"],
        "category": ["category1"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeUpdateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testUpdateTaskExtremeLower(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "3",
        "name": ["a" * 3],
        "description": [""],
        "deadline": [""],
        "category": ["a" * 3],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeUpdateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testUpdateTaskExtremeUpper(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "3",
        "name": ["a" * 32],
        "description": ["a" * 255],
        "deadline": ["01/01/2026"],
        "category": ["category1"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeUpdateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testUpdateTaskMinimumFields(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "3",
        "name": ["a" * 10],
        "description": [""],
        "deadline": [""],
        "category": [""],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeUpdateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testUpdateTaskExtremeLowerInvalid(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "3",
        "name": ["a" * 2, "a" * 5],
        "description": [""],
        "deadline": [""],
        "category": ["a" * 2, "a" * 5, "yes"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeUpdateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testUpdateTaskExtremeUpperInvalid(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "3",
        "name": ["a" * 33, "a" * 32],
        "description": ["a" * 256, "a" * 255],
        "deadline": ["01/01/2026"],
        "category": ["a" * 2, "a" * 5, "yes"],
    }
    expectedTask, userInputs = helpers.constructExpectedTaskAndUserInputs(
        expectedNewTaskInputs
    )

    executeUpdateTaskTestCase(monkeypatch, dummyModel, expectedTask, userInputs)


def testUpdateTaskDontConfirmCategory(monkeypatch, dummyModel):
    expectedNewTaskInputs = {
        "id": "3",
        "name": ["a" * 5],
        "description": [""],
        "deadline": [""],
        "category": ["a" * 5, "no", "a" * 5, "yes"],
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

    assert dummyModel._tasksById.get(taskToDelete.id) == None


def testDeleteTaskDontConfirm(monkeypatch, dummyModel):
    userInputs = ["3", "no"]
    monkeypatch.setattr(
        userInterface, "getUserInput", helpers.mockGetUserInputFactory(iter(userInputs))
    )
    monkeypatch.setattr(userInterface, "outputTask", helpers.mockOutputTask)

    taskToNotDelete = dummyModel._tasksById[userInputs[0]]

    controllers.deleteTask(dummyModel)

    assert dummyModel._tasksById.get(taskToNotDelete.id) != None
