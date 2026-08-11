class Task:
    id: str
    name: str
    description: str
    deadline: str
    category: str

    def __init__(
        self, id: str, name: str, description: str, deadline: str, category: str
    ):
        self.id = str(id)
        self.name = name
        self.description = description
        self.deadline = deadline
        self.category = category


# TODO: Add status property
