from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending', index=True)
    priority = db.Column(db.String(10), default='Medium', nullable=False)  # New field for priority
    
    # Relationship to User
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

    def __repr__(self):
        return f"<Task {self.id}: {self.title}, Priority: {self.priority}, Status: {self.status}>"

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Task relationship is already defined in the Task model via user_id
    
    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

    # Methods for handling password hashing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
