"""
Interactive CLI interface for the todo application.
"""
import inquirer
from src.services.task_service import TaskService
from src.lib.voice_input import get_voice_input
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint
from colorama import init, Fore, Style
import os

# Initialize colorama for cross-platform color support
init()

class InteractiveCLI:
    """
    Interactive command-line interface with menu navigation.
    """
    def __init__(self):
        self.service = TaskService()
        self.console = Console()

    def run(self):
        """
        Start the interactive CLI application.
        """
        # Display welcome message with styling
        welcome_text = Text("Welcome to the CLI Todo Application!", style="bold blue")
        description_text = Text("Manage your tasks efficiently with this interactive tool.", style="italic")

        self.console.print(Panel(welcome_text))
        self.console.print(description_text)
        self.console.print()

        while True:
            # Main menu options with styled prompt
            questions = [
                inquirer.List(
                    'action',
                    message="Select an action",
                    choices=[
                        'Add Task',
                        'View Tasks',
                        'Update Task',
                        'Delete Task',
                        'Mark Task Complete/Incomplete',
                        'Exit'
                    ],
                ),
            ]

            answers = inquirer.prompt(questions)

            if not answers:  # User pressed Ctrl+C
                rprint(f"\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                break

            action = answers['action']

            if action == 'Add Task':
                self._add_task()
            elif action == 'View Tasks':
                self._view_tasks()
            elif action == 'Update Task':
                self._update_task()
            elif action == 'Delete Task':
                self._delete_task()
            elif action == 'Mark Task Complete/Incomplete':
                self._toggle_task_completion()
            elif action == 'Exit':
                rprint(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                break

    def _add_task(self):
        """
        Add a new task through interactive prompts.
        """
        self.console.print(Panel("[bold blue]Add New Task[/bold blue]"))

        # Ask user if they want to use voice input
        input_method_question = [
            inquirer.List(
                'input_method',
                message="How would you like to enter the task?",
                choices=[
                    'Text Input',
                    'Voice Input'
                ],
            ),
        ]

        input_method_answer = inquirer.prompt(input_method_question)
        if not input_method_answer:
            return

        input_method = input_method_answer['input_method']

        title = ""

        if input_method == 'Voice Input':
            # Use voice input to get the task title
            self.console.print("[cyan]Using voice input...[/cyan]")
            voice_result = get_voice_input()

            if voice_result:
                title = voice_result.strip()
                self.console.print(f"[green]Voice input captured: {title}[/green]")

                # Confirm with user if they want to use this title
                confirm_question = [
                    inquirer.Confirm('confirm', message=f"Do you want to use '{title}' as the task title?")
                ]
                confirm_answer = inquirer.prompt(confirm_question)

                if not confirm_answer or not confirm_answer['confirm']:
                    # If user doesn't confirm, fall back to text input
                    self.console.print("[yellow]Voice input rejected. Falling back to text input.[/yellow]")
                    title = self._get_title_text_input()
                else:
                    # Use the voice input as the title
                    pass
            else:
                # Voice input failed or was cancelled, fall back to text input
                self.console.print("[yellow]Voice input failed or cancelled. Falling back to text input.[/yellow]")
                title = self._get_title_text_input()
        else:
            # Use text input
            title = self._get_title_text_input()

        # If title is still empty after all attempts, exit
        if not title:
            self.console.print("[red]Task title cannot be empty. Please try again.[/red]")
            return

        # Optionally get task description
        desc_question = [
            inquirer.Text('description', message="Enter task description (optional, press Enter to skip)")
        ]

        desc_answer = inquirer.prompt(desc_question)
        if not desc_answer:  # User cancelled
            return

        description = desc_answer['description'].strip() or None

        try:
            task_id = self.service.add_task(title, description)
            self.console.print(f"[green]Task added successfully with ID: {task_id}[/green]")
        except ValueError as e:
            self.console.print(f"[red]Error: {e}[/red]")
            # If it was a duplicate task error, ask user if they want to proceed anyway
            if "already exists" in str(e):
                retry_question = [
                    inquirer.Confirm('retry', message="Do you want to try adding a different title?")
                ]
                retry_answer = inquirer.prompt(retry_question)
                if retry_answer and retry_answer['retry']:
                    self._add_task()  # Recursive call to try again

    def _get_title_text_input(self):
        """
        Helper method to get task title via text input
        """
        title_question = [
            inquirer.Text('title', message="Enter task title")
        ]

        title_answer = inquirer.prompt(title_question)
        if not title_answer:
            return ""

        return title_answer['title'].strip()

    def _view_tasks(self):
        """
        View all tasks in the list.
        """
        self.console.print(Panel("[bold blue]View Tasks[/bold blue]"))

        tasks = self.service.get_all_tasks()

        if not tasks:
            self.console.print("[yellow]No tasks found.[/yellow]")
            return

        # Create a rich table for displaying tasks
        table = Table(title=f"Total tasks: {len(tasks)}", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=5)
        table.add_column("Status", style="dim", width=10)
        table.add_column("Title", min_width=20)
        table.add_column("Description", min_width=30)

        for task in tasks:
            status_symbol = "✓" if task['completed'] else "○"
            status_color = "green" if task['completed'] else "red"
            status_text = f"[{status_color}]{status_symbol} {'Completed' if task['completed'] else 'Pending'}[/{status_color}]"

            title_color = "green strike" if task['completed'] else "white"
            title_text = f"[{title_color}]{task['title']}[/{title_color}]"

            description = task['description'] or ""
            table.add_row(str(task['id']), status_text, title_text, description)

        self.console.print(table)

        # Add pagination for large task lists
        if len(tasks) > 20:
            self.console.print(f"[cyan]Note: Showing {len(tasks)} tasks. Consider using filters for easier navigation.[/cyan]")

    def _update_task(self):
        """
        Update an existing task.
        """
        self.console.print(Panel("[bold blue]Update Task[/bold blue]"))

        tasks = self.service.get_all_tasks()

        if not tasks:
            self.console.print("[yellow]No tasks available to update.[/yellow]")
            return

        # Create a list of task choices for selection
        task_choices = [f"ID: {task['id']} - {task['title']}" for task in tasks]
        task_choices.append("Back to main menu")

        task_selection = [
            inquirer.List(
                'selected_task',
                message="Select a task to update",
                choices=task_choices,
            ),
        ]

        task_answer = inquirer.prompt(task_selection)
        if not task_answer or task_answer['selected_task'] == "Back to main menu":
            return

        # Extract task ID from selection
        selected_text = task_answer['selected_task']
        # Handle the format "ID: X - title" and extract the ID
        if selected_text.startswith("ID: "):
            task_id_str = selected_text.split()[1]  # Get "X" from "ID: X - title"
            task_id = int(task_id_str)
        else:
            # If it's the "Back to main menu" option, return early
            return

        # Get current task to show existing values
        current_task = self.service.get_task_by_id(task_id)
        if not current_task:
            self.console.print(f"[red]Error: No task found with ID {task_id}[/red]")
            return

        # Get new title
        title_question = [
            inquirer.Text('title', message=f"Enter new title (current: '{current_task['title']}')")
        ]

        title_answer = inquirer.prompt(title_question)
        if not title_answer:
            return

        # Use new title or keep current if empty
        new_title = title_answer['title'].strip()
        if not new_title:
            new_title = current_task['title']

        # Get new description
        current_desc = current_task['description'] or ''
        desc_question = [
            inquirer.Text('description', message=f"Enter new description (current: '{current_desc}')")
        ]

        desc_answer = inquirer.prompt(desc_question)
        if not desc_answer:
            return

        # Use new description or keep current if empty, convert empty string to None
        new_description = desc_answer['description'].strip()
        if not new_description:
            new_description = current_task['description']

        try:
            success = self.service.update_task(task_id, new_title, new_description)
            if success:
                self.console.print("[green]Task updated successfully![/green]")
            else:
                self.console.print(f"[red]No task found with ID: {task_id}[/red]")
        except ValueError as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def _delete_task(self):
        """
        Delete a task.
        """
        self.console.print(Panel("[bold blue]Delete Task[/bold blue]"))

        tasks = self.service.get_all_tasks()

        if not tasks:
            self.console.print("[yellow]No tasks available to delete.[/yellow]")
            return

        # Create a list of task choices for selection
        task_choices = [f"ID: {task['id']} - {task['title']}" for task in tasks]
        task_choices.append("Back to main menu")

        task_selection = [
            inquirer.List(
                'selected_task',
                message="Select a task to delete",
                choices=task_choices,
            ),
        ]

        task_answer = inquirer.prompt(task_selection)
        if not task_answer or task_answer['selected_task'] == "Back to main menu":
            return

        # Extract task ID from selection
        selected_text = task_answer['selected_task']
        # Handle the format "ID: X - title" and extract the ID
        if selected_text.startswith("ID: "):
            task_id_str = selected_text.split()[1]  # Get "X" from "ID: X - title"
            task_id = int(task_id_str)
        else:
            # If it's the "Back to main menu" option, return early
            return

        # Verify task exists before attempting deletion
        task_to_delete = self.service.get_task_by_id(task_id)
        if not task_to_delete:
            self.console.print(f"[red]Error: No task found with ID {task_id}. Cannot delete non-existent task.[/red]")
            return

        confirm_question = [
            inquirer.Confirm('confirm', message=f"Are you sure you want to delete task '{task_to_delete['title']}' (ID: {task_id})?")
        ]

        confirm_answer = inquirer.prompt(confirm_question)
        if not confirm_answer or not confirm_answer['confirm']:
            self.console.print("[yellow]Deletion cancelled.[/yellow]")
            return

        try:
            success = self.service.delete_task(task_id)
            if success:
                self.console.print("[green]Task deleted successfully![/green]")
            else:
                self.console.print(f"[red]No task found with ID: {task_id}[/red]")
        except ValueError as e:
            self.console.print(f"[red]Error: {e}[/red]")

    def _toggle_task_completion(self):
        """
        Toggle task completion status.
        """
        self.console.print(Panel("[bold blue]Mark Task Complete/Incomplete[/bold blue]"))

        tasks = self.service.get_all_tasks()

        if not tasks:
            self.console.print("[yellow]No tasks available.[/yellow]")
            return

        # Create a list of task choices for selection
        task_choices = []
        for task in tasks:
            status = "✓" if task['completed'] else "○"
            task_choices.append(f"[{status}] ID: {task['id']} - {task['title']}")
        task_choices.append("Back to main menu")

        task_selection = [
            inquirer.List(
                'selected_task',
                message="Select a task to toggle completion status",
                choices=task_choices,
            ),
        ]

        task_answer = inquirer.prompt(task_selection)
        if not task_answer or task_answer['selected_task'] == "Back to main menu":
            return

        # Extract task ID from selection
        selected_text = task_answer['selected_task']
        # Handle the format "[X] ID: X - title" and extract the ID
        if selected_text.startswith("[") and " ID: " in selected_text:
            # Split by " ID: " and take the part after, then split and get the ID
            id_part = selected_text.split(" ID: ")[1]  # Get "X - title"
            task_id_str = id_part.split()[0]  # Get "X"
            task_id = int(task_id_str)
        else:
            # If it's the "Back to main menu" option, return early
            return

        try:
            success = self.service.toggle_task_completion(task_id)
            if success:
                # Get updated task to show new status
                updated_task = self.service.get_task_by_id(task_id)
                status = "completed" if updated_task['completed'] else "pending"
                status_icon = "✓" if updated_task['completed'] else "○"
                self.console.print(f"[green]Task marked as {status}! [{status_icon}][/green]")
            else:
                self.console.print(f"[red]No task found with ID: {task_id}[/red]")
        except ValueError as e:
            self.console.print(f"[red]Error: {e}[/red]")