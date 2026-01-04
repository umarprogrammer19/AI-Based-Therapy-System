from typing import List, Optional
from src.models.task import Task, Priority
from src.lib.storage import Storage


class TaskService:
    """Task management logic (CRUD operations)"""

    def __init__(self, storage: Storage = None):
        self.storage = storage or Storage()

    def create_task(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        completed: bool = False
    ) -> Task:
        """Create a new task with the given parameters"""
        task = Task(
            title=title,
            description=description,
            priority=priority,
            completed=completed
        )
        tasks = self.storage.load_tasks()
        tasks.append(task)
        self.storage.save_tasks(tasks)
        return task

    def get_task(self, task_id: str) -> Task:
        """Get a task by its ID"""
        tasks = self.storage.load_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        raise ValueError(f"Task with ID {task_id} does not exist")

    def list_tasks(
        self,
        completed: Optional[bool] = None,
        priority: Optional[Priority] = None
    ) -> List[Task]:
        """List tasks with optional filtering by completion status and priority"""
        tasks = self.storage.load_tasks()

        # Apply filters if specified
        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]

        if priority is not None:
            tasks = [task for task in tasks if task.priority == priority]

        return tasks

    def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority] = None,
        completed: Optional[bool] = None
    ) -> Task:
        """Update a task with the given parameters"""
        tasks = self.storage.load_tasks()
        task_found = False

        for i, task in enumerate(tasks):
            if task.id == task_id:
                task.update(
                    title=title,
                    description=description,
                    priority=priority,
                    completed=completed
                )
                tasks[i] = task
                task_found = True
                break

        if not task_found:
            raise ValueError(f"Task with ID {task_id} does not exist")

        self.storage.save_tasks(tasks)
        return tasks[i]

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by its ID"""
        tasks = self.storage.load_tasks()
        original_length = len(tasks)

        tasks = [task for task in tasks if task.id != task_id]

        if len(tasks) == original_length:
            raise ValueError(f"Task with ID {task_id} does not exist")

        self.storage.save_tasks(tasks)
        return True

    def complete_task(self, task_id: str) -> Task:
        """Mark a task as completed"""
        tasks = self.storage.load_tasks()

        for i, task in enumerate(tasks):
            if task.id == task_id:
                task.mark_completed()
                tasks[i] = task
                self.storage.save_tasks(tasks)
                return task

        raise ValueError(f"Task with ID {task_id} does not exist")

    def get_task_statistics(self) -> dict:
        """Get statistics about tasks"""
        tasks = self.storage.load_tasks()
        total = len(tasks)
        completed = len([task for task in tasks if task.completed])
        pending = total - completed

        return {
            "total_count": total,
            "completed_count": completed,
            "pending_count": pending
        }