from Task import Task


def assertTaskHasSameValues(actualTask: Task, expectedTask: dict):
    assert actualTask.id == expectedTask["id"]
    assert actualTask.name == expectedTask["name"]
    assert actualTask.description == expectedTask["description"]
    assert actualTask.deadline == expectedTask["deadline"]
    assert actualTask.category == expectedTask["category"]
