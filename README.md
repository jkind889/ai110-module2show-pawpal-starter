# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

========================================
  Today's Schedule — Friday, June 19 2026
========================================

Bob (black):
  08:00 — Feeding (10 min) [HIGH]
  08:10 — Grooming (20 min) [MEDIUM]
  08:30 — Enrichment play (15 min) [LOW]

Twin (golden retriever):
  08:00 — Morning walk (30 min) [HIGH]
  08:30 — Feeding (10 min) [HIGH]
  08:40 — Medication (5 min) [MEDIUM]

Yugi (golden retriever):
  08:00 — Park run (45 min) [HIGH]
  08:45 — Feeding (10 min) [HIGH]
  08:55 — Training session (20 min) [LOW]

========================================

## 🧪 Testing PawPal+

```bash
python3 -m pytest
```

Sample test output:

```
==================================================================================== test session starts ====================================================================================
platform darwin -- Python 3.13.0, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/jovakind/repos/ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 7 items                                                                                                                                                                           

tests/test_pawpal.py .......                                                                                                                                                          [100%]

===================================================================================== 7 passed in 0.02s =====================================================================================
```

Confidence Level: ⭐⭐⭐⭐ (4/5)

Tests cover, scheduling a pet with no tasks, a pet with two overlapping task times, overall tests with expected behaviors, adding a task to a pet that doesn't exist, tasks that exceed owner availability

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sort by priority | `Scheduler.sort_by_priority()`, `Pet.get_tasks_by_priority()` | Tasks sorted HIGH → MEDIUM → LOW using `Priority` enum integer values; both the `Scheduler` and `Pet` expose this independently |
| Sort by duration | `Scheduler.sort_tasks_by_duration()` | Secondary sort that orders tasks shortest → longest, useful for fitting more tasks into a constrained time window |
| Sort scheduled by time | `Scheduler.sort_by_time()` | Reorders already-scheduled tasks chronologically by `start_time` before displaying them |
| Greedy time-budget filtering | `Scheduler.schedule()` via `Scheduler.fits_in_time()` | Iterates tasks in priority order and skips any task whose `duration_minutes` exceeds the owner's remaining available minutes; skipped tasks are surfaced in the UI |
| Task validation filtering | `Task.validate()` / `WalkTask.validate()` | Tasks with missing IDs, empty names, non-positive durations, or invalid priority values are silently skipped during scheduling |
| Completion + pet-name filtering | `Scheduler.filter_tasks()` | Filters a task list by `is_completed` status and/or pet name, enabling views of pending vs. done tasks per pet |
| Conflict detection | `Scheduler.detect_conflicts()` | O(n²) pairwise scan of scheduled tasks; flags any pair where one task's window overlaps another using the interval overlap condition (`a.start < b.end and b.start < a.end`) |
| Recurring tasks | `Task.mark_completed()` | Marking a `daily` or `weekly` recurring task complete returns a cloned next-occurrence instance with `is_completed = False`, allowing the recurrence chain to continue |

## 📸 Demo Walkthrough

1. **Enter owner info** — Type the owner's name and set their daily availability in minutes (e.g., 120 min). This acts as the hard time budget for the scheduler.
2. **Enter pet info** — Type the pet's name and select its species. The schedule is generated per pet.
3. **Add tasks** — For each care task (walk, feeding, medication, etc.), enter a title, duration in minutes, and priority (low / medium / high), then click **Add task**. The task appears in the unsorted task table below.
4. **Review the task list** — The table shows all added tasks before any scheduling logic runs. Use **Clear all tasks** to start over.
5. **Generate the schedule** — Click **Build schedule**. The app first displays tasks re-ordered by priority (HIGH → MEDIUM → LOW), then runs the greedy scheduler.
6. **Read the daily plan** — Each scheduled task is shown as a card with its time window (`08:00 → 08:30`), priority badge, and the scheduling rationale. Tasks are sorted chronologically.
7. **Check for skipped tasks** — If any task's duration exceeded the remaining availability budget, it appears in the **Skipped Tasks** section with an explanation.
8. **Check for conflicts** — The app runs overlap detection across all scheduled tasks and either lists any conflicts found or confirms "No scheduling conflicts detected."

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
