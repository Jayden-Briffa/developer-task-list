# Automated tests
| Test # | Suite name | Status | Investigation & issue found | Actions | Evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | testModel | Failed | All tests found an AttributeError: 'dict' object has no attribute 'tasksById'. This indicates that something is going wrong in the model's initialisation. Noticed that this would apply to saving too, so the Task's __dict__ attribute is called when dumping to json | Added dict -> Task translation to loadTasks | ![alt text](img/dictTaskTranslation.png) |
| 2 | test_taskModel | Failed | Most tests found a "KeyError: 1" or similar, referring to the id | Treat ids as strings rather than integers |  |
| 3 | test_taskModel | Failed | testInsertTask found "KeyError: '4'" when reading from self._tasksById. Print debugging found that the new task's id wa incorrectly being set to 1 rather than 4 | Update dummyModel definition to update lastInsertId | ![alt text](img/debuggingTest.png) ![alt text](img/fixingTest.png)
| 4 | test_taskModel | Passed | | | | |
| 5 | test_controllers | Failed (3 passed) | Many tests found a "ValueError: time data '' does not match format '%d/%m/%Y'". Error message indicates that this only happens with empty inputs, which should be allowed for this input. Grep for formatting in files showed it was in validateTaskDeadline | Made datetime formatting conditional on a non-empty input in validateTaskDeadline | ![alt text](img/grepDeadlineFormatting.png)|
| 6 | test_controllers | Failed (3 passed) | Many tests found a "AttributeError: 'function' object has no attribute 'keys'". Searching for message in logs revealed incorrect syntax where a model method was being treated as its return value | | | ![alt text](img/invalidMethodHandling.png) |
| 7 | test_controllers | Failed (3 passed) | Many tests found a "KeyError: 'category1'". The error happened in model.selectTasksByCategories when the category was not yet discovered in tasksById | Use safer .get() function to prevent always finding a keyError | Controllers (L58) Before: ```if not categorised[task.category]:```, After: ```if not categorised.get(task.category):``` |
| 8 | test_controllers | Failed (6 passed) | Update task, create task and viewTaskByName tests sometimes failed with "Expected a task object, but actual was None.". Investigation into the function responsible for governing retrieval, validateExistingTaskName, found that it returned None on success, compared to validateExistingTaskId, which returns its value | Make validateExistingTaskName return the found task on success | |
| 9 | test_controllers | Failed (7 passed) | Update task and create task tests sometimes failed with "Expected a task object, but actual was None.". Error logs showed that the assertion was from assertTaskHasSameValues. Other tests using that helper worked, so it was the controllers.py or test_controllers.py logic. WB investigation found update tests mistakenly did not include the id in userInputs | Place id in a list for update tests. Continue with manual testing | |
| 9m1 | Update task (normal) | Failed | Recieved invalid menu input error on main menu | Cast i as str before comparing to task id | ![alt text](img/variablesShowingInconsistentTyping.png) | 
| 9m2 | Update task (normal) | Failed | Data wasn't saved and the task wasn't outtputed. Noticed that tasks were never saved. Tracing return values showed that model.updateTask does not return the new task as would usually be expected | Add autosave to controllers. Add return statement to model.updateTask | |
| 9m3 | Update task (normal) | Passed | Data was passed to json store and new task information was printed to the screen | | |
| 10 | test_controllers | Failed (10 passed) | userInputs ran out of inputs, suggesting that validation incorrectly failed. Noticed that it would be creating a new category and would require confirmation | Add a "yes" input to category input lists where it is a new name | |
| 11 | test_controllers | Failed (10 passed) | userInputs ran out of inputs, suggesting that validation incorrectly failed | Use manual testing | | 
| 11m1 | Create task (minimum fields) | Failed | When creating the category, it did not allow me to leave the task uncategorised | Only perform length validation if the field is given | |
| 11m2 | Create task (minimum fields) | Passed | | | |
| 12 | test_controllers | Failed (10 passed) | Many tests found "AssertionError: Task mismatch:". This was accompanied by an expected task where category="yes". Examining the code found that the protection from using confirmations as values was overwritten after the conditional statement. | Place failed condition path in an else statement | ![alt text](img/adjustedConditionBefore.png) ![alt text](img/adjustedConditionAfter.png)
| 13 | test_controllers | Failed (16 passed) | 2 "extremeUpper" tests found "ValueError: time data 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa...", indicating that some inputs were passed incorrectly by tests. Examining the tests, inputs and handling is accurate, indicating that validation is allowing too-long description values through | Adjust maximum value in validateTaskDescription to be 255 rather than 256 | |
| 14 | test_controllers | Failed (18 passed) | No task was returned by testCreateTaskDontConfirmCategory. White box examination revealed no obvious input faults | Use manual testing | |
| 14m1 | Create task (dont confirm category) | Failed | The user is sent straight back to the main menu, instead of being allowed to change the category they want to enter. White box examination showed that controllers.createTask simply returned on non confirmation. I questioned why this wasn't also an issue in updateTask. Upon examination, I noticed that it doesn't have any confirmation logic at all | Encase category selection logic in a while loop that breaks on confirmation. Update dontConfirmCategory tests to input different category names | ![alt text](img/newWhileLoopInCategorySelection.png)|
| 14m2 | Create task (dont confirm category) | Failed | The user is, as expected, asked to repeat their input when not confirming. However, existing categories now ask the user for a category forever | Add additional else:break clause to break if the category already exists | |
| 14m3 | Create task (dont confirm category) | Passed | The user is, as expected, asked to repeat their input when not confirming and existing categories no longer loop forever | | |
| 15 | test_controllers | Failed (18 passed) | Update task with lower extreme inputs prematurely exhausts its inputs. As this only started failing after the last change, it is likely due to the new category selection logic. As controllers.updateTask did not previously confirm category selections at all, indicating that the test may not have a confirmation input. This was correct | Add "yes" as the final category input in testUpdateTaskExtremeLower | |
| 16 | test_controllers | Passed | | | |
| 17 | test_performance | Passed | All key actions executed on average under 0.5s | Stress test to find a bottleneck | |
| 18 | test_performance | Forced to fail | Stress-tested performance by gradually adding tasks. First failure was between 70k-80k tasks and was only failed by saveTasks. This is a totally unrealistic number of tasks for a single developer, but could highlight a potential future bottleneck | | | 

