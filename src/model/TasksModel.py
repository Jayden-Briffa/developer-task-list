import json
import os
from Task import Task


class TasksModel:
    _jsonStorePath: str
    _tasksById: dict[str, Task]
    _taskIdsByCategory: dict[str, list[int]]
    _taskIdsByName: dict[str, int]
    _lastInsertId: int

    def __init__(self, filePath: str):
        if not os.path.exists(filePath):
            with open(filePath, "w") as _:
                pass

            self._lastInsertId = 0
            self._tasksById = dict()
            self._taskIdsByCategory = dict()
            self._taskIdsByName = dict()

        self._jsonStorePath = filePath

        self.loadTasks()

    def loadTasks(self) -> None:
        with open(self._jsonStorePath, "r"):
            loaded = json.load(self._jsonStorePath)
            self._tasksById = loaded.tasksById
            self._lastInsertId = loaded.lastInsertId

        for id, task in self._tasksById:
            self._taskIdsByCategory[task.category].append(id)
            self._taskIdsByName[task.name] = id

    def saveTasks(self) -> None:
        toSave = {"tasksById": self._tasksById, "lastInsertId": self._lastInsertId}

        with open(self._jsonStorePath, "w") as f:
            json.dump(toSave, f)

    # Selectors
    def selectTasks(self) -> dict[str, Task]:
        return self._tasksById

    def selectTasksByIds(self, ids: list[int]) -> dict[int, Task]:
        foundTasks = []

        for id in ids:
            foundTask = self._tasksById[id]
            foundTasks.append(foundTask)

        return foundTasks

    def selectTasksByCategories(
        self, categories: list[str] = []
    ) -> dict[str, list[Task]]:
        if categories == []:

            # Does not use self._taskIdsByCategory as it provides no speed benefit when iterating over all tasks
            categorised = dict()
            for _, task in self._tasksById:
                if not categorised[task.category]:
                    categorised[task.category] = []

                categorised[task.category].append(task)

            return categorised

        foundTasks = {}
        for category in categories:
            if not categorised[task.category]:
                categorised[task.category] = []

            taskIdsInCategory = self._taskIdsByCategory[category]
            for id in taskIdsInCategory:
                foundTask = self._tasksById[id]
                foundTasks[category].append(foundTask)

        return foundTasks

    def selectTasksByNames(self, names: list[str] = []) -> dict[str, Task]:
        foundTasks = {}

        if names == []:
            for _, task in self._tasksById:
                foundTasks[task.name] = task

            return foundTasks

        for name in names:
            foundTask = self._taskIdsByName[name]
            foundTasks[name] = self._tasksById[foundTask.id]

        return foundTasks

    # Insert
    def insertTask(self, name: str, description: str, deadline: str, category: str):
        self._lastInsertId += 1
        self._tasksById[self._lastInsertId] = Task(
            id=self._lastInsertId,
            name=name,
            description=description,
            deadline=deadline,
            category=category,
        )

        if not self._taskIdsByCategory.get(category):
            self._taskIdsByCategory[category] = []

        self._taskIdsByCategory[category].append(self._lastInsertId)
        self._taskIdsByName[name] = self._lastInsertId

        return self._tasksById[self._lastInsertId]

    # Update
    def updateTask(
        self, id: int, name: str, description: str, deadline: str, category: str
    ):

        # Verify task existence, otherwise the following statement could create a new task
        oldTask = self.selectTasksByIds([id])

        self._tasksById[id] = Task(
            id=id,
            name=name,
            description=description,
            deadline=deadline,
            category=category,
        )

        # Clean up now-empty category
        if len(self._taskIdsByCategory[oldTask.category]) == 0:
            del self._taskIdsByCategory[oldTask.category]

    # Delete
    def deleteTask(self, id: int):
        task = self.selectTasksByIds([id])

        self._tasksById.pop(task.id)
        self._taskIdsByCategory[task.category].remove(task.id)
        self._taskIdsByName.pop(task.name)

        if len(self._taskIdsByCategory[task.category]) == 0:
            del self._taskIdsByCategory[task.category]


# TODO: Test that file is created at init if not exists
# TODO: Validate filePath before initing
