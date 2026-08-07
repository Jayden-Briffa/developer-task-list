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


# if __name__ == "__main__":
#     print({
#         1: Task(1, "name1", "desc1", "dead1", "cat1").__dict__,
#         2: Task(2, "name2", "desc2", "dead2", "cat2").__dict__,
#     }.__dict__)