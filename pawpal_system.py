from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Dict, Optional, Set, Tuple

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
    pet_name: Optional[str] = None  # Track which pet this task belongs to

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
        # Use explicit priority order instead of set to ensure deterministic behavior
        priority_order = ["feed", "walk", "play"]
        for keyword in priority_order:
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
class RecurringTask(Task):
    """Task that repeats on a schedule."""
    recurrence_pattern: str = "daily"  # daily, weekly, custom
    recurrence_days: Set[int] = field(default_factory=lambda: {0, 1, 2, 3, 4, 5, 6})  # 0=Mon, 6=Sun
    start_date: date = field(default_factory=date.today)
    end_date: Optional[date] = None
    due_date: Optional[date] = field(default_factory=date.today)  # When this instance is due
    last_completed_date: Optional[date] = None  # Track when this was last completed

    ALLOWED_PATTERNS = {"daily", "weekly", "custom"}

    def __post_init__(self) -> None:
        """Initialize recurring task with validation."""
        super().__post_init__()
        if self.recurrence_pattern not in self.ALLOWED_PATTERNS:
            raise ValueError(f"Recurrence pattern must be one of: {', '.join(self.ALLOWED_PATTERNS)}")
        if self.end_date and self.end_date < self.start_date:
            raise ValueError("End date cannot be before start date")
        # Set due_date to start_date if not provided
        if self.due_date is None:
            self.due_date = self.start_date

    def is_active_on_date(self, check_date: date) -> bool:
        """Check if this recurring task is active on a given date."""
        if check_date < self.start_date:
            return False
        if self.end_date and check_date > self.end_date:
            return False
        
        if self.recurrence_pattern == "daily":
            return True
        elif self.recurrence_pattern == "weekly":
            return check_date.weekday() in self.recurrence_days
        return False

    def get_occurrences_in_range(self, start: date, end: date) -> List[date]:
        """Get all dates this task occurs within a date range."""
        occurrences = []
        current = max(start, self.start_date)
        end_check = min(end, self.end_date) if self.end_date else end
        
        while current <= end_check:
            if self.is_active_on_date(current):
                occurrences.append(current)
            current += timedelta(days=1)
        
        return occurrences

    def get_next_occurrence(self, after: date) -> Optional[date]:
        """Get the next occurrence date after a given date using timedelta.
        
        For daily tasks: next = after + timedelta(days=1)
        For weekly tasks: find next matching weekday after 'after' date
        
        Args:
            after: Search for next occurrence after this date
            
        Returns None if past end_date.
        """
        if self.end_date and after >= self.end_date:
            return None
        
        if self.recurrence_pattern == "daily":
            # Simple: next day is tomorrow from 'after'
            next_date = after + timedelta(days=1)
            if self.end_date and next_date > self.end_date:
                return None
            return next_date
        
        elif self.recurrence_pattern == "weekly":
            # Find next matching weekday after the 'after' date
            check_date = after + timedelta(days=1)
            # Search up to 7 days to find next matching weekday
            for _ in range(7):
                if self.end_date and check_date > self.end_date:
                    return None
                if check_date.weekday() in self.recurrence_days:
                    return check_date
                check_date += timedelta(days=1)
            return None
        
        return None

    def mark_complete(self) -> Optional['RecurringTask']:
        """Mark this task as completed and return a new instance for next occurrence.
        
        Returns a new RecurringTask for the next occurrence, or None if recurrence ended.
        The original task is marked completed, and a new task is created with:
        - Same title, duration, priority, etc.
        - due_date set to the next occurrence
        - completed=False
        - last_completed_date set to today
        
        Uses the task's due_date (not today) to calculate next occurrence for accuracy.
        """
        # Mark this instance as completed
        self.completed = True
        self.last_completed_date = date.today()
        
        # Get next occurrence date using this task's due_date
        # This ensures weekly tasks find the next matching weekday from their scheduled date
        next_date = self.get_next_occurrence(self.due_date)
        
        # If no next occurrence, return None (recurrence ended)
        if next_date is None:
            return None
        
        # Create new instance for next occurrence
        next_task = RecurringTask(
            title=self.title,
            duration_minutes=self.duration_minutes,
            task_type=self.task_type,
            priority=self.priority,
            notes=self.notes,
            completed=False,
            pet_name=self.pet_name,
            recurrence_pattern=self.recurrence_pattern,
            recurrence_days=self.recurrence_days.copy(),  # Copy the set
            start_date=self.start_date,
            end_date=self.end_date,
            due_date=next_date,
            last_completed_date=None
        )
        
        return next_task

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
                    "pet_name": task.pet_name,
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

    def get_tasks_sorted_by_time(self) -> List[Dict[str, str]]:
        """Return plan slots sorted by start time using lambda key function.
        
        The lambda converts HH:MM format times to minutes for numeric comparison:
        lambda slot: self._time_to_minutes(slot['start'])
        
        This approach handles 12-hour format (7:30 AM, 2:15 PM, etc.) by:
        1. Parsing the time string into hours and minutes
        2. Converting to total minutes (hour*60 + minute)
        3. Using numeric values for sorting (much simpler than string comparison)
        """
        # Already sorted by build_plan, but re-sort to ensure consistency
        return sorted(self.plan_slots, key=lambda slot: self._time_to_minutes(slot['start']))

    @staticmethod
    def _time_to_minutes(time_str: str) -> int:
        """Convert time string like '7:30 AM' to minutes since midnight."""
        from datetime import datetime
        dt = datetime.strptime(time_str, "%I:%M %p")
        return dt.hour * 60 + dt.minute

    def filter_tasks_by_pet(self, pet_name: str) -> List[Task]:
        """Filter and return all tasks for a specific pet.
        
        Uses list comprehension for efficient filtering:
        [t for t in self.tasks if t.pet_name == pet_name or t.pet_name is None]
        
        Design: Tasks with pet_name=None are included for any pet (universal tasks).
        """
        return [t for t in self.tasks if t.pet_name == pet_name or t.pet_name is None]

    def filter_tasks_by_status(self, completed: bool = True) -> List[Task]:
        """Filter tasks by completion status.
        
        Args:
            completed (bool): If True, return completed tasks; if False, return incomplete tasks
            
        Returns:
            List of tasks matching the completion status
        """
        return [t for t in self.tasks if t.completed == completed]

    def filter_plan_by_status(self, completed: bool = True) -> List[Dict[str, str]]:
        """Return scheduled slots filtered by completion status."""
        for slot in self.plan_slots:
            if "completed" not in slot:
                slot["completed"] = False
        return [s for s in self.plan_slots if s.get("completed", False) == completed]

    def detect_conflicts(self) -> List[Dict[str, object]]:
        """Detect overlapping tasks in the current plan. Returns list of conflict dicts."""
        conflicts = []
        
        for i, slot1 in enumerate(self.plan_slots):
            for slot2 in self.plan_slots[i+1:]:
                # Check if slots overlap
                start1 = self._time_to_minutes(slot1['start'])
                end1 = self._time_to_minutes(slot1['end'])
                start2 = self._time_to_minutes(slot2['start'])
                end2 = self._time_to_minutes(slot2['end'])

                if start1 < end2 and start2 < end1:
                    conflict_type = "different pets"
                    pet1, pet2 = slot1.get('pet_name'), slot2.get('pet_name')
                    if pet1 and pet2 and pet1 == pet2:
                        conflict_type = "same pet"

                    conflicts.append({
                        "task1": slot1['title'],
                        "task2": slot2['title'],
                        "pet1": pet1,
                        "pet2": pet2,
                        "time1": f"{slot1['start']} - {slot1['end']}",
                        "time2": f"{slot2['start']} - {slot2['end']}",
                        "conflict_type": conflict_type,
                        "overlap_description": f"'{slot1['title']}' and '{slot2['title']}' overlap in schedule"
                    })
        
        return conflicts

    def get_conflict_warnings(self) -> List[str]:
        """Return lightweight conflict warnings (no exceptions)."""
        warnings = []
        for c in self.detect_conflicts():
            if c['conflict_type'] == 'same pet':
                warnings.append(
                    f"WARNING: Same pet '{c['pet1']}' has overlapping tasks '{c['task1']}' "
                    f"and '{c['task2']}' at {c['time1']} / {c['time2']}"
                )
            else:
                warnings.append(
                    f"WARNING: Tasks for different pets ('{c['pet1']}'/'{c['pet2']}') overlap: "
                    f"'{c['task1']}' and '{c['task2']}' at {c['time1']} / {c['time2']}"
                )
        return warnings

    def get_daily_task_summary(self) -> Dict[str, object]:
        """Return a summary of the day's schedule with conflicts and status."""
        summary = {
            "date": str(self.date),
            "total_tasks": len(self.plan),
            "completed_tasks": sum(1 for t in self.plan if t.completed),
            "remaining_tasks": sum(1 for t in self.plan if not t.completed),
            "total_duration_minutes": sum(t.duration_minutes for t in self.plan),
            "conflicts_detected": self.detect_conflicts(),
            "available_time_minutes": self.available_minutes()
        }
        return summary

    def complete_task(self, task: Task) -> Optional[Task]:
        """Complete a task and auto-create next occurrence if it's recurring.
        
        For RecurringTask: marks complete, creates and adds next occurrence to schedule.
        For regular Task: marks complete.
        
        Args:
            task: The task to complete
            
        Returns:
            The next RecurringTask instance if created, otherwise None
        """
        if isinstance(task, RecurringTask):
            # Mark complete and get next occurrence
            next_task = task.mark_complete()
            
            if next_task:
                # Auto-add next occurrence to the schedule
                self.add_task(next_task)
                return next_task
            else:
                # Recurrence has ended, just mark complete (already done in mark_complete)
                return None
        else:
            # Regular task, just mark complete
            task.mark_complete()
            return None

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
