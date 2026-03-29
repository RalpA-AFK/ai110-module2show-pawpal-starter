import streamlit as st
from pawpal_system import Owner, Pet, Task, Schedule, DisplayChart

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
PawPal+ is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) with time constraints and priorities.
"""
)

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

st.subheader("Owner & Pets")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
owner_contact = st.text_input("Contact info", value=st.session_state.owner.contact or "")

if owner_name != st.session_state.owner.name:
    st.session_state.owner.update_name(owner_name)

if owner_contact and owner_contact != st.session_state.owner.contact:
    st.session_state.owner.contact = owner_contact

with st.expander("Add pet", expanded=False):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed", value="")
    food_type = st.text_input("Food type", value="")

    if st.button("Add pet"):
        try:
            new_pet = Pet(name=pet_name.strip(), species=species.strip(), breed=breed.strip() or None, food_type=food_type.strip() or None)
            st.session_state.owner.add_pet(new_pet)
            st.success(f"Added pet: {new_pet.name}")
        except Exception as e:
            st.error(str(e))

if st.session_state.owner.pets:
    st.write("### Current pets")
    st.table([{"name": p.name, "species": p.species, "breed": p.breed or "", "food_type": p.food_type or ""} for p in st.session_state.owner.pets])
else:
    st.info("No pets added yet")

with st.expander("Pet preferred task times", expanded=False):
    if st.session_state.owner.pets:
        pet_select_for_times = st.selectbox("Choose pet", [p.name for p in st.session_state.owner.pets])
        task_type_time = st.selectbox("Task type", ["feed", "walk", "play"])
        preferred_time = st.time_input("Preferred time", value=None)

        if st.button("Set preferred task time"):
            if pet_select_for_times and preferred_time:
                st.session_state.owner.set_pet_task_time(pet_select_for_times, task_type_time, preferred_time.strftime("%H:%M"))
                st.success(f"Set {task_type_time} for {pet_select_for_times} at {preferred_time.strftime('%H:%M')}")

        pet_time_rows = []
        for pet in st.session_state.owner.pets:
            timings = st.session_state.owner.pet_task_times.get(pet.name, {})
            pet_time_rows.append({"pet": pet.name, "feed": timings.get("feed", ""), "walk": timings.get("walk", ""), "play": timings.get("play", "")})
        if pet_time_rows:
            st.table(pet_time_rows)
    else:
        st.info("Add a pet first to set preferred task times.")

st.divider()

st.subheader("Tasks")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Dog feed")
with col2:
    task_type = st.selectbox("Task type", ["feed", "walk", "play"], index=0)
with col3:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=15)
with col4:
    priority = st.selectbox("Priority", ["high", "medium", "low"], index=0)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title.strip(), "task_type": task_type, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

selected_pet = None
if st.session_state.owner.pets:
    selected_pet_name = st.selectbox("Select pet for schedule", [p.name for p in st.session_state.owner.pets])
    selected_pet = next((p for p in st.session_state.owner.pets if p.name == selected_pet_name), None)

if st.button("Generate schedule"):
        if not selected_pet:
            st.error("Please add and select a pet before generating a schedule.")
        elif not st.session_state.tasks:
            st.error("Please add tasks before generating a schedule.")
        else:
            schedule = Schedule(owner=st.session_state.owner, pet=selected_pet)

            for task_data in st.session_state.tasks:
                try:
                    schedule.add_task(Task(
                        title=task_data["title"],
                        duration_minutes=task_data["duration_minutes"],
                        task_type=task_data["task_type"],
                        priority=task_data["priority"],
                    ))
                except Exception as e:
                    st.error(f"Skipping task '{task_data['title']}': {e}")

            plan = schedule.build_plan(start_hour=8, start_minute=0)
            if not plan:
                st.warning("No tasks could be scheduled (time constraints or empty task list).")
            else:
                st.session_state.current_schedule = schedule

                st.markdown("### Daily schedule")
                chart = DisplayChart(schedule)
                st.text(chart.display())

                # mark complete action
                completed_task = st.selectbox(
                    "Select a task to mark complete",
                    [task.title for task in schedule.plan],
                    key="complete_task_select"
                )
                if st.button("Mark task complete"):
                    task_to_complete = next((task for task in schedule.plan if task.title == completed_task), None)
                    if task_to_complete:
                        task_to_complete.mark_complete()
                        for slot in schedule.plan_slots:
                            if slot["title"] == task_to_complete.title:
                                slot["completed"] = True
                        st.success(f"Marked '{task_to_complete.title}' as complete")
                        st.text(DisplayChart(schedule).display())

                st.markdown("### Plan explanation")
                st.text(schedule.explain_plan())

                st.markdown("### Schedule table")
                st.table(schedule.plan_slots)
