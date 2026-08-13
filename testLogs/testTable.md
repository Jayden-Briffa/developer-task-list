# Unit & integration Tests by Suite

## test_taskModel.py - Model Storage Tests

| Test # | Test Function | Test type | Requirement links | Description | Inputs | Expected results |
|---|---|---|---|---|---|---|
| 1 | [testSaveTasks](src/tests/test_taskModel.py) | Normal | FR3 | Accurately overwrites `tasks.json` with data from `tasksById`. | `tasksById = {Task(id="1", name="Task1", ...), Task(id="2", name="Task2", ...)}` | File `tasks.json` contains all task data in correct JSON format with matching ids. |
| 2 | [testLoadTasks](src/tests/test_taskModel.py) | Normal | FR3 | Accurately retrieves data from `tasks.json` and reconstructs all task storage objects (`tasksById`, `taskIdsByName`, `taskIdsByCategory`). | — | `tasksById` contains all tasks from file; `taskIdsByName` maps names to correct ids; `taskIdsByCategory` maps categories to correct id lists. |
| 3 | [testInsertTask](src/tests/test_taskModel.py) | Normal | FR1, FR2 | Adds a new task with given information to all task storage objects with auto-incremented id. | `name="task4"`, `description="mydescription4"`, `deadline="30/11/2026"`, `category="category2"`, `status="Testing"` | Task is added to `tasksById` with id "4"; `taskIdsByName` includes the new name mapped to "4"; `taskIdsByCategory["category2"]` includes "4". |
| 4 | [testSelectTasks<br>ByIds](src/tests/test_taskModel.py) | Normal | FR1, FR2 | Retrieves tasks by their ids from storage. | `ids=["1", "2"]` | Returns dict with both tasks; task ids and all fields match stored data. |
| 5 | [testSelectTasks<br>ByCategory](src/tests/test_taskModel.py) | Normal | FR1, FR2 | Retrieves all tasks in a given category from storage. | `categories=["category2"]` | Returns dict with key "category2" containing all tasks with ids ["2", "3"]. |
| 6 | [testSelectTasks<br>ByNames](src/tests/test_taskModel.py) | Normal | FR1, FR2 | Retrieves tasks by their names from storage (case-insensitive). | `names=["task1", "task2"]` | Returns dict with both tasks matching given names. |
| 7 | [testUpdateTask](src/tests/test_taskModel.py) | Normal | FR1, FR2 | Replaces task information and updates all index mappings (`taskIdsByName`, `taskIdsByCategory`). | `taskId="2"`, `name="newTask2"`, `description="myNewDescription"`, `deadline="30/10/2026"`, `category="category1"`, `status="Completed"` | `tasksById["2"]` contains new values; `taskIdsByName` maps new name to "2" and removes old name; `taskIdsByCategory` moves id "2" to new category. |
| 8 | [testDeleteTask](src/tests/test_taskModel.py) | Normal | FR1, FR2 | Removes task from all storage objects and updates indexes. | `taskId="2"` | Task is removed from `tasksById`; removed from `taskIdsByName` mapping; removed from `taskIdsByCategory` (category key deleted if empty). |

## test_controllers.py - Controller View Tests

| Test # | Test Function | Test type | Requirement links | Description | Inputs | Expected results |
|---|---|---|---|---|---|---|
| 9 | [testViewAll<br>TasksByCategory](src/tests/test_controllers.py) | Integration | FR1, FR2 | Controller retrieves and outputs all tasks organized by category. | — | Returns dict with all categories present; each category contains correct task objects with matching ids. |
| 10 | [testViewTask<br>ById](src/tests/test_controllers.py) | Integration | FR1 | Controller retrieves and outputs a single task by user-entered id. | `userInput="1"` | Returns correct task object; task id and all fields match stored data. |
| 11 | [testViewTask<br>ByName](src/tests/test_controllers.py) | Integration | FR1 | Controller retrieves and outputs a single task by user-entered name (case-insensitive). | `userInput="TaSk1"` | Returns correct task object matching the name despite case difference. |

## test_controllers.py - Controller Create Task Tests

