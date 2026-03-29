"""
Demo script showcasing all advanced PawPal+ features:
- Task sorting by time
- Filtering by pet/status
- Recurring tasks
- Conflict detection
"""

from pawpal_system import Owner, Pet, Task, Schedule, RecurringTask
from datetime import date

print("=" * 60)
print("PawPal+ Advanced Features Demo")
print("=" * 60)

# Setup
owner = Owner(name="Sarah")
max_dog = Pet(name="Max", species="dog", breed="Golden Retriever")
bella_cat = Pet(name="Bella", species="cat", breed="Tabby")

owner.add_pet(max_dog)
owner.add_pet(bella_cat)

# Create a schedule
schedule = Schedule(owner=owner, pet=max_dog)

print("\n1. TASK CREATION WITH PET TRACKING")
print("-" * 60)
tasks = [
    Task(title="Max breakfast", duration_minutes=10, task_type="feed", priority="high", pet_name="Max"),
    Task(title="Max morning walk", duration_minutes=30, task_type="walk", priority="medium", pet_name="Max"),
    Task(title="Bella breakfast", duration_minutes=10, task_type="feed", priority="high", pet_name="Bella"),
    Task(title="Play with Max", duration_minutes=20, task_type="play", priority="low", pet_name="Max"),
]

for task in tasks:
    schedule.add_task(task)
    print(f"✓ Added: {task.title} ({task.duration_minutes}m) - Pet: {task.pet_name or 'Any'}")

print("\n2. FILTERING TASKS BY PET")
print("-" * 60)
max_tasks = schedule.filter_tasks_by_pet("Max")
bella_tasks = schedule.filter_tasks_by_pet("Bella")
print(f"Tasks for Max ({len(max_tasks)}): {[t.title for t in max_tasks]}")
print(f"Tasks for Bella ({len(bella_tasks)}): {[t.title for t in bella_tasks]}")

print("\n3. TASK COMPLETION STATUS")
print("-" * 60)
tasks[0].mark_complete()  # Mark first task as complete
tasks[2].mark_complete()  # Mark Bella's breakfast as complete

completed = schedule.filter_tasks_by_status(completed=True)
incomplete = schedule.filter_tasks_by_status(completed=False)
print(f"Completed tasks ({len(completed)}): {[t.title for t in completed]}")
print(f"Incomplete tasks ({len(incomplete)}): {[t.title for t in incomplete]}")

print("\n4. SCHEDULING AND TIME-BASED SORTING")
print("-" * 60)
plan = schedule.build_plan(start_hour=7, start_minute=30)
sorted_slots = schedule.get_tasks_sorted_by_time()

print("Schedule (sorted by time):")
for i, slot in enumerate(sorted_slots, 1):
    print(f"  {i}. {slot['start']} - {slot['end']}: {slot['title']} ({slot['duration_minutes']}m)")

print("\n5. RECURRING TASKS")
print("-" * 60)
recurring_feed = RecurringTask(
    title="Daily Max feeding",
    duration_minutes=10,
    task_type="feed",
    pet_name="Max",
    recurrence_pattern="daily",
    start_date=date(2026, 3, 29),
    end_date=date(2026, 4, 2)
)

print(f"Recurring Task: {recurring_feed.title}")
print(f"Pattern: {recurring_feed.recurrence_pattern}")
print(f"Active on 2026-03-29 (Sun): {recurring_feed.is_active_on_date(date(2026, 3, 29))}")
print(f"Active on 2026-03-30 (Mon): {recurring_feed.is_active_on_date(date(2026, 3, 30))}")

occurrences = recurring_feed.get_occurrences_in_range(
    date(2026, 3, 29), date(2026, 4, 2)
)
print(f"Occurrences in range: {len(occurrences)} days")
for occ_date in occurrences:
    print(f"  - {occ_date.strftime('%A, %B %d, %Y')}")

print("\n6. CONFLICT DETECTION")
print("-" * 60)
# Create a schedule with overlapping tasks
conflict_schedule = Schedule(owner=owner, pet=max_dog)
conflict_schedule.plan_slots = [
    {"title": "Breakfast", "start": "7:30 AM", "end": "7:45 AM", "duration_minutes": 15},
    {"title": "Walk", "start": "7:40 AM", "end": "8:10 AM", "duration_minutes": 30},  # Overlaps!
    {"title": "Play", "start": "8:15 AM", "end": "8:35 AM", "duration_minutes": 20},
]

conflicts = conflict_schedule.detect_conflicts()
if conflicts:
    print(f"⚠️  {len(conflicts)} conflict(s) detected:")
    for conflict in conflicts:
        print(f"  • {conflict['overlap_description']}")
        print(f"    {conflict['task1']}: {conflict['time1']}")
        print(f"    {conflict['task2']}: {conflict['time2']}")
else:
    print("✓ No conflicts detected")

print("\n7. DAILY TASK SUMMARY")
print("-" * 60)
summary = schedule.get_daily_task_summary()
print(f"Date: {summary['date']}")
print(f"Total tasks: {summary['total_tasks']}")
print(f"Completed: {summary['completed_tasks']}")
print(f"Remaining: {summary['remaining_tasks']}")
print(f"Total duration: {summary['total_duration_minutes']} minutes")
print(f"Available time: {summary['available_time_minutes']} minutes")
print(f"Conflicts: {len(summary['conflicts_detected'])}")

print("\n" + "=" * 60)
print("Demo Complete!")
print("=" * 60)
