from dataclasses import dataclass, field
from datetime import date
from typing import List, Dict, Optional

@dataclass
class Owner:
    name: str
    contact: Optional[str] = None
    preferences: Dict[str, str] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)
    pet_task_times: Dict[str, Dict[str, str]] = field(default_factory=dict)

    def add_preference(self, key: str, value: str) -> None:
        """Store an owner preference key-value pair."""
        self.preferences[key] = value

    def update_name(self, new_name: str) -> None:
        """Update the owner's name."""
        self.name = new_name

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        if not isinstance(pet, Pet):
            raise ValueError("Can only add Pet instances")
        if any(existing.name == pet.name for existing in self.pets):
            raise ValueError(f"Pet with name '{pet.name}' already exists")
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet and its task times by pet name."""
        self.pets = [pet for pet in self.pets if pet.name != pet_name]
        self.pet_task_times.pop(pet_name, None)

    @staticmethod
    def _normalize_time_str(time_str: str) -> str:
        """Convert a string to normalized 12-hour time with AM/PM."""
        if not isinstance(time_str, str) or not time_str.strip():
            raise ValueError("time_str must be a non-empty string in 12-hour format, e.g. '5:00 PM'")

        normalized = time_str.strip().upper().replace(" ", "")
        if normalized.endswith("AM") or normalized.endswith("PM"):
            # add colon if missing
            raw = normalized[:-2]
            suffix = normalized[-2:]
            if ":" not in raw:
                raw = raw + ":00"
            try:
                from datetime import datetime
                dt = datetime.strptime(raw + suffix, "%I:%M%p")
                return dt.strftime("%I:%M %p").lstrip('0')
            except ValueError:
                raise ValueError("time_str must be in 12-hour format, e.g. '5:00 PM' or '5 PM'")

        raise ValueError("time_str must include AM or PM, e.g. '5:00 PM'.")

    def set_pet_task_time(self, pet_name: str, task_type: str, time_str: str) -> None:
        """Set preferred time for a specific pet task type."""
        if pet_name not in [pet.name for pet in self.pets]:
            raise ValueError(f"Pet '{pet_name}' is not owned by {self.name}")

        task_type = task_type.strip().lower()
        if task_type not in {"feed", "walk", "play"}:
            raise ValueError("task_type must be one of: feed, walk, play")

        normalized_time = self._normalize_time_str(time_str)

        if pet_name not in self.pet_task_times:
            self.pet_task_times[pet_name] = {}

        self.pet_task_times[pet_name][task_type] = normalized_time

    def get_pet_task_time(self, pet_name: str, task_type: str) -> Optional[str]:
        """Get preferred time for a specific pet task type."""
        return self.pet_task_times.get(pet_name, {}).get(task_type)

@dataclass
class Pet:
    name: str
    species: str
    breed: Optional[str] = None
    food_type: Optional[str] = None

    ALLOWED_SPECIES = {"dog", "cat", "other"}

    def __post_init__(self) -> None:
        """Validate pet fields after initialization."""
        self._validate_name(self.name)
        self._validate_species(self.species)

    @staticmethod
    def _validate_name(name: str) -> None:
        """Validate that pet name is non-empty."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Pet name must be a non-empty string")

    @classmethod
    def _validate_species(cls, species: str) -> None:
        """Validate that species is one of allowed values."""
        if not isinstance(species, str) or species.strip().lower() not in cls.ALLOWED_SPECIES:
            raise ValueError(f"Species must be one of: {', '.join(sorted(cls.ALLOWED_SPECIES))}")

    def update_name(self, new_name: str) -> None:
        """Update pet name with validation."""
        self._validate_name(new_name)
        self.name = new_name.strip()

    def update_species(self, new_species: str) -> None:
        """Update pet species with validation."""
        self._validate_species(new_species)
        self.species = new_species.strip().lower()

    def set_breed(self, breed: Optional[str]) -> None:
        """Set or clear pet breed."""
        self.breed = breed.strip() if isinstance(breed, str) and breed.strip() else None

    def set_food_type(self, food_type: str) -> None:
        """Set pet food type with validation."""
        if not isinstance(food_type, str) or not food_type.strip():
            raise ValueError("Food type must be a non-empty string")
        self.food_type = food_type.strip()