| Test # | Test Function | Test type | Requirement links | Description | Inputs | Expected results |
|---|---|---|---|---|---|---|
| 12 | [testCreateTask<br>Normal](src/tests/test_controllers.py) | Integration | FR1, FR2 | Creates a new task with standard valid inputs and adds to model. | `name="Task4"`, `description="Description4"`, `deadline="01/01/2026"`, `category="Category1"`, `status="3"` | New task created with id "4"; added to all storage objects; controller outputs the new task. |
| 13 | [testCreateTask<br>ExtremeLower](src/tests/test_controllers.py) | Boundary (lower) | FR1, FR2, NFR1 | Creates task with minimal valid data and confirms new category. | `name="AaA"`, `description=""`, `deadline=""`, `category="AaA"`, `status="0"` | New task created with id "4"; user sees confirmation prompt for new category; task added with new category. |
| 14 | [testCreateTask<br>ExtremeUpper](src/tests/test_controllers.py) | Boundary (upper) | FR1, FR2 | Creates task with maximal but valid data. | `name="A"*32`, `description="A"*255`, `deadline="01/01/2026"`, `category="Category1"`, `status="Completed"` | New task created with id "4"; all fields stored correctly; task added to all indexes. |
| 15 | [testCreateTask<br>MinimumFields](src/tests/test_controllers.py) | Boundary (lower) | FR1, FR2, NFR1 | Creates task with only required fields (empty optional fields allowed). | `name="TaskNameAa"`, `description=""`, `deadline=""`, `category=""`, `status="2"` | New task created with id "4"; optional fields remain empty; category not required for task creation. |
| 16 | [testCreateTask<br>ExtremeLowerInvalid](src/tests/test_controllers.py) | Invalid / Boundary (lower) | NFR1, NFR2 | Rejects minimal invalid inputs and prompts retry for each field. | `name="Aa"` (too short), `deadline="invalid"`, `category="Aa"`, `status="4"` (out of range) | Error messages output for each field. User can retry inputs. |
| 17 | [testCreateTask<br>ExtremeUpperInvalid](src/tests/test_controllers.py) | Invalid / Boundary (upper) | NFR1, NFR2 | Rejects maximal invalid inputs and prompts retry for each field. | `name="A"*33`, `description="A"*256`, `category="a"*17` | Error messages output: name 3-32 chars, description max 255 chars, category 3-16 chars. User can retry. |
| 18 | [testCreateTask<br>DuplicateName](src/tests/test_controllers.py) | Invalid | NFR1, NFR2 | Prevents duplicate task names and prompts user to choose a different name. | `name="Task1"` (already exists), then `name="Task4"` | Error message: name already exists. User prompted to retry. After retry with unique name, task created. |
| 19 | [testCreateTask<br>DontConfirmCategory](src/tests/test_controllers.py) | Integration | FR1, FR2, NFR1 | Rejects new category, allows user to retry with different category, then confirms. | `category=["AaAaA", "no", "AaAaAa", "yes"]` | User sees confirmation for "AaAaA"; enters "no"; returned to category prompt; enters "AaAaAa"; confirms with "yes"; task created. |

## test_controllers.py - Controller Update Task Tests

| Test # | Test Function | Test type | Requirement links | Description | Inputs | Expected results |
|---|---|---|---|---|---|---|
| 20 | [testUpdateTask<br>Normal](src/tests/test_controllers.py) | Integration | FR1, FR2 | Updates task with standard valid inputs. Task id selected first, then fields prefilled with current values. | `taskId="3"`, `name="Task3"`, `description="Description3"`, `deadline="01/01/2026"`, `category="Category1"`, `status="3"` | Task id "3" updated with new values; all storage indexes updated correctly; new task data output. |
| 21 | [testUpdateTask<br>ExtremeLower](src/tests/test_controllers.py) | Boundary (lower) | FR1, FR2, NFR1 | Updates task with minimal but valid data and confirms new category. | `taskId="3"`, `name="AaA"`, `description=""`, `deadline=""`, `category="AaA"`, `status="0"` | Task updated; user sees confirmation for new category; task moved to new category; indexes synchronized. |
| 22 | [testUpdateTask<br>ExtremeUpper](src/tests/test_controllers.py) | Boundary (upper) | FR1, FR2 | Updates task with maximal but valid data. | `taskId="3"`, `name="A"*32`, `description="A"*255`, `deadline="01/01/2026"`, `category="Category1"`, `status="Completed"` | Task updated with all max-length fields; indexes updated; data stored correctly. |
| 23 | [testUpdateTask<br>MinimumFields](src/tests/test_controllers.py) | Boundary (lower) | FR1, FR2, NFR1 | Updates task with only required fields (empty optional fields allowed). | `taskId="3"`, `name="TaskNameAa"`, `description=""`, `deadline=""`, `category=""`, `status="2"` | Task updated with minimal data; optional fields remain empty; category can be empty without confirmation. |
| 24 | [testUpdateTask<br>ExtremeLowerInvalid](src/tests/test_controllers.py) | Invalid / Boundary (lower) | NFR1, NFR2 | Rejects minimal invalid inputs and allows retry. | `taskId="3"`, `name="Aa"`, `deadline="invalid"`, `category="Aa"` | Error messages displayed for each invalid field. State unchanged. User prompted to retry. |
| 25 | [testUpdateTask<br>ExtremeUpperInvalid](src/tests/test_controllers.py) | Invalid / Boundary (upper) | NFR1, NFR2 | Rejects maximal invalid inputs and allows retry. | `taskId="3"`, `name="A"*33`, `description="A"*256`, `category="a"*17` | Error messages displayed. State unchanged. User can retry. |
| 26 | [testUpdateTask<br>DontConfirmCategory](src/tests/test_controllers.py) | Integration | FR1, FR2, NFR1 | Rejects new category, allows user to retry with different category, then confirms. | `taskId="3"`, `category=["AaAaA", "no", "AaAaAa", "yes"]` | User sees confirmation for "AaAaA"; enters "no"; returned to category prompt; enters "AaAaAa"; confirms with "yes"; task updated. |

