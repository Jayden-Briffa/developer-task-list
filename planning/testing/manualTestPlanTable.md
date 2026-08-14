# Manual test plan
<!-- More granual as there is otherwise no documentation -->
| Test Name | Purpose | Requirements Verified |
|---|---|---|
| Main menu navigation | Verify main menu is displayed and accepts numeric and case-insensitive phrase inputs | NFR1 |
| View all tasks | Verify all stored tasks are displayed clearly with proper formatting and organization by category | FR1, FR2 |
| View task by ID | Verify task details are displayed when viewing by ID, including error handling for nonexistent IDs | FR1, FR2, NFR2 |
| View task by name | Verify task details are displayed when viewing by name, including error handling for nonexistent names | FR1, FR2, NFR2 |
| Create task (normal) | Verify user can create a task with all fields including category, with validation and confirmation prompts | FR1, FR2 |
| Create task (empty category) | Verify task can be created without a category, displaying appropriately in output | FR1, FR2 |
| Update task | Verify task fields including category can be updated with prefilled values and saved correctly | FR1, FR2 |
| Delete task | Verify task deletion with confirmation and proper state synchronization across categories | FR1, FR2 |
| Quit application | Verify application exits gracefully | NFR1 |
| Abort operation | Verify user can abort any input operation and return to main menu without crashing | NFR2 |