@dataclass
class Task:
    title: str
    duration_minutes: int
    task_type: Optional[str] = None
    priority: str = "medium"
    notes: Optional[str] = None
    completed: bool = False

    ALLOWED_PRIORITIES = {"low", "medium", "high"}
    ALLOWED_TASK_TYPES = {"feed", "walk", "play"}
    TASK_TYPE_DEFAULT_PRIORITY = {"feed": "high", "walk": "medium", "play": "low"}

    def __post_init__(self) -> None:
        """Initialize and validate task fields, with type-based default priority."""
        self._validate_title(self.title)
        self._validate_duration(self.duration_minutes)

        # Determine type and fallback default priority based on task type
        if self.task_type is None:
            self.task_type = self._determine_task_type(self.title)
        else:
            self.task_type = self.task_type.strip().lower()
            self._validate_task_type(self.task_type)

        # If priority is unspecified or default medium, inherit from task type
        requested_priority = self.priority.strip().lower() if isinstance(self.priority, str) else "medium"
        if requested_priority == "medium":
            self.priority = self.TASK_TYPE_DEFAULT_PRIORITY.get(self.task_type, "medium")

        self._validate_priority(self.priority)

    @staticmethod
    def _validate_title(title: str) -> None:
        """Validate that task title is not empty."""
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Task title must be a non-empty string")

    @staticmethod
    def _validate_duration(duration: int) -> None:
        """Validate task duration is a positive integer."""
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError("Duration must be a positive integer")

    @classmethod
    def _validate_priority(cls, priority: str) -> None:
        """Validate priority value is low/medium/high."""
        if not isinstance(priority, str) or priority.strip().lower() not in cls.ALLOWED_PRIORITIES:
            raise ValueError(f"Priority must be one of: {', '.join(sorted(cls.ALLOWED_PRIORITIES))}")

    @classmethod
    def _validate_task_type(cls, task_type: str) -> None:
        """Validate task type is feed/walk/play."""
        if not isinstance(task_type, str) or task_type.strip().lower() not in cls.ALLOWED_TASK_TYPES:
            raise ValueError(f"Task type must be one of: {', '.join(sorted(cls.ALLOWED_TASK_TYPES))}")

    @classmethod
    def _determine_task_type(cls, title: str) -> str:
        """Infer type from task title if type not given."""
        lower = title.strip().lower()
        for keyword in cls.ALLOWED_TASK_TYPES:
            if keyword in lower:
                return keyword
        raise ValueError(f"Task title must indicate type: {', '.join(sorted(cls.ALLOWED_TASK_TYPES))}")

    def set_duration(self, minutes: int) -> None:
        """Set a new duration with validation."""
        self._validate_duration(minutes)
        self.duration_minutes = minutes

    def set_priority(self, priority: str) -> None:
        """Update task priority with validation."""
        self._validate_priority(priority)
        self.priority = priority.strip().lower()

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    TASK_TYPE_PRIORITY = {
        "feed": 0,
        "walk": 1,
        "play": 2,
    }

    def add_notes(self, notes: str) -> None:
        if not isinstance(notes, str):
            raise ValueError("Notes must be a string")
        self.notes = notes.strip()

    def get_type_priority(self) -> int:
        """Get numeric priority based on task type for sorting."""
        task_type = (self.task_type or "").strip().lower()
        if task_type in self.TASK_TYPE_PRIORITY:
            return self.TASK_TYPE_PRIORITY[task_type]
        # Fallback to title scanning for compatibility
        title_lower = self.title.strip().lower()
        for key, value in self.TASK_TYPE_PRIORITY.items():
            if key in title_lower:
                return value
        return max(self.TASK_TYPE_PRIORITY.values()) + 1

    def get_duration_priority(self) -> int:
        """Provide duration-based prioritization score for task ranking."""
        # shorter tasks are prioritized for schedule fit, but longer tasks can be prioritized by impact
        if self.duration_minutes <= 15:
            return 0
        if self.duration_minutes <= 30:
            return 1
        if self.duration_minutes <= 60:
            return 2
        return 3

    def get_effective_priority_score(self) -> int:
        """Calculate a combined priority score used for scheduling sort order."""
        base = {"high": 0, "medium": 3, "low": 6}
        p = self.priority.strip().lower()
        base_score = base.get(p, 3)
        type_score = self.get_type_priority()
        duration_score = self.get_duration_priority()
        return base_score + type_score + duration_score

