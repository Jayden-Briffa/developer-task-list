import pytest
import json
from model.TasksModel import TasksModel
from model.Task import Task


def assertTaskHasSameValues(actualTask, expectedTask):
    assert actualTask.id == expectedTask.id
    assert actualTask.name == expectedTask["name"]
    assert actualTask.description == expectedTask["description"]
    assert actualTask.deadline == expectedTask["deadline"]
    assert actualTask.category == expectedTask["category"]


@pytest.fixture
def dummyData():
    return {
        1: Task(
            id=1,
            name="task1",
            description="mydescription1",
            deadline="30/12/2026",
            category="category1",
        ),
        2: Task(
            id=2,
            name="task2",
            description="mydescription2",
            deadline="30/11/2026",
            category="category2",
        ),
        3: Task(
            id=3,
            name="task3",
            description="mydescription3",
            deadline="30/11/2026",
            category="category2",
        ),
    }


@pytest.fixture
def dummyModel(tmp_path, dummyData):
    model = TasksModel(tmp_path)

    model._tasksById = dummyData

    model.saveTasks()

    return model


def testSaveTasks(tmp_path, dummyData):
    model = TasksModel(tmp_path)

    model._tasksById = dummyData

    model.saveTasks()

    contents = {}
    with open("testTasks.json", "r") as f:
        contents = json.load(f)

    assert contents[1] == dummyData[1]
    assert contents[2] == dummyData[2]


def testLoadTasks(dummyModel, dummyData):

    dummyModel._tasksById = dict()  # Empty before loading again
    dummyModel.loadTasks()

    assert dummyModel._tasksById[1] == dummyData[1]
    assert dummyModel._tasksById[2] == dummyData[2]

    assert dummyData[1].id in dummyModel._taskIdsByCategory[dummyData[1].category]
    assert dummyData[2].id in dummyModel._taskIdsByCategory[dummyData[2].category]

    assert dummyModel._taskIdsByName[dummyData[1].name] == dummyData[1].id
    assert dummyModel._taskIdsByName[dummyData[2].name] == dummyData[2].id


def testInsertTask(dummyModel):
    taskToInsert = {
        "name": "task2",
        "description": "mydescription2",
        "deadline": "30/11/2026",
        "category": "category2",
    }

    dummyModel.insertTask(*taskToInsert)

    taskToInsert["id"] = 4
    assertTaskHasSameValues(dummyModel._tasksById[4], taskToInsert)


def testSelectTasksById(dummyModel):
    foundTasks = dummyModel.selectTasksById([2, 1])
    validTasks = {
        1: dummyModel._tasksById[1],
        2: dummyModel._tasksById[2],
    }

    for validTask in validTasks:
        validTask["id"] = 4
        assertTaskHasSameValues(foundTasks[validTask.id], validTask)


def testSelectTasksByCategory(dumyModel):
    foundTasks = dumyModel.selectTasksByCategories(["category2"])

    for id in [1, 2]:
        assert any(task.id == id for task in foundTasks)


def testSelectTasksByNames(dumyModel):
    foundTasks = dumyModel.selectTasksByNames(["task1", "task2"])

    for id in [1, 2]:
        assert any(task.id == id for task in foundTasks)


def testUpdateTask(dummyModel):
    updatedTaskData = {
        "name": "newTask2",
        "description": "myNewDescription",
        "deadline": "30/10/2026",
        "category": "category1",
    }
    dummyModel.updateTask(2, *updatedTaskData)

    updatedTaskData["id"] = 2
    assertTaskHasSameValues(dummyModel._tasksById[2], updatedTaskData)


def testDeleteTask(dummyModel, dummyData):
    dummyModel.deleteTask(2)

    assert dummyData[2].id not in dummyModel._tasksById
    assert dummyData[2].id not in dummyModel._taskIdsByCategory[dummyData[2].category]
    assert dummyData[2].name not in dummyModel._taskIdsByName
