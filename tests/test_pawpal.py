import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, Owner, Scheduler, Priority


def test_add_task_to_pet():
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age_years=3)
    task = Task(task_id="t1", name="Morning walk", duration_minutes=30, priority=Priority.HIGH)

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0].task_id == "t1"


def test_complete_task_removes_it_from_pet():
    pet = Pet(name="Buddy", species="dog", breed="Labrador", age_years=3)
    task = Task(task_id="t2", name="Feed Buddy", duration_minutes=10, priority=Priority.MEDIUM)
    pet.add_task(task)

    pet.remove_task("t2")

    assert len(pet.tasks) == 0


# --- Pet with no tasks ---

def test_daily_plan_for_pet_with_no_tasks():
    pet = Pet(name="Luna", species="cat", breed="Siamese", age_years=2)
    owner = Owner(name="Alex", email="alex@example.com", available_minutes=120)
    owner.add_pet(pet)

    plan = owner.get_daily_plan(pet)

    assert plan == []


# --- Two tasks at the same time (conflict detection) ---

def test_detect_conflict_between_overlapping_tasks():
    pet = Pet(name="Max", species="dog", breed="Poodle", age_years=4)
    owner = Owner(name="Sam", email="sam@example.com", available_minutes=120)
    owner.add_pet(pet)

    task1 = Task(task_id="c1", name="Walk", duration_minutes=60, priority=Priority.HIGH)
    task2 = Task(task_id="c2", name="Bath", duration_minutes=60, priority=Priority.HIGH)
    pet.add_task(task1)
    pet.add_task(task2)

    scheduler = Scheduler(owner, pet)

    # Manually create two overlapping ScheduledTask entries to test conflict detection
    from pawpal_system import ScheduledTask
    overlap_a = ScheduledTask(task1, "08:00", "09:00")
    overlap_b = ScheduledTask(task2, "08:30", "09:30")
    conflicts = scheduler.detect_conflicts([overlap_a, overlap_b])

    assert len(conflicts) == 1
    assert "CONFLICT" in conflicts[0]


# --- Everything works (full happy path) ---

def test_full_happy_path_schedule():
    pet = Pet(name="Coco", species="dog", breed="Beagle", age_years=5)
    owner = Owner(name="Jordan", email="jordan@example.com", available_minutes=120)
    owner.add_pet(pet)

    task1 = Task(task_id="h1", name="Morning walk", duration_minutes=30, priority=Priority.HIGH)
    task2 = Task(task_id="h2", name="Feeding", duration_minutes=15, priority=Priority.MEDIUM)
    task3 = Task(task_id="h3", name="Playtime", duration_minutes=20, priority=Priority.LOW)
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)

    plan = owner.get_daily_plan(pet)

    assert len(plan) == 3
    # HIGH priority task should be scheduled first
    assert plan[0].task.task_id == "h1"
    assert plan[0].start_time == "08:00"
    assert plan[0].end_time == "08:30"


# --- Adding a task to a pet that doesn't exist on the owner ---

def test_add_task_to_unregistered_pet():
    owner = Owner(name="Riley", email="riley@example.com", available_minutes=60)
    ghost_pet = Pet(name="Ghost", species="dog", breed="Husky", age_years=3)
    # ghost_pet is never added to owner.pets

    task = Task(task_id="g1", name="Walk", duration_minutes=30, priority=Priority.HIGH)
    ghost_pet.add_task(task)

    # The pet is not in the owner's roster
    assert ghost_pet not in owner.pets
    assert len(ghost_pet.tasks) == 1


# --- Tasks that exceed owner availability ---

def test_tasks_exceeding_owner_availability_are_skipped():
    pet = Pet(name="Tiny", species="cat", breed="Persian", age_years=1)
    owner = Owner(name="Casey", email="casey@example.com", available_minutes=20)
    owner.add_pet(pet)

    short_task = Task(task_id="e1", name="Quick feed", duration_minutes=10, priority=Priority.HIGH)
    long_task = Task(task_id="e2", name="Long grooming", duration_minutes=60, priority=Priority.MEDIUM)
    pet.add_task(short_task)
    pet.add_task(long_task)

    plan = owner.get_daily_plan(pet)

    scheduled_ids = [st.task.task_id for st in plan]
    assert "e1" in scheduled_ids
    assert "e2" not in scheduled_ids
