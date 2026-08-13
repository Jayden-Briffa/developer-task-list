from TasksModel import TasksModel
from Task import Task
import userInterface
import validation


def viewAllTasksByCategory(model: TasksModel):
    tasksByCategory = model.selectTasksByCategories()
    return userInterface.outputTasksByCategory(tasksByCategory)


def viewTaskById(model: TasksModel):
    taskById = userInterface.getValidatedUserInput(
        "Enter the task id:", validation.validateExistingTaskId, model=model
    )
    return userInterface.outputTask(taskById)


def viewTaskByName(model: TasksModel):
    taskByName = userInterface.getValidatedUserInput(
        "Enter the task name: ", validation.validateExistingTaskName, model=model
    )

    return userInterface.outputTask(taskByName)


def getConfirmedTaskCategory(model: TasksModel, default: str = "") -> str:
    while True:
        existingCategories = list(model.selectTasksByCategories().keys())
        print("Available categories:")
        if len(existingCategories) == 0:
            print("- <none>")
        else:
            for existingCategory in existingCategories:
                categoryLabel = existingCategory if existingCategory != "" else "<no output>"
                print(f"- {categoryLabel}")

        print("Or enter a new category to create it.")

        category = userInterface.getValidatedUserInput(
            "Enter the task category: ",
            validation.validateTaskCategory,
            default=default,
        )
        existingCategory = any(
            storedCategory.lower() == category.lower()
            for storedCategory in model.selectTasksByCategories().keys()
        )
        if not existingCategory:
            print()
            print(
                f"This will create a new category. Are you sure you want to use the category '{category}'?"
            )
            confirmation = userInterface.getUserInput(
                "Only 'yes' will be accepted: ", format=False
            )
            if confirmation.lower() == "yes":
                break

        else:
            break

    return category


TASK_STATUS_OPTIONS = [
    "Not started",
    "In progress",
    "Blocked",
    "Testing",
    "Completed",
]


def getTaskStatusChoice(default: str = "Not started") -> str:
    return userInterface.getMenuChoiceInput(
        "Select task status",
        TASK_STATUS_OPTIONS,
        defaultChoice=default,
    )


def createTask(model: TasksModel):
    taskName = userInterface.getValidatedUserInput(
        "Enter the task name: ", validation.validateTaskName, model=model
    )
    # What if the user missinputted on the main menu and doesn't want to enter all fields?
    description = userInterface.getValidatedUserInput(
        "Enter the task description: ", validation.validateTaskDescription
    )
    deadline = userInterface.getValidatedUserInput(
        "Enter the task deadline (DD/MM/YYYY): ", validation.validateTaskDeadline
    )

    category = getConfirmedTaskCategory(model)
    status = getTaskStatusChoice()

    # What if this fails
    newTask = model.insertTask(
        name=taskName,
        description=description,
        deadline=deadline,
        category=category,
        status=status,
    )

    print("Task created")
    return userInterface.outputTask(newTask)


def updateTask(model: TasksModel):
    taskById = userInterface.getValidatedUserInput(
        "Enter the task id: ", validation.validateExistingTaskId, model=model
    )

    name = userInterface.getValidatedUserInput(
        "Enter the task name: ",
        lambda userInput, model: validation.validateTaskName(
            userInput, model=model, currentTaskId=taskById.id
        ),
        model=model,
        default=taskById.name,
    )
    description = userInterface.getValidatedUserInput(
        "Enter the task description: ",
        validation.validateTaskDescription,
        default=taskById.description,
    )
    deadline = userInterface.getValidatedUserInput(
        "Enter the task deadline (DD/MM/YYYY): ",
        validation.validateTaskDeadline,
        default=taskById.deadline,
    )

    category = getConfirmedTaskCategory(model, default=taskById.category)
    status = getTaskStatusChoice(default=taskById.status)

    result = model.updateTask(
        taskById.id, name, description, deadline, category, status
    )
    print("Task updated")
    userInterface.outputTask(result)
    return result


def deleteTask(model: TasksModel):
    taskById = userInterface.getValidatedUserInput(
        "Enter the task id:", validation.validateExistingTaskId, model=model
    )

    print("Confirm deletion of the following task:\n")
    userInterface.outputTask(taskById, pressEnter=False)
    print("Are you sure you want to delete this task? This action cannot be undone.")
    confirmation = userInterface.getUserInput(
        "Only 'yes' will be accepted: ", format=False
    )

    if confirmation.lower() != "yes":
        return

    result = model.deleteTask(taskById.id)
    print("Task deleted")
    return result


def saveTasks(model: TasksModel):
    print("Saving...")
    model.saveTasks()
