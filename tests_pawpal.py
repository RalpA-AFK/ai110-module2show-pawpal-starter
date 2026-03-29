import pytest
from pawpal_system import Pet


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
    p = Pet(name="Mochi", species="cat")
    p.update_name("Neko")
    p.update_species("other")
    p.set_breed("Mixed")
    p.set_food_type("wet food")

    assert p.name == "Neko"
    assert p.species == "other"
    assert p.breed == "Mixed"
    assert p.food_type == "wet food"


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
