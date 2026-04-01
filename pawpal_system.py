from dataclasses import dataclass, field
from enum import Enum
from datetime import date, timedelta


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
    time: str = "08:00"              # format: "HH:MM"
    frequency: str = "once"          # "once", "daily", "weekly"
    is_completed: bool = False
    due_date: date = field(default_factory=date.today)

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

    def sort_by_time(self):
        """Return all tasks sorted by their scheduled time (HH:MM)."""
        return sorted(self.get_all_tasks(), key=lambda t: t.time)

    def filter_by_pet(self, pet_name: str):
        """Return tasks for a specific pet."""
        return [t for t in self.get_all_tasks() if t.pet_name == pet_name]

    def filter_by_status(self, completed: bool):
        """Return tasks filtered by completion status."""
        return [t for t in self.get_all_tasks() if t.is_completed == completed]

    def handle_recurring(self, task: Task):
        """If a completed task is recurring, create the next occurrence."""
        if task.frequency == "daily":
            new_due = task.due_date + timedelta(days=1)
        elif task.frequency == "weekly":
            new_due = task.due_date + timedelta(weeks=1)
        else:
            return None

        new_task = Task(
            title=task.title,
            task_type=task.task_type,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            pet_name=task.pet_name,
            time=task.time,
            frequency=task.frequency,
            due_date=new_due
        )
        return new_task

    def detect_conflicts(self):
        """Return a list of warning messages for tasks scheduled at the same time for the same pet."""
        tasks = self.get_all_tasks()
        warnings = []
        seen = {}
        for task in tasks:
            key = (task.pet_name, task.time)
            if key in seen:
                warnings.append(
                    f"Conflict: '{task.title}' and '{seen[key]}' are both scheduled at {task.time} for {task.pet_name}"
                )
            else:
                seen[key] = task.title
        return warnings