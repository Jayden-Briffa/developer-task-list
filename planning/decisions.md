# Why use an MVC split
This split is inspired by REST API where data management is a core function. It is one here too, so it is useful to totally separate the logic for state management, outputs, inputs, and general logic. This makes it easier to narrow down which function a logical error may belong to at its root. It also separates concerns in development, allowing a single part of the system be focussed on at a time.

# Why switch to automated tests
More code to maintain but offers documentation and speed
Better organisation of similar or adjacent tests

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