import pytest
from pawpal_system import Pet
from datetime import timedelta


def test_pet_initialization_valid():
    p = Pet(name="Mochi", species="dog", breed="Shiba", food_type="kibble")
    assert p.name == "Mochi"
    assert p.species == "dog"
    assert p.breed == "Shiba"
    assert p.food_type == "kibble"


def test_pet_invalid_name_raises():
    with pytest.raises(ValueError):
        Pet(name="", species="cat")


def test_pet_invalid_species_raises():
    with pytest.raises(ValueError):
        Pet(name="Mochi", species="dragon")


def test_pet_updates():
    p = Pet(name="Mochi", species="cat")
    p.update_name("Neko")
    p.update_species("other")
    p.set_breed("Mixed")
    p.set_food_type("wet food")

    assert p.name == "Neko"
    assert p.species == "other"
    assert p.breed == "Mixed"
    assert p.food_type == "wet food"


def test_task_initialization_and_priority():
    from pawpal_system import Task

    t = Task(title="Walk", duration_minutes=30, priority="high")
    assert t.title == "Walk"
    assert t.duration_minutes == 30
    assert t.priority == "high"


def test_task_invalid_values_raise():
    from pawpal_system import Task

    with pytest.raises(ValueError):
        Task(title="", duration_minutes=10)

    with pytest.raises(ValueError):
        Task(title="Feed", duration_minutes=0)

    with pytest.raises(ValueError):
        Task(title="Vet visit", duration_minutes=30, priority="urgent")

    with pytest.raises(ValueError):
        Task(title="Grooming", duration_minutes=20, task_type="groom")


def test_task_updates():
    from pawpal_system import Task

    t = Task(title="Feed Mochi", duration_minutes=15, task_type="feed", priority="high")
    t.set_duration(20)
    t.set_priority("low")
    t.add_notes("Morning feeding")

    assert t.duration_minutes == 20
    assert t.priority == "low"
    assert t.notes == "Morning feeding"
    assert t.title == "Feed Mochi"


def test_task_setters():
    from pawpal_system import Task

    t = Task(title="Play grooming", duration_minutes=15, task_type="play", priority="low")
    t.set_duration(20)
    t.set_priority("medium")
    t.add_notes("Evening grooming")

    assert t.duration_minutes == 20
    assert t.priority == "medium"
    assert t.notes == "Evening grooming"
    assert t.task_type == "play"


def test_owner_multiple_pets_and_task_times():
    from pawpal_system import Owner, Pet

    owner = Owner(name="Jordan")
    pet1 = Pet(name="Mochi", species="dog")
    pet2 = Pet(name="Luna", species="cat")

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    assert len(owner.pets) == 2

    owner.set_pet_task_time("Mochi", "feed", "7:30 AM")
    owner.set_pet_task_time("Mochi", "walk", "8:00 AM")
    owner.set_pet_task_time("Luna", "feed", "7:00 AM")

    assert owner.get_pet_task_time("Mochi", "feed") == "7:30 AM"
    assert owner.get_pet_task_time("Luna", "feed") == "7:00 AM"

    with pytest.raises(ValueError):
        owner.set_pet_task_time("Mochi", "feed", "07:30")

    with pytest.raises(ValueError):
        owner.set_pet_task_time("Mochi", "groom", "09:00")

    with pytest.raises(ValueError):
        owner.set_pet_task_time("Rex", "feed", "09:00")


def test_task_completion_marks():
    from pawpal_system import Task

    t = Task(title="Dog feed", duration_minutes=10, task_type="feed", priority="high")
    assert not t.completed
    t.mark_complete()
    assert t.completed


def test_task_type_inherits_priority():
    from pawpal_system import Task

    t1 = Task(title="Dog feed", duration_minutes=10, task_type="feed")
    t2 = Task(title="Morning walk", duration_minutes=30, task_type="walk")
    t3 = Task(title="Play fetch", duration_minutes=20, task_type="play")

    assert t1.priority == "high"
    assert t2.priority == "medium"
    assert t3.priority == "low"


