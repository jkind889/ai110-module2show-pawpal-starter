from pawpal_system import Owner,Task,WalkTask,Pet,ScheduledTask,Scheduler,Priority
from datetime import date

def main():

    owner = Owner("Jay","jk@gmail.com",180)

    bob = Pet("bob","cat","black",18)
    twin = Pet("twin","dog","golden retriever",20)
    yugi = Pet("yugi","dog","golden retriever",10)

    owner.add_pet(bob)
    owner.add_pet(twin)
    owner.add_pet(yugi)

    today = date.today()

    bob.add_task(Task("b1", "Feeding", 10, Priority.HIGH))
    bob.add_task(Task("b2", "Grooming", 20, Priority.MEDIUM))
    bob.add_task(Task("b3", "Enrichment play", 15, Priority.LOW))

    twin.add_task(WalkTask("t1", "Morning walk", 30, Priority.HIGH, distance_km=1.5))
    twin.add_task(Task("t2", "Feeding", 10, Priority.HIGH))
    twin.add_task(Task("t3", "Medication", 5, Priority.MEDIUM))

    yugi.add_task(WalkTask("y1", "Park run", 45, Priority.HIGH, distance_km=3.0))
    yugi.add_task(Task("y2", "Feeding", 10, Priority.HIGH))
    yugi.add_task(Task("y3", "Training session", 20, Priority.LOW))

    print(f"\n{'='*40}")
    print(f"  Today's Schedule — {today.strftime('%A, %B %d %Y')}")
    print(f"{'='*40}")

    for pet in owner.pets:
        plan = owner.get_daily_plan(pet)
        print(f"\n{pet.name.capitalize()} ({pet.breed}):")
        if not plan:
            print("  No tasks scheduled.")
        for entry in plan:
            print(f"  {entry}")

    print(f"\n{'='*40}\n")


main()
