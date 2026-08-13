# Why use an MVC split
This split is inspired by REST API where data management is a core function. It is one here too, so it is useful to totally separate the logic for state management, outputs, inputs, and general logic. This makes it easier to narrow down which function a logical error may belong to at its root. It also separates concerns in development, allowing a single part of the system be focussed on at a time.

# Why use typehints

# Docstrings used to summarise files

# Autosave

# Model
## Why change the Model method names
In the design phase, keywords like "retrieve" and "add", but these were changed to better align with widespread sql concepts like "insert" and "select" to make the limited functionality of the model clear.

Similarly, their functionalities were changed to accept a list of ids, names, or categories, rather than just one. This let them be flexible and improve the program's scalability while adhering closer to standards like SQL, where many-optional options are often preffered

## Why manage tasks indicies per-method rather than having a single synchronising method
Such a method would need to iterate over every task to reconstruct the indicies, which is much less efficient than adjusting them as-needed

## Why not store data directly in the indicies
This would duplicate data, leading to potential misalignmnet and increasing the memory requirements for the program

## Why use unsafe methods like dict[] notation instead of safe .get
The model is at the heart of the application and must therefore make any errors clear and visible. It is the job of the controller to make a good user experience, not the model.

## Why use an OOP pattern only for the model

## Why create and delete categories automatically 
This better maintains separation of concerns than a separate method as category management isn't necessary outside of specific processes like adding, updating, or deleting tasks. This means it is tightly coupled to the rest of the state

## Why note changes as TODOs instead of applying them immidiately
This ensures that the change is applied before release but prevents unnnecessary task switching which would disrupt flow.

# User interface
## Why transform all inputs
Making inputs consistently case-insensitive and ignore whitespace reduces user frustration when small, potentially invisble input errors are made. 

## Used prompt_toolkit.prompt for inputs
This provides a lightweight way to extend input functionality to allow placeholder text, improving the UX of updating a task by allowing users to simply alter values rather than typing them out in full

# Validations
## Validators can return Task or None for success
This allows us to reuse code and improve flexibility while removing unnecessary repetition of database reads, which could easily bottleneck the system. I considered moving some of the "get task" logic into controllers instead, but this would violate separation of concerns.

# Controllers
## deleteTask forces a very specific confirmation phrase
As this is a very destructive action, it is important to give the user multiple chances to back out if they missclicked or changed they mind. 

## getConfirmedTaskCategory is not a validator
Despite being similar to a validation in that there is a value being confirmed being moving on, this is more about controlling the flow of the program and the user's choice than ensuring the inputs are valid.


# Testing
## Why create the userInputs/expectedTask constructor
WIP
Chose to separate construction of userInputs/expectedTask and the execution. This quickly became useful as I needed to change only the latter for the updateTask tests

## Why switch to automated tests
More code to maintain but offers documentation and speed
Better organisation of similar or adjacent tests
Automates regression tests
Made time feel more restrictive

## Only make controller return != None when testing

## Making assertion template functions
This keeps code DRY but obscures the reason for failed assertions. Needed to manually apply error messages to report expected and actual outcomes on failure

# UI
## Press enter to continue
pressEnterToContinue() is called after important outputs which could otherwise get lost in fast-moving text. This breaks flow when outputting errors, which is important to show the user the ussue, or maintains flow when reading large outputs like all tasks sorted by