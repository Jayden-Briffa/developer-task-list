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

while True:
    try:
        bannerBuffer = "-" * 2
        print(
            bannerBuffer,
            "TYPE 'abort' AT ANY TIME TO ABORT THE CURRENT OPERATION",
            bannerBuffer,
        )

        bannerBuffer = "=" * 5
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

    except userInterface.UserAbortException:
        print("Operation aborted by the user.")
        userInterface.pressEnterToContinue()

    except Exception as e:
        userInterface.outputError(f"An unexpected error occurred: {str(e)}")
