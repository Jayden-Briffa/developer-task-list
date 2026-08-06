class Task:
    id: int
    name: str
    description: str
    deadline: str
    category: str

    def __init__(
        self, id: int, name: str, description: str, deadline: str, category: str
    ):
        self.id = (id,)
        self.name = (name,)
        self.description = (description,)
        self.deadline = (deadline,)
        self.category = (category,)
