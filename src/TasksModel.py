import json
import os

from Task import Task


class TasksModel:
    _jsonStorePath: str
    _tasksById: dict[str, Task]
    _taskIdsByCategory: dict[str, list[str]]
    _taskIdsByName: dict[str, str]
    _lastInsertId: int

    def __init__(self, filePath: str):
        self._jsonStorePath = filePath
        self._tasksById = {}
        self._taskIdsByCategory = {}
        self._taskIdsByName = {}
        self._lastInsertId = 0

        if not os.path.exists(filePath):
            with open(filePath, "w") as f:
                json.dump({"tasksById": {}, "lastInsertId": 0}, f)

        self.loadTasks()

    def loadTasks(self) -> None:
        with open(self._jsonStorePath, "r") as f:
            loaded = json.load(f)

        self._tasksById = {}
        self._taskIdsByCategory = {}
        self._taskIdsByName = {}
        self._lastInsertId = int(loaded.get("lastInsertId", 0))

        for rawId, task in loaded.get("tasksById", {}).items():
            taskId = str(rawId)
            self._tasksById[taskId] = Task(
                id=taskId,
                name=task["name"],
                description=task["description"],
                deadline=task["deadline"],
                category=task["category"],
            )

            if not self._taskIdsByCategory.get(task["category"]):
                self._taskIdsByCategory[task["category"]] = []

            self._taskIdsByCategory[task["category"]].append(rawId)
            self._taskIdsByName[task["name"]] = rawId

    def saveTasks(self) -> None:
        toSave = {
            "tasksById": {
                taskId: task.__dict__ for taskId, task in self._tasksById.items()
            },
            "lastInsertId": self._lastInsertId,
        }

        with open(self._jsonStorePath, "w") as f:
            json.dump(toSave, f)

    # Selectors
    def selectTasksByIds(self, ids: list[str] | None = None) -> dict[str, Task]:
        if not ids:
            return self._tasksById

        return {str(taskId): self._tasksById[str(taskId)] for taskId in ids}

    # TODO: Adjust methods to match prototype scope
    def selectTasksByCategories(
        self, categories: list[str] = []
    ) -> dict[str, list[Task]]:
        if categories == []:

            # Does not use self._taskIdsByCategory as it provides no speed benefit when iterating over all tasks
            categorised = dict()
            for _, task in self._tasksById.items():
                if not categorised.get(task.category):
                    categorised[task.category] = []

                categorised[task.category].append(task)

            return categorised

        foundTasks = {}
        for category in categories:
            foundTasks[category] = []
            for taskId in self._taskIdsByCategory.get(category, []):
                foundTasks[category].append(self._tasksById[taskId])

        return foundTasks

    def selectTasksByNames(self, names: list[str] | None = None) -> dict[str, Task]:
        foundTasks = {}

        if not names:
            for task in self._tasksById.values():
                foundTasks[task.name] = task
            return foundTasks

        for name in names:
            taskId = self._taskIdsByName[name]
            foundTasks[name] = self._tasksById[taskId]

        return foundTasks

    # Create
    def insertTask(self, name: str, description: str, deadline: str, category: str):
        self._lastInsertId += 1
        taskId = str(self._lastInsertId)
        print("New task id: ", taskId)
        self._tasksById[taskId] = Task(
            id=taskId,
            name=name,
            description=description,
            deadline=deadline,
            category=category,
        )

        self._taskIdsByCategory.setdefault(category, []).append(taskId)
        self._taskIdsByName[name] = taskId

        return self._tasksById[taskId]

    # Update
    def updateTask(
        self, id: str, name: str, description: str, deadline: str, category: str
    ):
        taskId = str(id)
        oldTask = self._tasksById[taskId]

        self._tasksById[taskId] = Task(
            id=taskId,
            name=name,
            description=description,
            deadline=deadline,
            category=category,
        )

        # Clean up now-empty category
        if len(self._taskIdsByCategory[oldTask.category]) == 0:
            del self._taskIdsByCategory[oldTask.category]

        return self._tasksById[taskId]

    # Delete
    def deleteTask(self, id: str):
        taskId = str(id)
        task = self._tasksById[taskId]

        self._tasksById.pop(task.id)
        self._taskIdsByCategory[task.category].remove(task.id)
        self._taskIdsByName.pop(task.name)

        if len(self._taskIdsByCategory[task.category]) == 0:
            del self._taskIdsByCategory[task.category]


# TODO: Test that file is created at init if not exists
# TODO: Validate filePath before initing
