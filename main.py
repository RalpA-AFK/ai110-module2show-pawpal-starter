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

    # Build tasks
    tasks = [
        Task(title="Dog feed", duration_minutes=10, task_type="feed", priority="high"),
        Task(title="Morning walk", duration_minutes=30, task_type="walk", priority="medium"),
        Task(title="Play fetch", duration_minutes=20, task_type="play", priority="low"),
        Task(title="Cat feed", duration_minutes=10, task_type="feed", priority="high"),
    ]

    # Create schedule for one pet and add tasks
    schedule = Schedule(owner=owner, pet=pet1)
    for t in tasks:
        schedule.add_task(t)

    plan = schedule.build_plan(start_hour=7, start_minute=30)

    # Print results
    print("Today's Schedule")
    print("===============")
    print(DisplayChart(schedule).display())

    print("\nDetailed plan slots:")
    for slot in schedule.plan_slots:
        print(f"- {slot['start']} to {slot['end']}: {slot['title']} ({slot['duration_minutes']}m)")


if __name__ == "__main__":
    main()
