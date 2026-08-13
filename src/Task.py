class Task:
    id: str
    name: str
    description: str
    deadline: str
    category: str
    status: str

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        deadline: str,
        category: str,
        status: str = "Not started",
    ):
        self.id = str(id)
        self.name = name
        self.description = description
        self.deadline = deadline
        self.category = category
        self.status = status
