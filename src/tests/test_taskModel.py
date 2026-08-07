import json

import pytest

from Task import Task
from TasksModel import TasksModel


def assertTaskHasSameValues(actualTask: Task, expectedTask: dict):
    assert actualTask.id == expectedTask["id"]
    assert actualTask.name == expectedTask["name"]
    assert actualTask.description == expectedTask["description"]
    assert actualTask.deadline == expectedTask["deadline"]
    assert actualTask.category == expectedTask["category"]


@pytest.fixture
def dummyData():
    return {
        "1": Task(
            id="1",
            name="task1",
            description="mydescription1",
            deadline="30/12/2026",
            category="category1",
        ),
        "2": Task(
            id="2",
            name="task2",
            description="mydescription2",
            deadline="30/11/2026",
            category="category2",
        ),
        "3": Task(
            id="3",
            name="task3",
            description="mydescription3",
            deadline="30/11/2026",
            category="category2",
        ),
    }


@pytest.fixture
def dummyModel(tmp_path, dummyData):
    storePath = tmp_path / "testTasks.json"
    model = TasksModel(storePath)

    model._tasksById = dummyData.copy()
    model._taskIdsByCategory = {
        "category1": ["1"],
        "category2": ["2", "3"],
    }
    model._taskIdsByName = {
        "task1": "1",
        "task2": "2",
        "task3": "3",
    }
    model._lastInsertId = 3

    model.saveTasks()

    return model


def testSaveTasks(tmp_path, dummyData):
    storePath = tmp_path / "testTasks.json"
    model = TasksModel(storePath)

    model._tasksById = dummyData

    model.saveTasks()

    with open(storePath, "r") as f:
        contents = json.load(f)

    assert contents["tasksById"]["1"]["id"] == dummyData["1"].id
    assert contents["tasksById"]["2"]["id"] == dummyData["2"].id


def testLoadTasks(dummyModel, dummyData):

    dummyModel._tasksById = dict()  # Empty before loading again
    dummyModel.loadTasks()

    assert dummyModel._tasksById["1"].id == dummyData["1"].id
    assert dummyModel._tasksById["2"].id == dummyData["2"].id

    assert dummyData["1"].id in dummyModel._taskIdsByCategory[dummyData["1"].category]
    assert dummyData["2"].id in dummyModel._taskIdsByCategory[dummyData["2"].category]

    assert dummyModel._taskIdsByName[dummyData["1"].name] == dummyData["1"].id
    assert dummyModel._taskIdsByName[dummyData["2"].name] == dummyData["2"].id


def testInsertTask(dummyModel):
    taskToInsert = {
        "name": "task4",
        "description": "mydescription4",
        "deadline": "30/11/2026",
        "category": "category2",
    }
    print(f"{taskToInsert}")
    dummyModel.insertTask(**taskToInsert)

    taskToInsert["id"] = "4"
    assertTaskHasSameValues(dummyModel._tasksById["4"], taskToInsert)


def testSelectTasksByIds(dummyModel):
    foundTasks = dummyModel.selectTasksByIds(["2", "1"])
    validTasks = {
        "1": dummyModel._tasksById["1"],
        "2": dummyModel._tasksById["2"],
    }

    for validTask in validTasks.values():
        assertTaskHasSameValues(foundTasks[validTask.id], validTask.__dict__)


def testSelectTasksByCategory(dummyModel):
    foundTasks = dummyModel.selectTasksByCategories(["category2"])

    assert {task.id for task in foundTasks["category2"]} == {"2", "3"}


def testSelectTasksByNames(dummyModel):
    foundTasks = dummyModel.selectTasksByNames(["task1", "task2"])

    assert {task.id for task in foundTasks.values()} == {"1", "2"}


def testUpdateTask(dummyModel):
    updatedTaskData = {
        "name": "newTask2",
        "description": "myNewDescription",
        "deadline": "30/10/2026",
        "category": "category1",
    }
    dummyModel.updateTask("2", **updatedTaskData)

    updatedTaskData["id"] = "2"
    assertTaskHasSameValues(dummyModel._tasksById["2"], updatedTaskData)


def testDeleteTask(dummyModel, dummyData):
    dummyModel.deleteTask("2")

    assert dummyData["2"].id not in dummyModel._tasksById
    assert dummyData["2"].id not in dummyModel._taskIdsByCategory[dummyData["2"].category]
    assert dummyData["2"].name not in dummyModel._taskIdsByName