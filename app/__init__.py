from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize the db
db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # App Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'tasks.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Tests pass their own settings, such as an in-memory database
    if test_config:
        app.config.update(test_config)

    # Initialize Migrate with app and db
    migrate = Migrate(app, db)

    # Initialize the database with app
    db.init_app(app)

    # Import and Register Blueprint
    from tasks.routes import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/tasks')

    # Create all tables (only for development, use migrations for production)
    with app.app_context():
        db.create_all()  # You can remove this if you prefer migrations for schema changes

    # Home route
    @app.route('/')
    def home():
        return render_template('tasks/landing_page.html')

    return app
