
class Task:
    def __init__(self, task_id: str, name: str, duration_minutes: int, priority: str,
                 is_recurring: bool = False, recurrence: str = ""):
        self.task_id = task_id
        self.name = name
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.is_recurring = is_recurring
        self.recurrence = recurrence

    def validate(self) -> bool:
        pass


class WalkTask(Task):
    def __init__(self, task_id: str, name: str, duration_minutes: int, priority: str,
                 distance_km: float = 0.0, route_notes: str = "", needs_leash: bool = True,
                 is_recurring: bool = False, recurrence: str = ""):
        super().__init__(task_id, name, duration_minutes, priority, is_recurring, recurrence)
        self.distance_km = distance_km
        self.route_notes = route_notes
        self.needs_leash = needs_leash

    def validate(self) -> bool:
        pass


class Pet:
    def __init__(self, name: str, species: str, breed: str, age_years: int):
        self.name = name
        self.species = species
        self.breed = breed
        self.age_years = age_years
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_id: str) -> None:
        pass

    def get_tasks_by_priority(self) -> list[Task]:
        pass


class Owner:
    def __init__(self, name: str, email: str, available_minutes: int):
        self.name = name
        self.email = email
        self.available_minutes = available_minutes
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_daily_plan(self) -> list["ScheduledTask"]:
        pass


class ScheduledTask:
    def __init__(self, task: Task, start_time: str, end_time: str, reasoning: str = ""):
        self.task = task
        self.start_time = start_time
        self.end_time = end_time
        self.reasoning = reasoning


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet
        self.available_minutes = owner.available_minutes

    def schedule(self, tasks: list[Task]) -> list[ScheduledTask]:
        pass

    def fits_in_time(self, task: Task, remaining: int) -> bool:
        pass

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        pass