## test_controllers.py - Controller Delete Task Tests

| Test # | Test Function | Test type | Requirement links | Description | Inputs | Expected results |
|---|---|---|---|---|---|---|
| 27 | [testDeleteTask](src/tests/test_controllers.py) | Integration | FR1, NFR1 | Deletes task after user confirms. Shows task details and permanence warning. | `taskId="3"`, `confirmation="yes"` | Task output displayed with warning message. User enters "yes" to confirm. Task removed from all storage objects and indexes. |
| 28 | [testDeleteTask<br>DontConfirm](src/tests/test_controllers.py) | Integration | FR1, NFR1 | Cancels deletion if user does not confirm. | `taskId="3"`, `confirmation="no"` | Task output displayed. User enters "no". Task remains in all storage objects unchanged. |

## test_performance.py - Performance Tests (1000 tasks across 20 categories, average value of repeated 5 times)

| Test # | Test Function | Test type | Requirement links | Description | Inputs | Expected results |
|---|---|---|---|---|---|---|
| 29 | [testSaveTasks<br>LargeDatasetUnderHalfSecond](src/tests/test_performance.py) | Extreme | NFR3 | Saves large dataset with 1000 tasks to file within time limit. | Pre-populated storage with 1000 tasks (50 per category across 20 categories) | Task completion time averaged over 5 runs is <= 0.5s. File written correctly with all data. |
| 30 | [testSelectTasks<br>ByIdsLargeDatasetUnderHalfSecond](src/tests/test_performance.py) | Extreme | NFR3 | Retrieves all 1000 tasks by id efficiently. | `ids=["1", "2", ..., "1000"]` (all task ids) | All tasks retrieved correctly; average execution time over 5 runs is <= 0.5s. |
| 31 | [testSelectTasks<br>ByCategoriesLargeDatasetUnderHalfSecond](src/tests/test_performance.py) | Extreme | NFR3 | Retrieves all tasks from all 20 categories efficiently. | `categories=["category0", "category1", ..., "category19"]` | All tasks grouped by category correctly; average execution time over 5 runs is <= 0.5s. |
| 32 | [testSelectTasks<br>ByNamesLargeDatasetUnderHalfSecond](src/tests/test_performance.py) | Extreme | NFR3 | Retrieves all 1000 tasks by name efficiently. | `names=["task1", "task2", ..., "task1000"]` | All 1000 tasks retrieved; average execution time over 5 runs is <= 0.5s. |
| 33 | [testInsertTask<br>LargeDatasetUnderHalfSecond](src/tests/test_performance.py) | Extreme | NFR3 | Inserts new task into large dataset efficiently. | Insert `name="task1001"`, `category="category0"` into 1000-task model | New task added to all storage objects; average execution time over 5 runs is <= 0.5s. |
| 34 | [testUpdateTask<br>LargeDatasetUnderHalfSecond](src/tests/test_performance.py) | Extreme | NFR3 | Updates a task in large dataset efficiently. | Update task id "500": `name="updatedTask500"`, `category="category7"` in 1000-task model | Task updated; all indexes synchronized; average execution time over 5 runs is <= 0.5s. |
| 35 | [testDeleteTask<br>LargeDatasetUnderHalfSecond](src/tests/test_performance.py) | Extreme | NFR3 | Deletes a task from large dataset efficiently. | Delete task id "1" from 1000-task model | Task removed from all storage objects and indexes; average execution time over 5 runs is <= 0.5s. |
| 36 | [testLoadTasks<br>LargeDatasetUnderHalfSecond](src/tests/test_performance.py) | Extreme | NFR3 | Loads large dataset from file efficiently. | Load 1000-task JSON file | All tasks loaded; all indexes rebuilt; average execution time over 5 runs is <= 0.5s. |
