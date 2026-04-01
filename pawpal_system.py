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
class Task:
    """Represents a single pet care activity."""
    title: str
    task_type: TaskType
    duration_minutes: int
    priority: Priority
    pet_name: str
    is_completed: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        self.is_completed = True


@dataclass
class Pet:
    """Stores pet details and their list of tasks."""
    name: str
    species: str
    age: int
    breed: str = ""
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet."""
        self.tasks.append(task)

    def get_tasks(self):
        """Return all tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""
    name: str
    email: str
    available_minutes: int = 120
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Return all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Retrieves, organizes, and manages tasks across all of an owner's pets."""

    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def get_all_tasks(self):
        """Get all tasks from all pets."""
        return self.owner.get_all_tasks()

    def get_todays_schedule(self):
        """Return tasks sorted by priority (high to low)."""
        tasks = self.get_all_tasks()
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda t: priority_order[t.priority.value])

    def get_pending_tasks(self):
        """Return only tasks that are not completed."""
        return [t for t in self.get_all_tasks() if not t.is_completed]