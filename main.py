from pawpal_system import Owner, Pet, Task, Schedule, DisplayChart


def main():
    # Setup owner and pets
    owner = Owner(name="Jordan", contact="jordan@example.com")
    pet1 = Pet(name="Mochi", species="dog", breed="Shiba")
    pet2 = Pet(name="Luna", species="cat")

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # Set preferred task times (optional, for reference)
    owner.set_pet_task_time("Mochi", "feed", "7:30 AM")
    owner.set_pet_task_time("Mochi", "walk", "8:00 AM")
    owner.set_pet_task_time("Luna", "feed", "8:00 AM")

    # Build tasks OUT OF ORDER to demonstrate sorting
    print("=" * 70)
    print("ADDING TASKS OUT OF ORDER")
    print("=" * 70)
    
    tasks = [
        Task(title="Play fetch", duration_minutes=20, task_type="play", priority="low", pet_name="Mochi"),
        Task(title="Morning walk", duration_minutes=30, task_type="walk", priority="medium", pet_name="Mochi"),
        Task(title="Cat feed", duration_minutes=10, task_type="feed", priority="high", pet_name="Luna"),
        Task(title="Dog feed", duration_minutes=10, task_type="feed", priority="high", pet_name="Mochi"),
    ]
    
    # Print tasks in the order they were added
    print("\nTasks added in this order:")
    for i, t in enumerate(tasks, 1):
        print(f"  {i}. {t.title} ({t.duration_minutes}m, {t.priority} priority, pet: {t.pet_name})")

    # Create schedule for one pet and add tasks
    schedule = Schedule(owner=owner, pet=pet1)
    for t in tasks:
        schedule.add_task(t)

    # Build the plan (which sorts by priority)
    plan = schedule.build_plan(start_hour=7, start_minute=30)

    # DEMONSTRATION 1: SORTED BY TIME
    print("\n" + "=" * 70)
    print("FEATURE 1: SORTING BY TIME")
    print("=" * 70)
    print("\nSchedule sorted by start time (using lambda function):")
    sorted_slots = schedule.get_tasks_sorted_by_time()
    for i, slot in enumerate(sorted_slots, 1):
        print(f"  {i}. {slot['start']:8} - {slot['end']:8} | {slot['title']:15} ({slot['duration_minutes']:2}m)")

    # DEMONSTRATION 4: CONFLICT DETECTION BY TIME AND PET NAME
    print("\n" + "=" * 70)
    print("FEATURE 4: CONFLICT DETECTION")
    print("=" * 70)

    # Force a same-time schedule conflict (two tasks at exactly the same window)
    schedule.plan_slots.append({
        "title": "Conflict task",
        "start": "7:40 AM",
        "end": "7:50 AM",
        "duration_minutes": 10,
        "pet_name": "Luna"
    })

    schedule.plan_slots.append({
        "title": "Conflict task 2",
        "start": "7:40 AM",
        "end": "7:50 AM",
        "duration_minutes": 10,
        "pet_name": "Mochi"
    })

    warnings = schedule.get_conflict_warnings()
    if warnings:
        print("\nConflict warnings:")
        for w in warnings:
            print(f"  {w}")
    else:
        print("\nNo conflicts detected.")

    # DEMONSTRATION 2: FILTERING BY PET
    print("\n" + "=" * 70)
    print("FEATURE 2: FILTERING BY PET")
    print("=" * 70)
    
    mochi_tasks = schedule.filter_tasks_by_pet("Mochi")
    luna_tasks = schedule.filter_tasks_by_pet("Luna")
    
    print(f"\nTasks for Mochi ({len(mochi_tasks)} tasks):")
    for t in mochi_tasks:
        status = "✓ completed" if t.completed else "○ pending"
        print(f"  • {t.title:20} ({t.duration_minutes}m, {t.priority} priority) [{status}]")
    
    print(f"\nTasks for Luna ({len(luna_tasks)} tasks):")
    for t in luna_tasks:
        status = "✓ completed" if t.completed else "○ pending"
        print(f"  • {t.title:20} ({t.duration_minutes}m, {t.priority} priority) [{status}]")

    # DEMONSTRATION 3: FILTERING BY STATUS
    print("\n" + "=" * 70)
    print("FEATURE 3: FILTERING BY COMPLETION STATUS")
    print("=" * 70)
    
    # Mark some tasks as complete
    print("\nMarking tasks as complete...")
    schedule.tasks[0].mark_complete()  # Play fetch
    schedule.tasks[2].mark_complete()  # Cat feed
    
    completed_tasks = schedule.filter_tasks_by_status(completed=True)
    incomplete_tasks = schedule.filter_tasks_by_status(completed=False)
    
    print(f"\n✓ Completed tasks ({len(completed_tasks)}):")
    for t in completed_tasks:
        print(f"  • {t.title}")
    
    print(f"\n○ Incomplete tasks ({len(incomplete_tasks)}):")
    for t in incomplete_tasks:
        print(f"  • {t.title}")

    # FINAL DISPLAY
    print("\n" + "=" * 70)
    print("TODAY'S SCHEDULE")
    print("=" * 70)
    print(DisplayChart(schedule).display())


if __name__ == "__main__":
    main()
