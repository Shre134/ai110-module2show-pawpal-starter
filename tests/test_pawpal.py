from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler, TaskType, Priority


# --- Helpers ---

def make_owner_with_pets():
    owner = Owner(name="Jordan", email="jordan@email.com")
    dog = Pet(name="Mochi", species="dog", age=3)
    cat = Pet(name="Luna", species="cat", age=5)
    owner.add_pet(dog)
    owner.add_pet(cat)
    return owner, dog, cat


# --- Happy path tests ---

def test_mark_complete():
    """Task should be marked complete after calling mark_complete()."""
    task = Task("Walk", TaskType.WALK, 30, Priority.HIGH, "Mochi")
    task.mark_complete()
    assert task.is_completed == True


def test_add_task_increases_count():
    """Adding a task to a pet should increase their task count."""
    pet = Pet(name="Mochi", species="dog", age=3)
    task = Task("Feed", TaskType.FEEDING, 10, Priority.MEDIUM, "Mochi")
    pet.add_task(task)
    assert len(pet.get_tasks()) == 1


def test_sort_by_time():
    """Tasks should be returned in chronological order."""
    owner, dog, _ = make_owner_with_pets()
    dog.add_task(Task("Evening walk", TaskType.WALK, 30, Priority.LOW, "Mochi", time="18:00"))
    dog.add_task(Task("Morning walk", TaskType.WALK, 30, Priority.HIGH, "Mochi", time="07:00"))
    dog.add_task(Task("Midday feed", TaskType.FEEDING, 10, Priority.MEDIUM, "Mochi", time="12:00"))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for t in sorted_tasks]
    assert times == sorted(times)


def test_conflict_detection():
    """Scheduler should flag two tasks at the same time for the same pet."""
    owner, dog, _ = make_owner_with_pets()
    dog.add_task(Task("Morning walk", TaskType.WALK, 30, Priority.HIGH, "Mochi", time="07:00"))
    dog.add_task(Task("Medication", TaskType.MEDICATION, 5, Priority.HIGH, "Mochi", time="07:00"))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) > 0


def test_recurring_daily_creates_next_task():
    """A daily task should generate a new task due the following day."""
    task = Task(
        "Feed breakfast", TaskType.FEEDING, 10, Priority.HIGH, "Mochi",
        frequency="daily", due_date=date.today()
    )
    owner = Owner(name="Jordan", email="jordan@email.com")
    dog = Pet(name="Mochi", species="dog", age=3)
    dog.add_task(task)
    owner.add_pet(dog)

    scheduler = Scheduler(owner)
    next_task = scheduler.handle_recurring(task)
    assert next_task.due_date == date.today() + timedelta(days=1)


# --- Edge case tests ---

def test_pet_with_no_tasks():
    """A pet with no tasks should return an empty list."""
    pet = Pet(name="Mochi", species="dog", age=3)
    assert pet.get_tasks() == []


def test_no_conflicts_different_times():
    """Tasks at different times should not produce conflicts."""
    owner, dog, _ = make_owner_with_pets()
    dog.add_task(Task("Morning walk", TaskType.WALK, 30, Priority.HIGH, "Mochi", time="07:00"))
    dog.add_task(Task("Evening walk", TaskType.WALK, 30, Priority.LOW, "Mochi", time="18:00"))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 0