def test_task_priority_order_in_schedule():
    from pawpal_system import Schedule, Owner, Pet, Task

    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    schedule = Schedule(owner=owner, pet=pet)

    schedule.add_task(Task(title="Play fetch", duration_minutes=20, priority="low"))
    schedule.add_task(Task(title="Morning walk", duration_minutes=30, priority="medium"))
    schedule.add_task(Task(title="Dog feed", duration_minutes=10, priority="high"))

    plan = schedule.build_plan()

    assert [t.title for t in plan] == ["Dog feed", "Morning walk", "Play fetch"]
    assert schedule.plan_slots[0]["start"] == "8:00 AM"
    assert schedule.plan_slots[0]["end"] == "8:10 AM"
    assert schedule.plan_slots[1]["start"] == "8:10 AM"
    assert schedule.plan_slots[1]["end"] == "8:40 AM"
    assert schedule.plan_slots[2]["start"] == "8:40 AM"
    assert schedule.plan_slots[2]["end"] == "9:00 AM"


def test_task_sorting_by_time():
    from pawpal_system import Schedule, Owner, Pet, Task

    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    schedule = Schedule(owner=owner, pet=pet)

    schedule.add_task(Task(title="Play fetch", duration_minutes=20, priority="low"))
    schedule.add_task(Task(title="Morning walk", duration_minutes=30, priority="medium"))
    schedule.add_task(Task(title="Dog feed", duration_minutes=10, priority="high"))

    plan = schedule.build_plan()
    sorted_slots = schedule.get_tasks_sorted_by_time()

    assert len(sorted_slots) == 3
    assert sorted_slots[0]["title"] == "Dog feed"
    assert sorted_slots[1]["title"] == "Morning walk"
    assert sorted_slots[2]["title"] == "Play fetch"


def test_filter_tasks_by_pet():
    from pawpal_system import Schedule, Owner, Pet, Task

    owner = Owner(name="Jordan")
    pet1 = Pet(name="Mochi", species="dog")
    pet2 = Pet(name="Luna", species="cat")
    schedule = Schedule(owner=owner, pet=pet1)

    task1 = Task(title="Dog feed", duration_minutes=10, task_type="feed", pet_name="Mochi")
    task2 = Task(title="Cat feed", duration_minutes=10, task_type="feed", pet_name="Luna")
    task3 = Task(title="General play", duration_minutes=15, task_type="play", pet_name=None)

    schedule.add_task(task1)
    schedule.add_task(task2)
    schedule.add_task(task3)

    mochi_tasks = schedule.filter_tasks_by_pet("Mochi")
    assert len(mochi_tasks) == 2  # Dog feed + General play (pet_name=None)
    assert task1 in mochi_tasks
    assert task3 in mochi_tasks
    assert task2 not in mochi_tasks


def test_filter_tasks_by_status():
    from pawpal_system import Schedule, Owner, Pet, Task

    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    schedule = Schedule(owner=owner, pet=pet)

    task1 = Task(title="Dog feed", duration_minutes=10, task_type="feed")
    task2 = Task(title="Morning walk", duration_minutes=30, task_type="walk")
    task3 = Task(title="Play fetch", duration_minutes=20, task_type="play")

    task1.mark_complete()

    schedule.add_task(task1)
    schedule.add_task(task2)
    schedule.add_task(task3)

    completed = schedule.filter_tasks_by_status(completed=True)
    incomplete = schedule.filter_tasks_by_status(completed=False)

    assert len(completed) == 1
    assert task1 in completed
    assert len(incomplete) == 2
    assert task2 in incomplete
    assert task3 in incomplete


def test_recurring_task_creation():
    from pawpal_system import RecurringTask
    from datetime import date

    start = date(2026, 3, 29)
    rt = RecurringTask(
        title="Daily feeding",
        duration_minutes=10,
        task_type="feed",
        recurrence_pattern="daily",
        start_date=start
    )

    assert rt.title == "Daily feeding"
    assert rt.recurrence_pattern == "daily"
    assert rt.is_active_on_date(start)
    assert rt.is_active_on_date(date(2026, 3, 30))


