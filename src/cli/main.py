import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from enum import Enum

from src.models.task import Task, Priority
from src.services.task_service import TaskService
from src.lib.storage import Storage

# Initialize Typer app
app = typer.Typer()

# Initialize Rich console
console = Console()

# Initialize services
storage = Storage()
task_service = TaskService(storage)

# Function Create
@app.command()
def create(
    title: str = typer.Option(..., prompt=True, help="Title of the task"),
    description: str = typer.Option("", prompt=True, help="Description of the task"),
    priority: Priority = typer.Option(Priority.MEDIUM, prompt=True, case_sensitive=False,
                                     help="Priority level: high, medium, or low")
):
    """
    Create a new task with title, description, and priority level
    """
    try:
        task = task_service.create_task(
            title=title,
            description=description,
            priority=priority
        )
        console.print(f"[green]Task created successfully![/green]")
        console.print(f"ID: {task.id}")
        console.print(f"Title: {task.title}")
        console.print(f"Description: {task.description}")
        console.print(f"Priority: {task.priority.value}")
        console.print(f"Completed: {'Yes' if task.completed else 'No'}")
    except ValueError as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@app.command()
def list_tasks(
    completed: Optional[bool] = typer.Option(None, "--completed", help="Filter by completion status"),
    priority: Optional[Priority] = typer.Option(None, "--priority", case_sensitive=False,
                                               help="Filter by priority level: high, medium, or low")
):
    """
    List all tasks with optional filtering by completion status and priority
    """
    try:
        tasks = task_service.list_tasks(completed=completed, priority=priority)

        if not tasks:
            console.print("[yellow]No tasks found.[/yellow]")
            return

        table = Table(title="Tasks")
        table.add_column("ID", style="dim", width=36)
        table.add_column("Title", style="bold")
        table.add_column("Description")
        table.add_column("Priority", justify="center")
        table.add_column("Completed", justify="center")

        for task in tasks:
            priority_style = "red" if task.priority == Priority.HIGH else \
                           "yellow" if task.priority == Priority.MEDIUM else "blue"

            table.add_row(
                task.id,
                task.title,
                task.description,
                f"[{priority_style}]{task.priority.value}[/]",
                "Yes" if task.completed else "No"
            )

        console.print(table)

        # Show statistics
        stats = task_service.get_task_statistics()
        console.print(f"\nTotal: {stats['total_count']}, "
                     f"Completed: {stats['completed_count']}, "
                     f"Pending: {stats['pending_count']}")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@app.command()
def update(
    task_id: str = typer.Argument(..., help="ID of the task to update"),
    title: Optional[str] = typer.Option(None, "--title", help="New title for the task"),
    description: Optional[str] = typer.Option(None, "--description", help="New description for the task"),
    priority: Optional[Priority] = typer.Option(None, "--priority", case_sensitive=False,
                                               help="New priority level: high, medium, or low"),
    completed: Optional[bool] = typer.Option(None, "--completed", help="Set completion status")
):
    """
    Update an existing task
    """
    try:
        task = task_service.update_task(
            task_id=task_id,
            title=title,
            description=description,
            priority=priority,
            completed=completed
        )
        console.print(f"[green]Task updated successfully![/green]")
        console.print(f"ID: {task.id}")
        console.print(f"Title: {task.title}")
        console.print(f"Description: {task.description}")
        console.print(f"Priority: {task.priority.value}")
        console.print(f"Completed: {'Yes' if task.completed else 'No'}")
    except ValueError as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@app.command()
def complete(
    task_id: str = typer.Argument(..., help="ID of the task to mark as complete")
):
    """
    Mark a task as completed
    """
    try:
        task = task_service.complete_task(task_id)
        console.print(f"[green]Task marked as completed![/green]")
        console.print(f"ID: {task.id}")
        console.print(f"Title: {task.title}")
    except ValueError as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@app.command()
def delete(
    task_id: str = typer.Argument(..., help="ID of the task to delete")
):
    """
    Delete a task
    """
    try:
        # Confirm deletion
        confirm = Confirm.ask(f"Are you sure you want to delete task {task_id}?")
        if not confirm:
            console.print("[yellow]Deletion cancelled.[/yellow]")
            return

        result = task_service.delete_task(task_id)
        if result:
            console.print(f"[green]Task deleted successfully![/green]")
        else:
            console.print(f"[red]Failed to delete task.[/red]")
    except ValueError as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@app.command()
