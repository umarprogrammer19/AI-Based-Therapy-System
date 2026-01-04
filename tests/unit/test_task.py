import pytest
from datetime import datetime
from src.models.task import Task, Priority


class TestTaskModel:
    """Unit tests for Task model validation"""

    def test_task_creation_with_valid_data(self):
        """Test creating a task with valid data"""
        task = Task(
            title="Test Task",
            description="Test Description",
            priority=Priority.HIGH,
            completed=False
        )

        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.priority == Priority.HIGH
        assert task.completed is False
        assert task.id is not None
        assert task.created_at is not None
        assert task.updated_at is not None

    def test_task_creation_with_defaults(self):
        """Test creating a task with default values"""
        task = Task(title="Test Task")

        assert task.title == "Test Task"
        assert task.description == ""
        assert task.priority == Priority.MEDIUM
        assert task.completed is False

    def test_task_title_validation_empty(self):
        """Test that empty title raises ValueError"""
        with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
            Task(title="")

    def test_task_title_validation_too_long(self):
        """Test that title longer than 200 characters raises ValueError"""
        long_title = "A" * 201
        with pytest.raises(ValueError, match="Title must be between 1 and 200 characters"):
            Task(title=long_title)

    def test_task_title_validation_correct_length(self):
        """Test that title with 200 characters is valid"""
        title_200_chars = "A" * 200
        task = Task(title=title_200_chars)
        assert task.title == title_200_chars

    def test_task_description_validation_too_long(self):
        """Test that description longer than 1000 characters raises ValueError"""
        long_description = "A" * 1001
        with pytest.raises(ValueError, match="Description must be 1000 characters or less"):
            Task(title="Test", description=long_description)

    def test_task_priority_validation(self):
        """Test that invalid priority raises ValueError"""
        with pytest.raises(ValueError, match="Priority must be one of: 'high', 'medium', 'low'"):
            Task(title="Test", priority="invalid_priority")

    def test_task_update_method(self):
        """Test updating task attributes"""
        task = Task(title="Original Title", description="Original Description", priority=Priority.LOW)

        task.update(
            title="Updated Title",
            description="Updated Description",
            priority=Priority.HIGH,
            completed=True
        )

        assert task.title == "Updated Title"
        assert task.description == "Updated Description"
        assert task.priority == Priority.HIGH
        assert task.completed is True

    def test_task_update_partial(self):
        """Test updating only some attributes of a task"""
        task = Task(title="Original Title", description="Original Description", priority=Priority.LOW)

        original_created_at = task.created_at
        task.update(title="Updated Title")

        assert task.title == "Updated Title"
        assert task.description == "Original Description"  # Should remain unchanged
        assert task.priority == Priority.LOW  # Should remain unchanged
        assert task.created_at == original_created_at  # Should remain unchanged
        assert task.updated_at > original_created_at  # Should be updated

    def test_task_mark_completed(self):
        """Test marking a task as completed"""
        task = Task(title="Test Task", completed=False)
        assert task.completed is False

        task.mark_completed()
        assert task.completed is True

    def test_task_to_dict_and_from_dict(self):
        """Test serialization and deserialization of a task"""
        original_task = Task(
            title="Test Title",
            description="Test Description",
            priority=Priority.HIGH,
            completed=True
        )

        task_dict = original_task.to_dict()
        reconstructed_task = Task.from_dict(task_dict)

        assert original_task.id == reconstructed_task.id
        assert original_task.title == reconstructed_task.title
        assert original_task.description == reconstructed_task.description
        assert original_task.priority == reconstructed_task.priority
        assert original_task.completed == reconstructed_task.completed
        assert original_task.created_at == reconstructed_task.created_at
        assert original_task.updated_at == reconstructed_task.updated_at