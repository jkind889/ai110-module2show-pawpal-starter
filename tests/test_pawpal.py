import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, Priority


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
