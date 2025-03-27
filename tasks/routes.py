from flask import Blueprint, render_template, redirect, url_for, request
from tasks.services import TaskService
from tasks.forms import TaskForm

# Initialize Blueprint for task-related routes
tasks_bp = Blueprint('tasks', __name__, template_folder='templates')

# Route to display the task list for a user
@tasks_bp.route('/')
def task_list():
    try:
        tasks = TaskService.get_user_tasks(user_id=1)  # Fetch tasks for user_id=1
        no_tasks_message = None
        if not tasks:
            no_tasks_message = "No tasks found. Create your first task!"

        return render_template(
            'tasks/list.html',  # Template to list tasks
            tasks=tasks,
            no_tasks_message=no_tasks_message,
            form=TaskForm()
        )
    except Exception as e:
        return render_template('tasks/error.html', error=str(e)), 500

# Route to create a task
@tasks_bp.route('/create', methods=['POST'])
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        try:
            TaskService.create_task(
                user_id=1,  # Replace with current_user.id if using Flask-Login
                title=form.title.data,
                description=form.description.data,
                priority=form.priority.data  # Include priority field
            )
            return redirect(url_for('tasks.task_list'))
        except Exception as e:
            return render_template('tasks/error.html', error=str(e)), 500
    return render_template('tasks/list.html', form=form)
