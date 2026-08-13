import pytest
from Task import Task
from TasksModel import TasksModel
import userInterface

import helpers


@pytest.fixture
def dummyData():
    return {
        "1": Task(
            id="1",
            name="task1",
            description="mydescription1",
            deadline="30/12/2026",
            category="category1",
            status="Not started",
        ),
        "2": Task(
            id="2",
            name="task2",
            description="mydescription2",
            deadline="30/11/2026",
            category="category2",
            status="In progress",
        ),
        "3": Task(
            id="3",
            name="task3",
            description="mydescription3",
            deadline="30/11/2026",
            category="category2",
            status="Blocked",
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


# Block pressEnterToContinue from disrupting tests
@pytest.fixture(autouse=True)
def mockOutputErrorForAllTests(monkeypatch):
    monkeypatch.setattr(userInterface, "outputError", helpers.mockOutputError)
