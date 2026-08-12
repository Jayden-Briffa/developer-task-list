# Planned functions
| Section | Name | Processing | Input | Output |
|---|---|---|---|---|
| Model | `saveTasks` | Write to `tasks.json` and load new state. | `tasksById: dict[str, Task]` | `tasksById`, `taskIdsByCategory`, `taskIdsByName` |
| Model | `loadTasks` | Read from `tasks.json` and return `tasksById`. | — | `tasksById`, `taskIdsByCategory`, `taskIdsByName` |
| Model | `insertTask` | Add new task to `tasksById` and `taskIdsByCategory`, then retrieve from `tasksById`. | `newTask: Task` | `newTask: Task` |
| Model | `updateTask` | Update attributes in `tasksById` to match `newTask`, then return task from `tasksById`. | `updatedTask: Task` | `updatedTask: Task` |
| Model | `deleteTask` | Remove the task with the given ID from `tasksById`, `taskIdsByCategory`, and `taskIdsByName`. | `taskId: integer` | `successful: boolean` |
| Model | `selectTasksByIds` | Return the task data for a given id in `tasksById`. | `taskId: integer` | `task: Task` |
| Model | `selectTasksByNames` | Retrieve the id associated with the given name from `taskIdsByName`, then call and return `retrieveTaskById`. | `taskName: string` | `task: Task` |
| Model | `selectTasksByCategories` | Retrieve the id associated with the given name from `taskIdsByCategory`, then call and return `retrieveTaskById`. | `category: string` | `task: Task` |
| Controllers | `createNewTask` | Ask the user to input task data, validate data inputs, then add and output the new task. | — | — |
| Controllers | `updateExistingTask` | Ask the user to input task data, validate data inputs, then update and output the task. | — | — |
| Controllers | `deleteExistingTask` | Ask the user to enter the task `id` or `name`, validate its existence, delete the task from all storage objects, and output confirmation of deletion. | — | — |
| Controllers | `outputAllTasks` | Output all tasks under clear categories to the terminal. | — | — |
| Controllers | `outputTask` | Ask for the target task `id` or `name` and output that task data. | — | — |
| InputsAndOutputs | `getMenuChoice` | Output a list of choices as a standard menu format, then ask for, validate, and return the user input. | `choices: dict[integer, string]` | `choice: integer` |
| InputsAndOutputs | `getUserInput` | Output a standard-formatted prompt message and return the user input. | `prompt: string` | `userInput: string` |
| Validators | `validateChoice` | Validate that the given choice corresponds to a valid choice. | `choices: dict[int, string]` | `isValid: boolean` |
| Validators | `validateTask` | Validate that a task data is valid. | `task: Task` | `isValid: boolean` |
| Validators | `validateCategory` | Validate that a category name is valid. | `category: string` | `isValid: boolean` |

# Schemas
## Task
| name | description | type | constraints | required/optional |
| --- | --- | --- | --- | --- |
| id | Persistent unique identifier for each task | string | | required |
| name | User-friendly summary of task | string | 3 <= len() <= 32 | required |
| description | Full task details | string | len() <= 255 | optional | 
| deadline | When the task should be completed by | string | Can be converted to Date("dd/mm/yyyy") | optional |
| category | Which group of tasks is the task in | string | 3 <= len() <= 16 | optional |