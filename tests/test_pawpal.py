from pawpal_system import Task, Pet, Owner, Scheduler, TaskType, Priority


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