def test_recurring_task_weekly_pattern():
    from pawpal_system import RecurringTask
    from datetime import date

    start = date(2026, 3, 29)  # Sunday (weekday=6)
    rt = RecurringTask(
        title="Weekday walk",
        duration_minutes=30,
        task_type="walk",
        recurrence_pattern="weekly",
        recurrence_days={0, 1, 2, 3, 4},  # Monday-Friday
        start_date=start
    )

    # Sunday (weekday=6) should not match (not in recurrence_days)
    assert not rt.is_active_on_date(start)
    # Monday (weekday=0) should match
    assert rt.is_active_on_date(date(2026, 3, 30))
    # Saturday (weekday=5) should not match
    assert not rt.is_active_on_date(date(2026, 3, 28))


def test_recurring_task_occurrences():
    from pawpal_system import RecurringTask
    from datetime import date

    start = date(2026, 3, 29)
    end = date(2026, 4, 2)
    rt = RecurringTask(
        title="Daily feed",
        duration_minutes=10,
        task_type="feed",
        recurrence_pattern="daily",
        start_date=start,
        end_date=end
    )

    occurrences = rt.get_occurrences_in_range(start, end)
    assert len(occurrences) == 5  # 5 days from Mar 29 to Apr 2


def test_conflict_detection():
    from pawpal_system import Schedule, Owner, Pet, Task

    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    schedule = Schedule(owner=owner, pet=pet)

    # Manually create plan slots with overlapping times
    schedule.plan = []
    schedule.plan_slots = [
        {"title": "Feed", "start": "8:00 AM", "end": "8:15 AM", "duration_minutes": 15},
        {"title": "Walk", "start": "8:10 AM", "end": "8:40 AM", "duration_minutes": 30},  # Overlaps with Feed
        {"title": "Play", "start": "9:00 AM", "end": "9:20 AM", "duration_minutes": 20},
    ]

    conflicts = schedule.detect_conflicts()
    assert len(conflicts) == 1
    assert conflicts[0]["task1"] == "Feed"
    assert conflicts[0]["task2"] == "Walk"


def test_daily_task_summary():
    from pawpal_system import Schedule, Owner, Pet, Task

    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    schedule = Schedule(owner=owner, pet=pet)

    schedule.add_task(Task(title="Dog feed", duration_minutes=10, task_type="feed"))
    schedule.add_task(Task(title="Morning walk", duration_minutes=30, task_type="walk"))

    plan = schedule.build_plan()
    summary = schedule.get_daily_task_summary()

    assert summary["total_tasks"] == 2
    assert summary["completed_tasks"] == 0
    assert summary["remaining_tasks"] == 2
    assert summary["total_duration_minutes"] == 40


def test_recurring_task_mark_complete_daily():
    """Test that marking a daily recurring task complete creates the next day's task."""
    from pawpal_system import RecurringTask, Schedule, Owner, Pet
    from datetime import date

    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    schedule = Schedule(owner=owner, pet=pet)

    today = date.today()
    rt = RecurringTask(
        title="Daily feeding",
        duration_minutes=10,
        task_type="feed",
        pet_name="Mochi",
        recurrence_pattern="daily",
        start_date=today,
        due_date=today
    )

    schedule.add_task(rt)
    
    # Mark complete using schedule method
    next_task = schedule.complete_task(rt)

    # Verify original task is marked complete
    assert rt.completed
    assert rt.last_completed_date == today

    # Verify next task was created and added
    assert next_task is not None
    assert isinstance(next_task, RecurringTask)
    assert next_task.due_date == today + timedelta(days=1)
    assert not next_task.completed
    assert next_task.title == "Daily feeding"

    # Verify next task is in schedule
    assert len(schedule.tasks) == 2
    assert next_task in schedule.tasks


