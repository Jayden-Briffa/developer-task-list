import json

import pytest

from Task import Task
from TasksModel import TasksModel

import helpers


def testSaveTasks(tmp_path, dummyData):
    storePath = tmp_path / "testTasks.json"
    model = TasksModel(storePath)

    model._tasksById = dummyData

    model.saveTasks()

    with open(storePath, "r") as f:
        contents = json.load(f)

    assert contents["tasksById"]["1"]["id"] == dummyData["1"].id, (
        f"Expected saved task id for task 1 to be {dummyData['1'].id!r}.\n"
        f"expected={dummyData['1'].id!r}\n"
        f"actual={contents['tasksById']['1']['id']!r}"
    )
    assert contents["tasksById"]["2"]["id"] == dummyData["2"].id, (
        f"Expected saved task id for task 2 to be {dummyData['2'].id!r}.\n"
        f"expected={dummyData['2'].id!r}\n"
        f"actual={contents['tasksById']['2']['id']!r}"
    )


def testLoadTasks(dummyModel, dummyData):

    dummyModel._tasksById = dict()  # Empty before loading again
    dummyModel.loadTasks()

    assert dummyModel._tasksById["1"].id == dummyData["1"].id, (
        f"Expected loaded id for task 1 to be {dummyData['1'].id!r}.\n"
        f"expected={dummyData['1'].id!r}\n"
        f"actual={dummyModel._tasksById['1'].id!r}"
    )
    assert dummyModel._tasksById["2"].id == dummyData["2"].id, (
        f"Expected loaded id for task 2 to be {dummyData['2'].id!r}.\n"
        f"expected={dummyData['2'].id!r}\n"
        f"actual={dummyModel._tasksById['2'].id!r}"
    )

    assert (
        dummyData["1"].id in dummyModel._taskIdsByCategory[dummyData["1"].category]
    ), (
        f"Expected task id {dummyData['1'].id!r} to be in category {dummyData['1'].category!r}.\n"
        f"expected={dummyData['1'].id!r}\n"
        f"actual={dummyModel._taskIdsByCategory.get(dummyData['1'].category)!r}"
    )
    assert (
        dummyData["2"].id in dummyModel._taskIdsByCategory[dummyData["2"].category]
    ), (
        f"Expected task id {dummyData['2'].id!r} to be in category {dummyData['2'].category!r}.\n"
        f"expected={dummyData['2'].id!r}\n"
        f"actual={dummyModel._taskIdsByCategory.get(dummyData['2'].category)!r}"
    )

    assert dummyModel._taskIdsByName[dummyData["1"].name] == dummyData["1"].id, (
        f"Expected task name mapping for {dummyData['1'].name!r} to be {dummyData['1'].id!r}.\n"
        f"expected={dummyData['1'].id!r}\n"
        f"actual={dummyModel._taskIdsByName.get(dummyData['1'].name)!r}"
    )
    assert dummyModel._taskIdsByName[dummyData["2"].name] == dummyData["2"].id, (
        f"Expected task name mapping for {dummyData['2'].name!r} to be {dummyData['2'].id!r}.\n"
        f"expected={dummyData['2'].id!r}\n"
        f"actual={dummyModel._taskIdsByName.get(dummyData['2'].name)!r}"
    )


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
    helpers.assertTaskHasSameValues(dummyModel._tasksById["4"], taskToInsert)


def testSelectTasksByIds(dummyModel):
    foundTasks = dummyModel.selectTasksByIds(["2", "1"])
    validTasks = {
        "1": dummyModel._tasksById["1"],
        "2": dummyModel._tasksById["2"],
    }

    for validTask in validTasks.values():
        helpers.assertTaskHasSameValues(foundTasks[validTask.id], validTask.__dict__)


def testSelectTasksByCategory(dummyModel):
    foundTasks = dummyModel.selectTasksByCategories(["category2"])

    assert {task.id for task in foundTasks["category2"]} == {"2", "3"}, (
        f"Expected category2 tasks to be {{'2', '3'}}.\n"
        f"expected={{'2', '3'}}\n"
        f"actual={ {task.id for task in foundTasks['category2']}!r }"
    )


def testSelectTasksByNames(dummyModel):
    foundTasks = dummyModel.selectTasksByNames(["task1", "task2"])

    assert {task.id for task in foundTasks.values()} == {"1", "2"}, (
        f"Expected matched task ids to be {{'1', '2'}}.\n"
        f"expected={{'1', '2'}}\n"
        f"actual={ {task.id for task in foundTasks.values()}!r }"
    )


def testUpdateTask(dummyModel):
    updatedTaskData = {
        "name": "newTask2",
        "description": "myNewDescription",
        "deadline": "30/10/2026",
        "category": "category1",
    }
    dummyModel.updateTask("2", **updatedTaskData)

    updatedTaskData["id"] = "2"
    helpers.assertTaskHasSameValues(dummyModel._tasksById["2"], updatedTaskData)


def testDeleteTask(dummyModel, dummyData):
    dummyModel.deleteTask("2")

    assert dummyData["2"].id not in dummyModel._tasksById, (
        f"Expected task id {dummyData['2'].id!r} to be removed from _tasksById.\n"
        f"expected={dummyData['2'].id!r} not in model\n"
        f"actual={list(dummyModel._tasksById.keys())!r}"
    )
    assert (
        dummyData["2"].id not in dummyModel._taskIdsByCategory[dummyData["2"].category]
    ), (
        f"Expected task id {dummyData['2'].id!r} to be removed from category {dummyData['2'].category!r}.\n"
        f"expected={dummyData['2'].id!r} not in {dummyModel._taskIdsByCategory.get(dummyData['2'].category)!r}\n"
        f"actual={dummyModel._taskIdsByCategory.get(dummyData['2'].category)!r}"
    )
    assert dummyData["2"].name not in dummyModel._taskIdsByName, (
        f"Expected task name {dummyData['2'].name!r} to be removed from _taskIdsByName.\n"
        f"expected={dummyData['2'].name!r} not in model\n"
        f"actual={dummyModel._taskIdsByName!r}"
    )
