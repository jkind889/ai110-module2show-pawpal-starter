from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Task:
    def __init__(self, task_id: str, name: str, duration_minutes: int, priority: Priority,
                 is_recurring: bool = False, recurrence: str = ""):
        self.task_id = task_id
        self.name = name
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.is_recurring = is_recurring
        self.recurrence = recurrence

    def validate(self) -> bool:
        """Return True if task_id, name, positive duration, and valid priority are all set."""
        if not self.task_id or not self.name:
            return False
        if self.duration_minutes <= 0:
            return False
        if not isinstance(self.priority, Priority):
            return False
        return True


class WalkTask(Task):
    def __init__(self, task_id: str, name: str, duration_minutes: int, priority: Priority,
                 distance_km: float = 0.0, route_notes: str = "", needs_leash: bool = True,
                 is_recurring: bool = False, recurrence: str = ""):
        """Extend Task with walk-specific attributes: distance, route notes, and leash requirement."""
        super().__init__(task_id, name, duration_minutes, priority, is_recurring, recurrence)
        self.distance_km = distance_km
        self.route_notes = route_notes
        self.needs_leash = needs_leash

    def validate(self) -> bool:
        """Return True if base task is valid and distance_km is non-negative."""
        if not super().validate():
            return False
        if self.distance_km < 0:
            return False
        return True


class Pet:
    def __init__(self, name: str, species: str, breed: str, age_years: int):
        """Initialize a pet with identifying info and an empty task list."""
        self.name = name
        self.species = species
        self.breed = breed
        self.age_years = age_years
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Append a task to this pet, raising ValueError if the task_id already exists."""
        if any(t.task_id == task.task_id for t in self.tasks):
            raise ValueError(f"Task '{task.task_id}' already exists for {self.name}")
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove the task with the given task_id, silently no-ops if not found."""
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def get_tasks_by_priority(self) -> list[Task]:
        """Return all tasks sorted from highest to lowest priority."""
        return sorted(self.tasks, key=lambda t: t.priority.value, reverse=True)


class Owner:
    def __init__(self, name: str, email: str, available_minutes: int):
        """Initialize an owner with contact info, daily availability, and an empty pet list."""
        self.name = name
        self.email = email
        self.available_minutes = available_minutes
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's roster."""
        self.pets.append(pet)

    def get_daily_plan(self, pet: Pet) -> list["ScheduledTask"]:
        """Build and return a priority-ordered daily schedule for the given pet."""
        scheduler = Scheduler(self, pet)
        return scheduler.schedule(pet.get_tasks_by_priority())


class ScheduledTask:
    def __init__(self, task: Task, start_time: str, end_time: str, reasoning: str = ""):
        """Wrap a Task with its scheduled start/end times and optional scheduling rationale."""
        self.task = task
        self.start_time = start_time
        self.end_time = end_time
        self.reasoning = reasoning

    def __repr__(self) -> str:
        """Return a human-readable summary of the scheduled task."""
        return f"{self.start_time} — {self.task.name} ({self.task.duration_minutes} min) [{self.task.priority.name}]"


class Scheduler:
    START_HOUR = 8  # daily plan begins at 08:00

    def __init__(self, owner: Owner, pet: Pet):
        """Bind the scheduler to a specific owner and pet."""
        self.owner = owner
        self.pet = pet

    def schedule(self, tasks: list[Task]) -> list[ScheduledTask]:
        """Greedily schedule valid tasks in priority order within the owner's available time."""
        sorted_tasks = self.sort_by_priority(tasks)
        remaining = self.owner.available_minutes
        current_minute = self.START_HOUR * 60
        plan: list[ScheduledTask] = []

        for task in sorted_tasks:
            if not task.validate():
                continue
            if not self.fits_in_time(task, remaining):
                continue
            start = self._minutes_to_time(current_minute)
            end = self._minutes_to_time(current_minute + task.duration_minutes)
            reasoning = f"Scheduled as {task.priority.name.lower()} priority task"
            plan.append(ScheduledTask(task, start, end, reasoning))
            current_minute += task.duration_minutes
            remaining -= task.duration_minutes

        return plan

    def fits_in_time(self, task: Task, remaining: int) -> bool:
        """Return True if the task duration fits within the remaining available minutes."""
        return task.duration_minutes <= remaining

    def sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted from highest to lowest priority value."""
        return sorted(tasks, key=lambda t: t.priority.value, reverse=True)

    @staticmethod
    def _minutes_to_time(total_minutes: int) -> str:
        """Convert an absolute minute offset into an HH:MM string."""
        hours = (total_minutes // 60) % 24
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}"
