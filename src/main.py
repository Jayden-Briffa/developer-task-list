from userInterface import getMenuInput, outputError
import controllers
from TasksModel import TasksModel

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

while True:
    userChoice = getMenuInput("Home", menuChoices)

    match userChoice:

        case "1":
            controllers.viewAllTasksByCategory()

        case "2":
            controllers.viewTaskById()

        case "3":
            controllers.viewTaskByName()

        case "4":
            controllers.createTask()

        case "5":
            controllers.updateTask()

        case "6":
            controllers.deleteTask()

        case "7":
            print("Exiting program...")
            exit()

        case _:
            outputError(
                f"Invalid menu input. You must enter numbers (1-{len(menuChoices)}) or the full phrase"
            )