# Manual UI tests
| Test # | Core function | Expected result | Actual result | Actions | Evidence |
| --- | --- | --- | --- | --- | --- |
| 19 | Main menu | Main menu is outputted clearly and accepts inputs of numbers and case-insensitive full phrases | Passed | |
| 20 | View all tasks | All currently-stored tasks are outputted clearly with truncated fields shown | Tasks are outputted, but the output is lost among the quickly-moving text. | Add padding to outputs and ask the user to press enter to continue | |
| 20a | View all tasks | All currently-stored tasks are outputted clearly with truncated fields shown | Passed | | |
| 21 | View task by id | All task fields are outputted untruncated, clearly | All fields other than category are shown | Add category "subheading" area to task output | |
| 21a | View task by id | All task fields are outputted untruncated, clearly | Passed | | | 
| 22 | View task by id (nonexistent id) | User is informed that the id should exist and is asked to re-enter the id | KeyError: '15'  is thrown | Replace dict[] syntax with safer .get in model.selectTaskByIds | |
| 22a | View task by id (nonexistent id) | User is informed that the id should exist and is asked to re-enter the id | Passed | | |
| 23 | View task by name | All task fields are outputted untruncated, clearly | Passed | | |
| 24 | View task by name (nonexistent name) | User is informed that the name should exist and is asked to re-enter the name | KeyError: 'srvd' is thrown | Apply safe .get() dict retrieval for selectTaskByNames | |
| 24a | View task by name (nonexistent name) | User is informed that the name should exist and is asked to re-enter the name | Passed | | |
| 25 | Create a new task | User is clearly prompted for each field, with invalid inputs being met by errors and prompts to retry | Invalid date inputs lead to "ValueError: time data 'invalidValue' does not match format '%d/%m/%Y'" beign thrown | Turn date validation into a try-catch block to stop errors from propogating | | |
| 25a | Create a new task | User is clearly prompted for each field, with invalid inputs being met by errors and prompts to retry | Date field allows the user to retry invalid inputs. However, action confirmation prompts are vague as they only say that 'yes' will be accepted (no surrounding context for what you're agreeing to) | Add context to confirmations | |
| 25a | Create a new task | User is clearly prompted for each field, with invalid inputs being met by errors and prompts to retry | Passed | | |
| 26 | Create a new task (empty category) | The task category remains empty in state, but output should display "<no output>" for category | The category simply remains empty | Do not overwrite category in the controller. Replace empty category with "<no output>" only at output time | | 
| 26a | Create a new task (empty category) | The task category remains empty in state, but output should display "<no output>" for category | Passed | | 
| 27 | Update task | Task fields are prefilled with existing values and new task values are outputted clearly afterwards | Passed | | |
| 28 | Delete task | Selected task is clearly outputted alongside a warning of permenance and user must confirm wanting to delete it with 'yes' | Warning and task output is present, but the following is thrown after confirmation: KeyError: 'newcategory'. This suggested that the newly-created category wasn't synchronised into taskIdsByCategory. This was confirmed by model code and extended to taskIdsByName | Synchronise taskIds indicies when updating tasks | |
| 28a | Delete task | Selected task is clearly outputted alongside a warning of permenance and user must confirm wanting to delete it with 'yes' | Passed | | |
| 29 | Update task | Category always seems to show as empty despite not being empty | Add default param to getConfirmedTaskCategory | | |
| 29a | Update task | Category always seems to show as empty despite not being empty | Passed | | |
| 30 | Quit | Exits program | Passed | | |
| 31 | Abort operation | Inputting "abort" at any input sends the user back to the main menu | Passed | | |

# Lessons
| Test # | Lesson |
| --- | --- |
| 1 | Make sure to think about how your custom classes will interact with other packages |