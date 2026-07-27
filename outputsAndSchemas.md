# Outputs
## Menu output
```
=== Menu title ===
1. Option 1
2. Option 2

Enter your choice:
```

## Tasks by category
```
--- Category name ---
. Task 1- <description> @ <dd/mm/yyyy>
. Task 2- <description> @ <dd/mm/yyyy>

--- Other category ---
. Task 1- <description> @ <dd/mm/yyyy>
. Task 2- <description> @ <dd/mm/yyyy>

```

# Schemas
## Task
| name | description | type | constraints | required/optional |
| --- | --- | --- | --- | --- |
| id | Persistent unique identifier for each task | integer | | required |
| name | User-friendly summary of task | string | 2 < len() < 24 | required |
| description | Full task details | string | len() < 255 | optional | 
| deadline | When the task should be completed by | string | Can be converted to Date("dd:mm:yyyy") | optional |