def test_recurring_task_mark_complete_weekly():
    """Test that marking a weekly recurring task complete creates the next occurrence."""
    from pawpal_system import RecurringTask, Schedule, Owner, Pet
    from datetime import date

    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    schedule = Schedule(owner=owner, pet=pet)

    # Use a specific Monday for testing
    monday = date(2026, 3, 30)  # This is a Monday
    
    rt = RecurringTask(
        title="Weekly grooming",
        duration_minutes=30,
        task_type="play",
        pet_name="Mochi",
        recurrence_pattern="weekly",
        recurrence_days={0},  # Monday only
        start_date=monday,
        due_date=monday
    )

    schedule.add_task(rt)
    next_task = schedule.complete_task(rt)

    # Verify original task is marked complete
    assert rt.completed

    # Verify next task is created with date after current due_date
    assert next_task is not None
    assert isinstance(next_task, RecurringTask)
    assert next_task.due_date.weekday() == 0  # Next is also Monday
    assert next_task.due_date > rt.due_date  # Next is definitely after current
    assert (next_task.due_date - rt.due_date).days == 7  # Exactly 7 days later


def test_recurring_task_end_date_stops_recurrence():
    """Test that when recurrence end date is reached, no new task is created."""
    from pawpal_system import RecurringTask, Schedule, Owner, Pet
    from datetime import date

    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    schedule = Schedule(owner=owner, pet=pet)

    today = date.today()
    
    rt = RecurringTask(
        title="Temporary daily task",
        duration_minutes=10,
        task_type="feed",
        pet_name="Mochi",
        recurrence_pattern="daily",
        start_date=today,
        end_date=today,  # End date is today, so no next occurrence
        due_date=today
    )

    schedule.add_task(rt)
    next_task = schedule.complete_task(rt)

    # Verify original task is marked complete
    assert rt.completed

    # Verify NO next task is created (recurrence ended)
    assert next_task is None
    assert len(schedule.tasks) == 1  # Only original, no new one


def test_get_next_occurrence_daily():
    """Test get_next_occurrence for daily pattern."""
    from pawpal_system import RecurringTask
    from datetime import date

    today = date.today()
    rt = RecurringTask(
        title="Daily feed",
        duration_minutes=10,
        task_type="feed",
        recurrence_pattern="daily",
        start_date=today,
        end_date=today + timedelta(days=10),
        due_date=today
    )

    next_date = rt.get_next_occurrence(today)
    assert next_date == today + timedelta(days=1)

    # Test multiple days ahead
    next_next_date = rt.get_next_occurrence(today + timedelta(days=1))
    assert next_next_date == today + timedelta(days=2)


def test_get_next_occurrence_weekly():
    """Test get_next_occurrence for weekly pattern."""
    from pawpal_system import RecurringTask
    from datetime import date

    # Start on Monday
    monday = date(2026, 3, 30)  # A Monday
    
    rt = RecurringTask(
        title="Weekly walk",
        duration_minutes=30,
        task_type="walk",
        recurrence_pattern="weekly",
        recurrence_days={0, 3},  # Monday and Thursday
        start_date=monday,
        due_date=monday
    )

    # From Monday, next should be Thursday
    thursday = rt.get_next_occurrence(monday)
    assert thursday.weekday() == 3  # Thursday

    # From Thursday, next should be next Monday (7 days)
    next_monday = rt.get_next_occurrence(thursday)
    assert next_monday.weekday() == 0  # Monday


def test_complete_task_regular_task():
    """Test complete_task with a regular (non-recurring) Task."""
    from pawpal_system import Task, Schedule, Owner, Pet

    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    schedule = Schedule(owner=owner, pet=pet)

    task = Task(title="One-time walk", duration_minutes=30, task_type="walk")
    schedule.add_task(task)

    # Complete regular task
    result = schedule.complete_task(task)

    # Verify task is marked complete
    assert task.completed

    # Verify no new task created (not recurring)
    assert result is None
    assert len(schedule.tasks) == 1
