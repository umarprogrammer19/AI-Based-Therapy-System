import pytest
from src.models.task import Task, Priority
from src.services.task_service import TaskService
from src.lib.storage import Storage


class TestTaskContracts:
    """Contract tests for task operations"""

    def setup_method(self):
        """Set up a fresh TaskService for each test"""
        self.storage = Storage("test_tasks.json")
        self.storage.clear_tasks()  # Ensure clean state
        self.task_service = TaskService(self.storage)

    def test_create_task_contract(self):
        """Contract test for create_task operation"""
        # Test creating a task with all parameters
        title = "Test Task"
        description = "Test Description"
        priority = Priority.HIGH

        task = self.task_service.create_task(
            title=title,
            description=description,
            priority=priority
        )

        # Verify return value is a Task object with correct attributes
        assert isinstance(task, Task)
        assert task.title == title
        assert task.description == description
        assert task.priority == priority
        assert task.completed is False
        assert task.id is not None

        # Verify task was saved to storage
        saved_tasks = self.task_service.list_tasks()
        assert len(saved_tasks) == 1
        saved_task = saved_tasks[0]
        assert saved_task.id == task.id
        assert saved_task.title == task.title

    def test_create_task_with_defaults(self):
        """Test create_task with minimal parameters (defaults should apply)"""
        task = self.task_service.create_task(title="Minimal Task")

        assert task.title == "Minimal Task"
        assert task.description == ""
        assert task.priority == Priority.MEDIUM  # Default priority
        assert task.completed is False

    def test_create_task_invalid_title(self):
        """Test that create_task raises ValueError for invalid titles"""
        with pytest.raises(ValueError):
            self.task_service.create_task(title="")  # Empty title

        with pytest.raises(ValueError):
            self.task_service.create_task(title="A" * 201)  # Too long title

    def test_get_task_contract(self):
        """Contract test for get_task operation"""
        # Create a task first
        created_task = self.task_service.create_task(title="Get Test Task")

        # Retrieve the task
        retrieved_task = self.task_service.get_task(created_task.id)

        # Verify the retrieved task matches the created one
        assert retrieved_task.id == created_task.id
        assert retrieved_task.title == created_task.title
        assert retrieved_task.description == created_task.description
        assert retrieved_task.priority == created_task.priority
        assert retrieved_task.completed == created_task.completed

    def test_get_task_not_found(self):
        """Test that get_task raises ValueError for non-existent task"""
        with pytest.raises(ValueError):
            self.task_service.get_task("non-existent-id")

    def test_list_tasks_contract(self):
        """Contract test for list_tasks operation"""
        # Create multiple tasks
        task1 = self.task_service.create_task(title="Task 1", priority=Priority.HIGH)
        task2 = self.task_service.create_task(title="Task 2", priority=Priority.LOW, completed=True)
        task3 = self.task_service.create_task(title="Task 3", completed=False)

        # Test listing all tasks
        all_tasks = self.task_service.list_tasks()
        assert len(all_tasks) == 3

        # Test filtering by completion status
        completed_tasks = self.task_service.list_tasks(completed=True)
        assert len(completed_tasks) == 1
        assert completed_tasks[0].id == task2.id

        pending_tasks = self.task_service.list_tasks(completed=False)
        assert len(pending_tasks) == 2

        # Test filtering by priority
        high_priority_tasks = self.task_service.list_tasks(priority=Priority.HIGH)
        assert len(high_priority_tasks) == 1
        assert high_priority_tasks[0].id == task1.id

        # Test combined filtering
        completed_high_tasks = self.task_service.list_tasks(completed=True, priority=Priority.HIGH)
        assert len(completed_high_tasks) == 0

    def test_update_task_contract(self):
        """Contract test for update_task operation"""
        # Create a task
        original_task = self.task_service.create_task(
            title="Original Title",
            description="Original Description",
            priority=Priority.LOW
        )

        # Update the task
        updated_task = self.task_service.update_task(
            task_id=original_task.id,
            title="Updated Title",
            description="Updated Description",
            priority=Priority.HIGH,
            completed=True
        )

        # Verify the returned task has updated values
        assert updated_task.id == original_task.id
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"
        assert updated_task.priority == Priority.HIGH
        assert updated_task.completed is True

        # Verify the task was actually updated in storage
        retrieved_task = self.task_service.get_task(original_task.id)
        assert retrieved_task.title == "Updated Title"

    def test_update_task_partial_contract(self):
        """Test updating only some attributes of a task"""
        original_task = self.task_service.create_task(
            title="Original Title",
            description="Original Description",
            priority=Priority.LOW,
            completed=False
        )

        # Update only the title
        updated_task = self.task_service.update_task(
            task_id=original_task.id,
            title="Updated Title"
        )

        # Verify only title changed
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Original Description"  # Unchanged
        assert updated_task.priority == Priority.LOW  # Unchanged
        assert updated_task.completed is False  # Unchanged

    def test_update_task_not_found(self):
        """Test that update_task raises ValueError for non-existent task"""
        with pytest.raises(ValueError):
            self.task_service.update_task(
                task_id="non-existent-id",
                title="New Title"
            )

    def test_delete_task_contract(self):
        """Contract test for delete_task operation"""
        # Create a task
        task_to_delete = self.task_service.create_task(title="Task to Delete")

        # Delete the task
        result = self.task_service.delete_task(task_to_delete.id)

        # Verify the return value
        assert result is True

        # Verify the task is gone from storage
        with pytest.raises(ValueError):
            self.task_service.get_task(task_to_delete.id)

        # Verify other tasks are unaffected
        remaining_tasks = self.task_service.list_tasks()
        assert len(remaining_tasks) == 0

    def test_delete_task_not_found(self):
        """Test that delete_task raises ValueError for non-existent task"""
        with pytest.raises(ValueError):
            self.task_service.delete_task("non-existent-id")

    def test_complete_task_contract(self):
        """Contract test for complete_task operation"""
        # Create an incomplete task
        task = self.task_service.create_task(title="Task to Complete", completed=False)

        # Complete the task
        completed_task = self.task_service.complete_task(task.id)

        # Verify the returned task is completed
        assert completed_task.id == task.id
        assert completed_task.completed is True

        # Verify the task is actually completed in storage
        retrieved_task = self.task_service.get_task(task.id)
        assert retrieved_task.completed is True

    def test_complete_task_not_found(self):
        """Test that complete_task raises ValueError for non-existent task"""
        with pytest.raises(ValueError):
            self.task_service.complete_task("non-existent-id")

    def teardown_method(self):
        """Clean up test storage file"""
        import os
        if os.path.exists("test_tasks.json"):
            os.remove("test_tasks.json")