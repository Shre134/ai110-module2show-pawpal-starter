import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler, TaskType, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# -------------------------------------------------------
# Session state — keeps data alive between button clicks
# -------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = None

# -------------------------------------------------------
# Step 1: Owner setup
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
# Only show the rest if owner exists
# -------------------------------------------------------
if st.session_state.owner:
    owner = st.session_state.owner

    st.divider()

    # -------------------------------------------------------
    # Step 2: Add a pet
    # -------------------------------------------------------
    st.subheader("Add a Pet")

    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=30, value=1, key="pet_age")

    breed = st.text_input("Breed (optional)")

    if st.button("Add Pet"):
        pet = Pet(name=pet_name, species=species, age=age, breed=breed)
        owner.add_pet(pet)
        st.success(f"{pet_name} added!")

    # Show current pets
    if owner.pets:
        st.write("Your pets:", [p.name for p in owner.pets])

    st.divider()

    # -------------------------------------------------------
    # Step 3: Add a task
    # -------------------------------------------------------
    st.subheader("Add a Task")

    if owner.pets:
        selected_pet_name = st.selectbox("Assign to pet", [p.name for p in owner.pets])
        task_title = st.text_input("Task title")
        task_type = st.selectbox("Task type", [t.value for t in TaskType])
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["high", "medium", "low"])

        if st.button("Add Task"):
            task = Task(
                title=task_title,
                task_type=TaskType(task_type),
                duration_minutes=duration,
                priority=Priority(priority),
                pet_name=selected_pet_name
            )
            # Find the pet and add the task to it
            for pet in owner.pets:
                if pet.name == selected_pet_name:
                    pet.add_task(task)
            st.success(f"Task '{task_title}' added!")
    else:
        st.info("Add a pet first before adding tasks.")

    st.divider()

    # -------------------------------------------------------
    # Step 4: Generate schedule
    # -------------------------------------------------------
    st.subheader("Today's Schedule")

    if st.button("Generate Schedule"):
        scheduler = Scheduler(owner)
        schedule = scheduler.get_todays_schedule()

        if schedule:
            for task in schedule:
                status = "✅" if task.is_completed else "⬜"
                st.markdown(
                    f"{status} **{task.title}** — {task.pet_name} "
                    f"| {task.duration_minutes} min | Priority: {task.priority.value.upper()}"
                )
        else:
            st.info("No tasks yet. Add some tasks first.")