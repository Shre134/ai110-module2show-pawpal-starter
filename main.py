from pawpal_system import Task, Pet, Owner, Scheduler, TaskType, Priority

# Create owner
owner = Owner(name="Jordan", email="jordan@email.com", available_minutes=120)

# Create pets
dog = Pet(name="Mochi", species="dog", age=3)
cat = Pet(name="Luna", species="cat", age=5)

# Add tasks to dog
dog.add_task(Task("Morning walk", TaskType.WALK, 30, Priority.HIGH, "Mochi"))
dog.add_task(Task("Feed breakfast", TaskType.FEEDING, 10, Priority.HIGH, "Mochi"))

# Add task to cat
cat.add_task(Task("Playtime", TaskType.OTHER, 20, Priority.MEDIUM, "Luna"))

# Register pets
owner.add_pet(dog)
owner.add_pet(cat)

# Run scheduler
scheduler = Scheduler(owner)
schedule = scheduler.get_todays_schedule()

# Print schedule
print("\n Today's Schedule for", owner.name)
print("-" * 35)
for task in schedule:
    status = "✓" if task.is_completed else "○"
    print(f"{status} [{task.priority.value.upper()}] {task.title} ({task.duration_minutes} min) — {task.pet_name}")
print("-" * 35)
print(f"Total tasks: {len(schedule)}")