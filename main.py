from pawpal_system import Task, Pet, Owner, Scheduler, TaskType, Priority

# Setup
owner = Owner(name="Jordan", email="jordan@email.com", available_minutes=120)

dog = Pet(name="Mochi", species="dog", age=3)
cat = Pet(name="Luna", species="cat", age=5)

# Add tasks out of order to test sorting
dog.add_task(Task("Evening walk", TaskType.WALK, 30, Priority.LOW, "Mochi", time="18:00"))
dog.add_task(Task("Morning walk", TaskType.WALK, 30, Priority.HIGH, "Mochi", time="07:00"))
dog.add_task(Task("Feed breakfast", TaskType.FEEDING, 10, Priority.HIGH, "Mochi", time="08:00", frequency="daily"))

# Conflict: same time as morning walk
dog.add_task(Task("Medication", TaskType.MEDICATION, 5, Priority.HIGH, "Mochi", time="07:00"))

cat.add_task(Task("Playtime", TaskType.OTHER, 20, Priority.MEDIUM, "Luna", time="10:00", frequency="weekly"))

owner.add_pet(dog)
owner.add_pet(cat)

scheduler = Scheduler(owner)

# Sorted by time
print("\n🕐 Tasks sorted by time:")
print("-" * 35)
for task in scheduler.sort_by_time():
    print(f"  {task.time} — {task.title} ({task.pet_name})")

# Filtered by pet
print("\n🐶 Mochi's tasks:")
print("-" * 35)
for task in scheduler.filter_by_pet("Mochi"):
    print(f"  {task.title}")

# Recurring task demo
print("\n🔁 Recurring task next occurrence:")
print("-" * 35)
for task in scheduler.get_all_tasks():
    if task.frequency != "once":
        next_task = scheduler.handle_recurring(task)
        if next_task:
            print(f"  Next '{next_task.title}' due: {next_task.due_date}")

# Conflict detection
print("\n  Conflicts:")
print("-" * 35)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  {warning}")
else:
    print("  No conflicts found.")