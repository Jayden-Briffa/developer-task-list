import userInterface
import controllers
from TasksModel import TasksModel
from Task import Task

menuChoices = [
    "View all tasks, sorted by category",  # 1
    "View a task with task id",  # 2
    "View a task with task name",  # 3
    "Create a new task",  # 4
    "Update an existing task",  # 5
    "Delete a task",  # 6
    "Quit",  # 7
]

tasksModel = TasksModel("taskData.json")
tasksModel._tasksById = {
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
tasksModel._taskIdsByCategory = {
    "category1": ["1"],
    "category2": ["2", "3"],
}
tasksModel._taskIdsByName = {
    "task1": "1",
    "task2": "2",
    "task3": "3",
}
tasksModel._lastInsertId = 3

while True:
    userChoice = userInterface.getMenuInput("Home", menuChoices)

    match userChoice:

        case "0":
            controllers.viewAllTasksByCategory(tasksModel)

        case "1":
            controllers.viewTaskById(tasksModel)

        case "2":
            controllers.viewTaskByName(tasksModel)

        case "3":
            controllers.createTask(tasksModel)

        case "4":
            controllers.updateTask(tasksModel)

        case "5":
            controllers.deleteTask(tasksModel)

        case "6":
            print("Exiting program...")
            exit()

        case _:
            userInterface.outputError(
                f"Invalid menu input. You must enter numbers (0-{len(menuChoices) - 1}) or the full phrase"
            )

    controllers.saveTasks(tasksModel)

# TODO: handle model errors, e.g., id not found
# TODO: Preserve input case for task name etc. but validate against case-insensitive duplicates
# TODO: Handle duplicate task names
# TODO: Show present categories when altering a task's category
# TODO: Allow the user to abort a menu choice by entering a special phrase at any input, e.g., "abort"
# TODO: Include category in task output
