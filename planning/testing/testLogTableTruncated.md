> Note: test whose id include an "m", e.g., "9m1" are manual tests zooming in on specific unit tests. Manual tests with a letter, e.g., "20a" are repeats of the previous test.

# Automated tests
| Test # | Suite name | Status | Actions |
| --- | --- | --- | --- |
| 1 | testModel | Failed | Added dict -> Task translation to loadTasks |
| 2 | test_taskModel | Failed | Treat ids as strings rather than integers |
| 3 | test_taskModel | Failed | Update dummyModel definition to update lastInsertId |
| 4 | test_taskModel | Passed | |
| 5 | test_controllers | Failed (3 passed) | Made datetime formatting conditional on a non-empty input in validateTaskDeadline |
| 6 | test_controllers | Failed (3 passed) | |
| 7 | test_controllers | Failed (3 passed) | Use safer .get() function to prevent always finding a keyError |
| 8 | test_controllers | Failed (6 passed) | Make validateExistingTaskName return the found task on success |
| 9 | test_controllers | Failed (7 passed) | Place id in a list for update tests. Continue with manual testing |
| 9m1 | Update task (normal) | Failed | Cast i as str before comparing to task id |
| 9m2 | Update task (normal) | Failed | Add autosave to controllers. Add return statement to model.updateTask |
| 9m3 | Update task (normal) | Passed | |
| 10 | test_controllers | Failed (10 passed) | Add a "yes" input to category input lists where it is a new name |
| 11 | test_controllers | Failed (10 passed) | Use manual testing |
| 11m1 | Create task (minimum fields) | Failed | Only perform length validation if the field is given |
| 11m2 | Create task (minimum fields) | Passed | |
| 12 | test_controllers | Failed (10 passed) | Place failed condition path in an else statement |
| 13 | test_controllers | Failed (16 passed) | Adjust maximum value in validateTaskDescription to be 255 rather than 256 |
| 14 | test_controllers | Failed (18 passed) | Use manual testing |
| 14m1 | Create task (dont confirm category) | Failed | Encase category selection logic in a while loop that breaks on confirmation. Update dontConfirmCategory tests to input different category names |
| 14m2 | Create task (dont confirm category) | Failed | Add additional else:break clause to break if the category already exists |
| 14m3 | Create task (dont confirm category) | Passed | |
| 15 | test_controllers | Failed (18 passed) | Add "yes" as the final category input in testUpdateTaskExtremeLower |
| 16 | test_controllers | Passed | |
| 17 | test_performance | Passed | Stress test to find a bottleneck |
| 18 | test_performance | Forced to fail | | 

# Manual UI tests
| Test # | Core function | Expected result | Actual result | Actions |
| --- | --- | --- | --- | --- |
| 19 | Main menu | Main menu is outputted clearly and accepts inputs of numbers and case-insensitive full phrases | Passed | |
| 20 | View all tasks | All currently-stored tasks are outputted clearly with truncated fields shown | Tasks are outputted, but the output is lost among the quickly-moving text. | Add padding to outputs and ask the user to press enter to continue |
| 21 | View all tasks | All currently-stored tasks are outputted clearly with truncated fields shown | Passed | |
| 22 | View task by id | All task fields are outputted untruncated, clearly | All fields other than category are shown | Add category "subheading" area to task output |
| 23 | View task by id | All task fields are outputted untruncated, clearly | Passed | |
| 24 | View task by id (nonexistent id) | User is informed that the id should exist and is asked to re-enter the id | KeyError: '15'  is thrown | Replace dict[] syntax with safer .get in model.selectTaskByIds |
| 25 | View task by id (nonexistent id) | User is informed that the id should exist and is asked to re-enter the id | Passed | |
| 26 | View task by name | All task fields are outputted untruncated, clearly | Passed | |
| 27 | View task by name (nonexistent name) | User is informed that the name should exist and is asked to re-enter the name | KeyError: 'srvd' is thrown | Apply safe .get() dict retrieval for selectTaskByNames |
| 28 | View task by name (nonexistent name) | User is informed that the name should exist and is asked to re-enter the name | Passed | |
| 29 | Create a new task | User is clearly prompted for each field, with invalid inputs being met by errors and prompts to retry | Invalid date inputs lead to "ValueError: time data 'invalidValue' does not match format '%d/%m/%Y'" beign thrown | Turn date validation into a try-catch block to stop errors from propogating |
| 30 | Create a new task | User is clearly prompted for each field, with invalid inputs being met by errors and prompts to retry | Date field allows the user to retry invalid inputs. However, action confirmation prompts are vague as they only say that 'yes' will be accepted (no surrounding context for what you're agreeing to) | Add context to confirmations |
| 31 | Create a new task | User is clearly prompted for each field, with invalid inputs being met by errors and prompts to retry | Passed | |
| 32 | Create a new task (empty category) | The task category remains empty in state, but output should display "<no output>" for category | The category simply remains empty | Do not overwrite category in the controller. Replace empty category with "<no output>" only at output time |
| 33 | Create a new task (empty category) | The task category remains empty in state, but output should display "<no output>" for category | Passed | |
| 34 | Update task | Task fields are prefilled with existing values and new task values are outputted clearly afterwards | Passed | |
| 35 | Delete task | Selected task is clearly outputted alongside a warning of permenance and user must confirm wanting to delete it with 'yes' | Warning and task output is present, but the following is thrown after confirmation: KeyError: 'newcategory'. This suggested that the newly-created category wasn't synchronised into taskIdsByCategory. This was confirmed by model code and extended to taskIdsByName | Synchronise taskIds indicies when updating tasks |
| 36 | Delete task | Selected task is clearly outputted alongside a warning of permenance and user must confirm wanting to delete it with 'yes' | Passed | |
| 37 | Update task | Category always seems to show as empty despite not being empty | Add default param to getConfirmedTaskCategory | |
| 38 | Update task | Category always seems to show as empty despite not being empty | Passed | |
| 39 | Quit | Exits program | Passed | |
| 40 | Abort operation | Inputting "abort" at any input sends the user back to the main menu | Passed | |