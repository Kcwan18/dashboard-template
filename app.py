from flask import Flask
from flask_login import LoginManager
import atexit

from config import Config
from models import db, User
from routes import init_routes
from scheduler import init_scheduler

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Initialize routes
    init_routes(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        _create_default_users()
    
    return app

def _create_default_users():
    """Create default users if they don't exist"""
    default_users = [
        ('competitor1', 'Cdc@2025AUD', '676878928656'),
        ('competitor2', 'Cdc@2025DKE', '457550570914'),
        ('competitor3', 'Cdc@2025QUP', '937554351945'),
        ('competitor4', 'Cdc@2025USD', '211669975908')
    ]
    
    for username, password, aws_account_id in default_users:
        if not User.query.filter_by(username=username).first():
            user = User(username=username, password=password, aws_account_id=aws_account_id)
            db.session.add(user)
            print(f"Created default user: {username}")
    
    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    
    # Start background scheduler
    scheduler = init_scheduler(app)
    atexit.register(lambda: scheduler.shutdown())
    
    # Run application
    print("Starting Game Dashboard Application...")
    print(f"Check interval: {Config.CHECK_INTERVAL_SECONDS} seconds")
    print(f"Points per successful check: {Config.POINTS_PER_CHECK}")
    app.run(debug=True, port=5000, use_reloader=False)
