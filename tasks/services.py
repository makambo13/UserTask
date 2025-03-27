
from app import db
from .models import Task
from sqlalchemy.exc import SQLAlchemyError

class TaskService:
    
    @staticmethod
    def get_user_tasks(user_id):
        """
        Retrieves a list of tasks for a given user.
        Returns a list of Task objects ordered by creation date.
        """
        try:
            tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()
            return tasks
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback if any error occurs
            raise Exception(f"Error fetching tasks for user {user_id}: {str(e)}")
    
    @staticmethod
    def create_task(user_id, title, description=None, priority='Medium'):
        """
        Creates a new task for a given user.
        Returns the created Task object.
        """
        try:
            task = Task(
                title=title,
                description=description,
                user_id=user_id,
                priority=priority  # Now we are passing the priority parameter
            )
            db.session.add(task)
            db.session.commit()
            return task
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of error
            raise Exception(f"Error creating task for user {user_id}: {str(e)}")
    
    @staticmethod
    def get_task_by_id(task_id):
        """
        Retrieves a task by its ID.
        Returns the Task object if found, or None if not found.
        """
        try:
            task = Task.query.get(task_id)
            return task
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback in case of error
            raise Exception(f"Error fetching task by ID {task_id}: {str(e)}")