def menu():
    """
    Start the interactive menu system
    """
    while True:
        console.print("\n[bold blue]CLI Todo App[/bold blue]")
        console.print("1. Create Task")
        console.print("2. List Tasks")
        console.print("3. Update Task")
        console.print("4. Complete Task")
        console.print("5. Delete Task")
        console.print("6. Exit")

        try:
            choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6"])

            if choice == "1":
                title = Prompt.ask("Enter task title")
                description = Prompt.ask("Enter task description (optional)", default="")
                priority_str = Prompt.ask("Enter priority (high/medium/low)", default="medium", choices=["high", "medium", "low"])
                priority = Priority(priority_str.lower())

                try:
                    task = task_service.create_task(title=title, description=description, priority=priority)
                    console.print(f"[green]Task created successfully![/green]")
                except ValueError as e:
                    console.print(f"[red]Error: {str(e)}[/red]")

            elif choice == "2":
                completed_filter = Prompt.ask("Filter by completion status? (all/completed/pending)",
                                            choices=["all", "completed", "pending"], default="all")

                completed = None
                if completed_filter == "completed":
                    completed = True
                elif completed_filter == "pending":
                    completed = False

                priority_filter = Prompt.ask("Filter by priority? (all/high/medium/low)",
                                           choices=["all", "high", "medium", "low"], default="all")

                priority = None
                if priority_filter != "all":
                    priority = Priority(priority_filter)

                tasks = task_service.list_tasks(completed=completed, priority=priority)

                if not tasks:
                    console.print("[yellow]No tasks found.[/yellow]")
                else:
                    table = Table(title="Tasks")
                    table.add_column("ID", style="dim", width=36)
                    table.add_column("Title", style="bold")
                    table.add_column("Description")
                    table.add_column("Priority", justify="center")
                    table.add_column("Completed", justify="center")

                    for task in tasks:
                        priority_style = "red" if task.priority == Priority.HIGH else \
                                       "yellow" if task.priority == Priority.MEDIUM else "blue"

                        table.add_row(
                            task.id,
                            task.title,
                            task.description,
                            f"[{priority_style}]{task.priority.value}[/]",
                            "Yes" if task.completed else "No"
                        )

                    console.print(table)

                    # Show statistics
                    stats = task_service.get_task_statistics()
                    console.print(f"\nTotal: {stats['total_count']}, "
                                 f"Completed: {stats['completed_count']}, "
                                 f"Pending: {stats['pending_count']}")

            elif choice == "3":
                task_id = Prompt.ask("Enter task ID to update")

                # Check if task exists
                try:
                    current_task = task_service.get_task(task_id)

                    console.print(f"Current task: {current_task.title}")

                    new_title = Prompt.ask("Enter new title (or press Enter to keep current)", default=current_task.title)
                    new_description = Prompt.ask("Enter new description (or press Enter to keep current)",
                                              default=current_task.description)
                    new_priority_str = Prompt.ask("Enter new priority (high/medium/low)",
                                                default=current_task.priority.value,
                                                choices=["high", "medium", "low"])
                    new_priority = Priority(new_priority_str.lower())
                    new_completed = Confirm.ask("Mark as completed?", default=current_task.completed)

                    task_service.update_task(
                        task_id=task_id,
                        title=new_title if new_title != current_task.title else None,
                        description=new_description if new_description != current_task.description else None,
                        priority=new_priority if new_priority != current_task.priority else None,
                        completed=new_completed if new_completed != current_task.completed else None
                    )

                    console.print(f"[green]Task updated successfully![/green]")

                except ValueError as e:
                    console.print(f"[red]Error: {str(e)}[/red]")

            elif choice == "4":
                task_id = Prompt.ask("Enter task ID to complete")

                try:
                    task_service.complete_task(task_id)
                    console.print(f"[green]Task marked as completed![/green]")
                except ValueError as e:
                    console.print(f"[red]Error: {str(e)}[/red]")

            elif choice == "5":
                task_id = Prompt.ask("Enter task ID to delete")

                confirm = Confirm.ask(f"Are you sure you want to delete task {task_id}?")
                if not confirm:
                    console.print("[yellow]Deletion cancelled.[/yellow]")
                    continue

                try:
                    task_service.delete_task(task_id)
                    console.print(f"[green]Task deleted successfully![/green]")
                except ValueError as e:
                    console.print(f"[red]Error: {str(e)}[/red]")

            elif choice == "6":
                console.print("[bold green]Goodbye![/bold green]")
                break

        except KeyboardInterrupt:
            console.print("\n[bold green]Goodbye![/bold green]")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")


if __name__ == "__main__":
    app()