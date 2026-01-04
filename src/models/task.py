from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class Priority(str, Enum):
    """Priority levels for tasks"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Task:
    """Represents a single todo item with attributes including title, description, priority level, completion status, and creation date"""

    def __init__(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        completed: bool = False,
        task_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        # Validate title
        if not title or len(title) > 200:
            raise ValueError("Title must be between 1 and 200 characters")

        # Validate description
        if len(description) > 1000:
            raise ValueError("Description must be 1000 characters or less")

        # Validate priority
        if priority not in [Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
            raise ValueError("Priority must be one of: 'high', 'medium', 'low'")

        self.id = task_id or str(uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = completed
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def mark_completed(self):
        """Mark the task as completed and update the timestamp"""
        self.completed = True
        self.updated_at = datetime.now()

    def update(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority] = None,
        completed: Optional[bool] = None
    ):
        """Update task attributes and update the timestamp"""
        if title is not None:
            if not title or len(title) > 200:
                raise ValueError("Title must be between 1 and 200 characters")
            self.title = title

        if description is not None:
            if len(description) > 1000:
                raise ValueError("Description must be 1000 characters or less")
            self.description = description

        if priority is not None:
            if priority not in [Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
                raise ValueError("Priority must be one of: 'high', 'medium', 'low'")
            self.priority = priority

        if completed is not None:
            self.completed = completed

        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """Convert the task to a dictionary representation"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create a Task instance from a dictionary representation"""
        return cls(
            task_id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            priority=Priority(data["priority"]),
            completed=data.get("completed", False),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
        )

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title='{self.title}', priority={self.priority}, completed={self.completed})"