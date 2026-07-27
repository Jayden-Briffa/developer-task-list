## Values
taskById{standard}

## Unit tests

| Test # | Depends on ids | Test type | Requirement links | Function | Description | Inputs | Expected results |
|---|---|---|---|---|---|---|---|
| — | — | Normal | FR3 | `loadTasks` | Accurately retrieves data from `tasks.json` and returns appropriate task storage objects. | — | Data from `tasksById` reflects `tasks.json` identically, and `taskIdsByName` and `taskIdsByCategory` map name and category to the correct id. |
| — | — | Normal | FR3 | `saveTasks` | Accurately overwrites `tasks.json` with the data from `tasksById`. | `tasksById= taskById{standard}` | Data in `tasks.json` matches: `taskById{standard} `|
| — | — | Boundary | FR1, FR1 | `createNewTask` | Adds the task with the given information to the task storage objects when given minimal but valid data. | `tasksById= taskById{standard}`<br>`newTask= {name: "a"*3}` | `tasksById` is updated to: `{1: {name:"task1"}, 2: {name:"task2"}, 3: {name:"a"*3}}` |
| — | — | Invalid / Boundary | NFR2 | `createNewTask` | Appropriate error messages are output when invalid inputs are given and the user may retry input. | `newTask= {name: "ta", deadline: "invalid"}` | The following error messages are output:<br><br>`Field 'name' must be between 3 and 255 characters long (inclusive)`<br><br>`Field 'deadline' must be a date in the format dd:mm:yyyy` |
| — | — | Normal | FR1 | `updateTask` | Replaces the information in `tasksById` with the given task data. | `{name:"newTask1"}` | `tasksById` is updated to:<br>`{1: {name:"task1"...}, 2: {name:"task2"...}}` |
| — | — | Normal | FR1 | `deleteTask` | Removes the task with the given id from all task storage objects. | `taskId: 1` | `{1: {name:"task1"...}, 2: {name:"task2"...}}` |
| — | — | Normal | FR1, NFR1 | `outputTasks` | Displays all tasks, separated by category. | — | Outputs a clearly segmented task list as shown in REPLACE_PLACE_NAME |taskById{standard}