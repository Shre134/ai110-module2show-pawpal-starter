from dataclasses import dataclass, field
from enum import Enum


class TaskType(Enum):
    WALK = "walk"
    FEEDING = "feeding"
    MEDICATION = "medication"
    GROOMING = "grooming"
    OTHER = "other"


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Pet:
    name: str
    species: str
    age: int
    breed: str = ""

    def get_tasks(self, schedule):
        pass


@dataclass
class Task:
    title: str
    task_type: TaskType
    duration_minutes: int
    priority: Priority
    pet: Pet
    is_completed: bool = False

    def mark_complete(self):
        pass


@dataclass
class Owner:
    name: str
    email: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        pass

    def get_pets(self):
        pass


class Schedule:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        pass

    def remove_task(self, task: Task):
        pass

    def get_todays_tasks(self):
        pass