@dataclass
class Constraint(Task):
    reason: Optional[str] = None
    impact_level: Optional[str] = None  # e.g. mild|moderate|severe

    def describe(self) -> str:
        return f"Constraint: {self.title} ({self.duration_minutes}m) - {self.reason or 'no reason'}"

@dataclass
class Schedule:
    owner: Owner
    pet: Pet
    tasks: List[Task] = field(default_factory=list)
    constraints: List[Constraint] = field(default_factory=list)
    date: date = field(default_factory=date.today)
    plan: List[Task] = field(default_factory=list)
    plan_slots: List[Dict[str, str]] = field(default_factory=list)
    daily_available_minutes: int = 8 * 60

    @staticmethod
    def _format_time(total_minutes: int) -> str:
        """Convert minute offset to a formatted 12-hour clock time."""
        hours = (total_minutes // 60) % 24
        minutes = total_minutes % 60
        suffix = "AM" if hours < 12 else "PM"
        display_hour = hours % 12
        if display_hour == 0:
            display_hour = 12
        return f"{display_hour}:{minutes:02d} {suffix}"

    def set_date(self, schedule_date: date) -> None:
        """Set schedule date."""
        self.date = schedule_date

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule."""
        self.tasks.append(task)

    def add_constraint(self, constraint: Constraint) -> None:
        """Add a time constraint to the schedule."""
        self.constraints.append(constraint)

    def available_minutes(self) -> int:
        """Return available minutes after deducting constraints."""
        used_by_constraints = sum(c.duration_minutes for c in self.constraints)
        available = self.daily_available_minutes - used_by_constraints
        return max(0, available)

    def build_plan(self, start_hour: int = 8, start_minute: int = 0) -> List[Task]:
        """Generate task plan and timeslots based on available time and priority."""
        self.plan = []
        self.plan_slots = []

        available = self.available_minutes()
        if available <= 0:
            return self.plan

        sorted_tasks = sorted(
            self.tasks,
            key=lambda t: (t.get_effective_priority_score(), t.duration_minutes)
        )

        current_time = start_hour * 60 + start_minute
        used = 0

        for task in sorted_tasks:
            if used + task.duration_minutes <= available:
                start = current_time
                end = current_time + task.duration_minutes

                self.plan.append(task)
                self.plan_slots.append({
                    "title": task.title,
                    "start": self._format_time(start),
                    "end": self._format_time(end),
                    "duration_minutes": task.duration_minutes,
                })

                used += task.duration_minutes
                current_time = end
            else:
                continue

        return self.plan

    def explain_plan(self) -> str:
        """Return a human-readable explanation of the schedule and constraints."""
        if not self.plan:
            remaining = self.available_minutes()
            if remaining == 0:
                return "No available time after constraints."
            return "No plan generated yet."

        plan_desc = "\n".join(
            f"{i+1}. {slot['title']} ({slot['duration_minutes']}m) "
            f"[{slot['start']} - {slot['end']}]"
            for i, slot in enumerate(self.plan_slots)
        )
        constraints_desc = "\n".join(c.describe() for c in self.constraints) or "No constraints."
        return f"Constraints:\n{constraints_desc}\n\nPlan:\n{plan_desc}"

class DisplayChart:
    """Render schedule as human-readable chart text."""

    def __init__(self, schedule: Schedule):
        """Create a display wrapper for a schedule."""
        self.schedule = schedule

    def display(self) -> str:
        """Return full chart display (table + explanation)."""
        table = self.render_table()
        explain = self.render_explanation()
        return f"{table}\n\n{explain}"

    def render_table(self) -> str:
        if not self.schedule.plan_slots:
            return "No schedule to display."

        header = f"Schedule for {self.schedule.date.isoformat()}"
        lines = [header, "Time | Task"]
        lines.append("-----|------")

        for slot in self.schedule.plan_slots:
            task_status = " ✅" if slot.get("completed") else ""
            text = f"{slot['start']} - {slot['end']} | {slot['title']} ({slot['duration_minutes']}m){task_status}"
            lines.append(text)

        return "\n".join(lines)

    def render_explanation(self) -> str:
        """Return the schedule explanation text."""
        return self.schedule.explain_plan()
