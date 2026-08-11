from TasksModel import TasksModel
from Task import Task
import userInterface
import validation


def viewAllTasksByCategory(model: TasksModel):
    tasksByCategory = model.selectTasksByCategories()
    userInterface.outputTasksByCategory(tasksByCategory)


def viewTaskById(model: TasksModel):
    taskById = userInterface.getValidatedUserInput(
        "Enter the task id:", validation.validateExistingTaskId, model=model
    )
    userInterface.outputTask(taskById)


def viewTaskByName(model: TasksModel):
    taskByName = userInterface.getValidatedUserInput(
        "Enter the task name: ", validation.validateExistingTaskName, model=model
    )
    userInterface.outputTask(taskByName)


def getConfirmedTaskCategory(model: TasksModel):
    while True:
        category = userInterface.getValidatedUserInput(
            "Enter the task category: ", validation.validateTaskCategory
        )

        if category not in model.selectTasksByCategories.keys():
            confirmation = userInterface.getUserInput(
                "Only 'yes' will be accepted: ", format=False
            )
            if confirmation != "yes":
                continue

            return category


def createTask(model: TasksModel):
    taskName = userInterface.getValidatedUserInput(
        "Enter the task name: ", validation.validateTaskName
    )
    # What if the user missinputted on the main menu and doesn't want to enter all fields?
    description = userInterface.getValidatedUserInput(
        "Enter the task description: ", validation.validateTaskDescription
    )
    deadline = userInterface.getValidatedUserInput(
        "Enter the task deadline (DD/MM/YYYY): ", validation.validateTaskDeadline
    )
    category = userInterface.getValidatedUserInput(
        "Enter the task category: ", validation.validateTaskCategory
    )

    if category not in model.selectTasksByCategories.keys():
        confirmation = userInterface.getUserInput(
            "Only 'yes' will be accepted: ", format=False
        )
        if confirmation != "yes":
            return

    # What if this fails
    newTask = model.insertTask(
        name=taskName, description=description, deadline=deadline, category=category
    )

    userInterface.outputTask(newTask)


def updateTask(model: TasksModel):
    taskById = userInterface.getValidatedUserInput(
        "Enter the task id:", validation.validateExistingTaskId, model=model
    )

    name = userInterface.getValidatedUserInput(
        "Enter the task name: ", validation.validateTaskName, default=taskById.name
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
    category = userInterface.getValidatedUserInput(
        "Enter the task category: ",
        validation.validateTaskCategory,
        default=taskById.category,
    )

    model.updateTask(taskById.id, name, description, deadline, category)


def deleteTask(model: TasksModel):
    taskById = userInterface.getValidatedUserInput(
        "Enter the task id:", validation.validateExistingTaskId, model=model
    )

    print("Confirm deletion of the following task:\n")
    userInterface.outputTask(taskById)
    confirmation = userInterface.getUserInput(
        "Only 'yes' will be accepted: ", format=False
    )

    if confirmation != "yes":
        return

    model.deleteTask(taskById.id)
