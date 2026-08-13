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
        "Enter the task name: ",
        lambda userInput, model: validation.validateTaskName(
            userInput, model=model, requireNew=False
        ),
        model=model,
    )

    return userInterface.outputTask(taskByName)


def createTask(model: TasksModel):
    taskName = userInterface.getValidatedUserInput(
        "Enter the task name: ", validation.validateTaskName, model=model
    )

    description = userInterface.getValidatedUserInput(
        "Enter the task description: ", validation.validateTaskDescription
    )
    deadline = userInterface.getValidatedUserInput(
        "Enter the task deadline (DD/MM/YYYY): ", validation.validateTaskDeadline
    )

    category = userInterface.getConfirmedTaskCategory(model)
    status = userInterface.getTaskStatusChoice()

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
            userInput, model=model, currentTaskId=taskById.id, requireNew=True
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

    category = userInterface.getConfirmedTaskCategory(model, default=taskById.category)
    status = userInterface.getTaskStatusChoice(default=taskById.status)

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
