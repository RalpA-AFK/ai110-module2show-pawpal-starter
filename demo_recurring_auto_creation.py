"""
Demo: Recurring Task Auto-Recreation
Shows how daily and weekly tasks automatically create their next occurrence
when marked complete, using Python's timedelta for date calculations.
"""

from pawpal_system import Owner, Pet, Schedule, RecurringTask
from datetime import date, timedelta

print("=" * 70)
print("RECURRING TASK AUTO-RECREATION DEMO")
print("=" * 70)

# Setup
owner = Owner(name="Sarah")
mochi = Pet(name="Mochi", species="dog")
owner.add_pet(mochi)

schedule = Schedule(owner=owner, pet=mochi)

print("\n1. DAILY RECURRING TASK AUTO-CREATION")
print("-" * 70)

today = date.today()
print(f"Today: {today.strftime('%A, %B %d, %Y')}")

# Create a daily recurring task
daily_feed = RecurringTask(
    title="Mochi's Daily Breakfast",
    duration_minutes=10,
    task_type="feed",
    pet_name="Mochi",
    recurrence_pattern="daily",
    start_date=today,
    end_date=today + timedelta(days=5),  # End after 5 days
    due_date=today
)

schedule.add_task(daily_feed)
print(f"\n✓ Created: {daily_feed.title}")
print(f"  DueDate: {daily_feed.due_date.strftime('%A, %B %d')}")
print(f"  Pattern: Daily, ends on {daily_feed.end_date.strftime('%A, %B %d')}")
print(f"  Using timedelta: today + timedelta(days=1) for next occurrence")

# Mark complete - should create tomorrow's task
print(f"\n→ Marking complete...")
next_daily = schedule.complete_task(daily_feed)

print(f"\n✓ Original task marked complete")
print(f"  Completed: {daily_feed.completed}")
print(f"  Last completed: {daily_feed.last_completed_date.strftime('%A, %B %d')}")

print(f"\n✓ New task auto-created for next occurrence:")
print(f"  Title: {next_daily.title}")
print(f"  Due Date: {next_daily.due_date.strftime('%A, %B %d')} (today + 1 day)")
print(f"  Status: {'Completed' if next_daily.completed else 'Pending'}")

print(f"\n→ Schedule now has {len(schedule.tasks)} tasks total")

print("\n" + "=" * 70)
print("2. WEEKLY RECURRING TASK AUTO-CREATION")
print("-" * 70)

# Get next Monday
monday = today if today.weekday() == 0 else today + timedelta(days=(7 - today.weekday()))
print(f"\nNext Monday: {monday.strftime('%A, %B %d, %Y')}")

# Create a weekly task
weekly_walk = RecurringTask(
    title="Mochi's Weekly Grooming",
    duration_minutes=45,
    task_type="play",
    pet_name="Mochi",
    recurrence_pattern="weekly",
    recurrence_days={0, 3},  # Monday and Thursday
    start_date=monday,
    end_date=monday + timedelta(days=28),  # 4 weeks
    due_date=monday
)

schedule.add_task(weekly_walk)
print(f"\n✓ Created: {weekly_walk.title}")
print(f"  Due Date: {weekly_walk.due_date.strftime('%A, %B %d')}")
print(f"  Pattern: Weekly on Mondays and Thursdays")
print(f"  Using timedelta: searches day-by-day until next matching weekday is found")

# Mark complete - should create next Thursday's task
print(f"\n→ Marking complete on {monday.strftime('%A')}...")
next_weekly = schedule.complete_task(weekly_walk)

print(f"\n✓ Original task marked complete")
print(f"  Completed: {weekly_walk.completed}")

print(f"\n✓ New task auto-created for next occurrence:")
print(f"  Title: {next_weekly.title}")
print(f"  Due Date: {next_weekly.due_date.strftime('%A, %B %d')} (next Thursday)")
print(f"  Days until next: {(next_weekly.due_date - weekly_walk.due_date).days} days")

print("\n" + "=" * 70)
print("3. RECURRING TASK CHAIN - MULTIPLE COMPLETIONS")
print("-" * 70)

print("\nCreating a 3-day daily task and completing it twice:")

three_day_task = RecurringTask(
    title="Check water bowl",
    duration_minutes=2,
    task_type="feed",
    pet_name="Mochi",
    recurrence_pattern="daily",
    start_date=today,
    end_date=today + timedelta(days=3),
    due_date=today
)

print(f"Day 0: Created - Due {today.strftime('%a, %b %d')}")

# First completion
task_day1 = schedule.complete_task(three_day_task)
print(f"Day 1: Completed '{three_day_task.title}' → Auto-created next for {task_day1.due_date.strftime('%a, %b %d')}")

# Second completion
if task_day1:
    task_day2 = schedule.complete_task(task_day1)
    print(f"Day 2: Completed '{task_day1.title}' → Auto-created next for {task_day2.due_date.strftime('%a, %b %d')}")

    # Third completion
    if task_day2:
        task_day3 = schedule.complete_task(task_day2)
        if task_day3:
            print(f"Day 3: Completed '{task_day2.title}' → Auto-created next for {task_day3.due_date.strftime('%a, %b %d')}")
        else:
            print(f"Day 3: Completed '{task_day2.title}' → No next occurrence (reached end date)")

print("\n" + "=" * 70)
print("4. SUMMARY - All Tasks in Schedule")
print("-" * 70)

print(f"\nTotal tasks in schedule: {len(schedule.tasks)}")
print("\nTask Chain:")
for i, task in enumerate(schedule.tasks, 1):
    if isinstance(task, RecurringTask):
        status = "✓ done" if task.completed else "○ pending"
        print(f"  {i}. {task.title:30} Due: {task.due_date.strftime('%a, %b %d'):15} [{status}]")

print("\n" + "=" * 70)
print("Demo Complete!")
print("=" * 70)
