import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler, TaskType, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# -------------------------------------------------------
# Session state
# -------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = None

# -------------------------------------------------------
# Owner setup
# -------------------------------------------------------
st.subheader("Owner Info")
owner_name = st.text_input("Your name")
owner_email = st.text_input("Your email")
available_minutes = st.number_input("Minutes available today", min_value=10, max_value=480, value=120)

if st.button("Save Owner"):
    st.session_state.owner = Owner(
        name=owner_name,
        email=owner_email,
        available_minutes=available_minutes
    )
    st.success(f"Owner {owner_name} saved!")

# -------------------------------------------------------
# Only show rest if owner exists
# -------------------------------------------------------
if st.session_state.owner:
    owner = st.session_state.owner

    st.divider()

    # -------------------------------------------------------
    # Add a pet
    # -------------------------------------------------------
    st.subheader("Add a Pet")
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=30, value=1, key="pet_age")
    breed = st.text_input("Breed (optional)")

    if st.button("Add Pet"):
        pet = Pet(name=pet_name, species=species, age=int(age), breed=breed)
        owner.add_pet(pet)
        st.success(f"{pet_name} added!")

    if owner.pets:
        st.write("Your pets:", [p.name for p in owner.pets])

    st.divider()

    # -------------------------------------------------------
    # Add a task
    # -------------------------------------------------------
    st.subheader("Add a Task")

    if owner.pets:
        selected_pet_name = st.selectbox("Assign to pet", [p.name for p in owner.pets])
        task_title = st.text_input("Task title")
        task_type = st.selectbox("Task type", [t.value for t in TaskType])
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["high", "medium", "low"])
        task_time = st.text_input("Scheduled time (HH:MM)", value="08:00")
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

        if st.button("Add Task"):
            task = Task(
                title=task_title,
                task_type=TaskType(task_type),
                duration_minutes=int(duration),
                priority=Priority(priority),
                pet_name=selected_pet_name,
                time=task_time,
                frequency=frequency
            )
            for pet in owner.pets:
                if pet.name == selected_pet_name:
                    pet.add_task(task)
            st.success(f"Task '{task_title}' added!")
    else:
        st.info("Add a pet first before adding tasks.")

    st.divider()

    # -------------------------------------------------------
    # Generate schedule
    # -------------------------------------------------------
    st.subheader("Today's Schedule")

    if st.button("Generate Schedule"):
        scheduler = Scheduler(owner)
        schedule = scheduler.sort_by_time()

        if schedule:
            # Conflict warnings
            conflicts = scheduler.detect_conflicts()
            if conflicts:
                for warning in conflicts:
                    st.warning(warning)

            # Display schedule as table
            table_data = []
            for task in schedule:
                table_data.append({
                    "Time": task.time,
                    "Task": task.title,
                    "Pet": task.pet_name,
                    "Duration (min)": task.duration_minutes,
                    "Priority": task.priority.value.upper(),
                    "Frequency": task.frequency,
                    "Done": "✅" if task.is_completed else "⬜"
                })
            st.table(table_data)

            # Pending vs completed summary
            pending = scheduler.filter_by_status(completed=False)
            done = scheduler.filter_by_status(completed=True)
            col1, col2 = st.columns(2)
            col1.metric("Pending tasks", len(pending))
            col2.metric("Completed tasks", len(done))

        else:
            st.info("No tasks yet. Add some tasks first.")