import time

from Task import Task
from TasksModel import TasksModel

import pytest


def buildLargeTaskDataset():
    categories = [f"category{index}" for index in range(20)]
    tasksById = {}
    taskIdsByCategory = {}
    taskIdsByName = {}

    for index in range(1, 1001):
        taskId = str(index)
        category = categories[(index - 1) % len(categories)]
        task = Task(
            id=taskId,
            name=f"task{index}",
            description=f"description{index}",
            deadline="30/11/2026",
            category=category,
        )

        tasksById[taskId] = task
        taskIdsByCategory.setdefault(category, []).append(taskId)
        taskIdsByName[task.name] = taskId

    return tasksById, taskIdsByCategory, taskIdsByName


def resetLargeDatasetModel(model: TasksModel):
    tasksById, taskIdsByCategory, taskIdsByName = buildLargeTaskDataset()
    model._tasksById = tasksById
    model._taskIdsByCategory = taskIdsByCategory
    model._taskIdsByName = taskIdsByName
    model._lastInsertId = len(tasksById)


@pytest.fixture
def largeDatasetDummyModel(tmp_path):
    storePath = tmp_path / "largeDatasetTasks.json"
    tasksById, taskIdsByCategory, taskIdsByName = buildLargeTaskDataset()

    model = TasksModel(storePath)
    model._tasksById = tasksById
    model._taskIdsByCategory = taskIdsByCategory
    model._taskIdsByName = taskIdsByName
    model._lastInsertId = len(tasksById)

    return model, tasksById, taskIdsByCategory


def assertMethodCompletesInTime(methodName, callback, maxDuration=0.5, beforeEach=None):

    totalDuration = 0
    numRuns = 5
    for _ in range(numRuns):
        if beforeEach is not None:
            beforeEach()

        startTime = time.perf_counter()
        callback()
        actualDuration = time.perf_counter() - startTime

        totalDuration += actualDuration

    averageDuration = totalDuration / numRuns

    assert averageDuration < maxDuration, (
        f"Expected {methodName} to complete in under {maxDuration:.1f}s.\n"
        f"expected=< {maxDuration:.1f}s\n"
        f"actual={averageDuration:.6f}s"
    )


def testSaveTasksLargeDatasetUnderHalfSecond(largeDatasetDummyModel):
    model, _, _ = largeDatasetDummyModel
    assertMethodCompletesInTime("saveTasks", lambda: model.saveTasks())


def testSelectTasksByIdsLargeDatasetUnderHalfSecond(largeDatasetDummyModel):
    model, tasksById, _ = largeDatasetDummyModel
    assertMethodCompletesInTime(
        "selectTasksByIds",
        lambda: model.selectTasksByIds(list(tasksById.keys())),
    )


def testSelectTasksByCategoriesLargeDatasetUnderHalfSecond(largeDatasetDummyModel):
    model, _, taskIdsByCategory = largeDatasetDummyModel
    assertMethodCompletesInTime(
        "selectTasksByCategories",
        lambda: model.selectTasksByCategories(list(taskIdsByCategory.keys())),
    )


def testSelectTasksByNamesLargeDatasetUnderHalfSecond(largeDatasetDummyModel):
    model, _, _ = largeDatasetDummyModel
    assertMethodCompletesInTime(
        "selectTasksByNames",
        lambda: model.selectTasksByNames([f"task{index}" for index in range(1, 1001)]),
    )


def testInsertTaskLargeDatasetUnderHalfSecond(largeDatasetDummyModel):
    model, _, _ = largeDatasetDummyModel
    assertMethodCompletesInTime(
        "insertTask",
        lambda: model.insertTask(
            name="task1001",
            description="description1001",
            deadline="30/11/2026",
            category="category0",
        ),
        beforeEach=lambda: resetLargeDatasetModel(model),
    )


def testUpdateTaskLargeDatasetUnderHalfSecond(largeDatasetDummyModel):
    model, _, _ = largeDatasetDummyModel
    assertMethodCompletesInTime(
        "updateTask",
        lambda: model.updateTask(
            "500",
            name="updatedTask500",
            description="updatedDescription500",
            deadline="31/12/2026",
            category="category7",
        ),
        beforeEach=lambda: resetLargeDatasetModel(model),
    )


def testDeleteTaskLargeDatasetUnderHalfSecond(largeDatasetDummyModel):
    model, _, _ = largeDatasetDummyModel
    assertMethodCompletesInTime(
        "deleteTask",
        lambda: model.deleteTask("1"),
        beforeEach=lambda: resetLargeDatasetModel(model),
    )


def testLoadTasksLargeDatasetUnderHalfSecond(largeDatasetDummyModel):
    model, _, _ = largeDatasetDummyModel
    assertMethodCompletesInTime("loadTasks", lambda: model.loadTasks())
