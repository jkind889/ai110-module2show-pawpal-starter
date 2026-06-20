import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Pet care planning assistant — priority-based daily scheduling")

# ── Owner & Pet inputs ────────────────────────────────────────────────────────
st.subheader("Owner & Pet")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
    available_minutes = st.number_input("Daily availability (minutes)", min_value=1, max_value=1440, value=120)
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])

st.divider()

# ── Task inputs ───────────────────────────────────────────────────────────────
st.subheader("Tasks")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    task_id = f"t{len(st.session_state.tasks) + 1}"
    st.session_state.tasks.append(
        {"id": task_id, "title": task_title, "duration_minutes": int(duration), "priority": priority}
    )
    st.success(f"Added **{task_title}** ({duration} min, {priority} priority)")

if st.session_state.tasks:
    st.markdown("**Current tasks (unsorted):**")
    st.table([
        {"Title": t["title"], "Duration (min)": t["duration_minutes"], "Priority": t["priority"].upper()}
        for t in st.session_state.tasks
    ])
    if st.button("Clear all tasks"):
        st.session_state.tasks = []
        st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# ── Schedule generation ───────────────────────────────────────────────────────
st.subheader("Generate Schedule")

if st.button("Build schedule", type="primary"):
    if not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        priority_map = {"low": Priority.LOW, "medium": Priority.MEDIUM, "high": Priority.HIGH}

        pet = Pet(name=pet_name, species=species, breed="", age_years=0)
        owner = Owner(name=owner_name, email="", available_minutes=int(available_minutes))
        owner.add_pet(pet)

        for t in st.session_state.tasks:
            task = Task(
                task_id=t["id"],
                name=t["title"],
                duration_minutes=t["duration_minutes"],
                priority=priority_map[t["priority"]],
            )
            pet.add_task(task)

        scheduler = Scheduler(owner, pet)
        sorted_tasks = scheduler.sort_by_priority(pet.tasks)
        plan = scheduler.schedule(sorted_tasks)

        # ── Sorted task list ──────────────────────────────────────────────────
        st.markdown("### Sorted by Priority")
        for task in sorted_tasks:
            badge = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(task.priority.name, "⚪")
            st.markdown(f"{badge} **{task.name}** — {task.duration_minutes} min `{task.priority.name}`")

        st.divider()

        # ── Schedule ──────────────────────────────────────────────────────────
        skipped = [t for t in sorted_tasks if not any(st.task.task_id == t.task_id for st in plan)]

        st.markdown("### Daily Schedule")
        if plan:
            st.success(f"Scheduled {len(plan)} task(s) within {available_minutes} minutes of availability.")
            for st_task in scheduler.sort_by_time(plan):
                with st.container(border=True):
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        badge = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(st_task.task.priority.name, "⚪")
                        st.markdown(f"{badge} **{st_task.task.name}**")
                        st.caption(st_task.reasoning)
                    with col_b:
                        st.markdown(f"`{st_task.start_time}` → `{st_task.end_time}`")
        else:
            st.error("No tasks could be scheduled — all tasks exceed the owner's available time.")

        if skipped:
            st.divider()
            st.markdown("### Skipped Tasks")
            st.warning(f"{len(skipped)} task(s) could not fit in the available time and were skipped.")
            for task in skipped:
                st.markdown(f"- **{task.name}** ({task.duration_minutes} min) — exceeds remaining availability")

        # ── Conflict detection ────────────────────────────────────────────────
        conflicts = scheduler.detect_conflicts(plan)
        if conflicts:
            st.divider()
            st.markdown("### Conflicts Detected")
            for msg in conflicts:
                st.warning(msg)
        elif plan:
            st.success("No scheduling conflicts detected.")
