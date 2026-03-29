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

## Smarter Scheduling Features

This implementation includes advanced scheduling capabilities:

### Task Sorting & Filtering
- **Priority-based sorting**: Tasks are sorted by effective priority score (combining task type priority and duration priority)
- **Pet-specific filtering**: Filter tasks by specific pet or include universal tasks
- **Status filtering**: Separate completed from incomplete tasks

### Recurring Tasks
- **Daily recurrence**: Tasks that repeat every day
- **Weekly recurrence**: Tasks that repeat on specific weekdays (e.g., Monday, Wednesday, Friday)
- **Auto-creation**: When a recurring task is completed, the next occurrence is automatically created and added to the schedule
- **End date support**: Recurring tasks can have an end date to stop recurrence

### Conflict Detection
- **Overlap detection**: Identifies when scheduled tasks overlap in time
- **Same-pet conflicts**: Warns when the same pet has overlapping tasks
- **Different-pet conflicts**: Notes when different pets have overlapping tasks
- **Conflict warnings**: Provides human-readable warnings about scheduling conflicts

### Schedule Management
- **Time-based sorting**: Tasks are displayed in chronological order
- **Duration tracking**: Shows task durations and total scheduled time
- **Constraint handling**: Respects time constraints when building schedules
- **Daily summaries**: Provides overview of daily tasks, completion status, and conflicts
