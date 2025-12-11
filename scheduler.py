from apscheduler.schedulers.background import BackgroundScheduler
from models import db, User
from checker import URLChecker
from config import Config

def check_all_urls(app):
    """Background task to check all user URLs"""
    with app.app_context():
        users = User.query.all()
        
        for user in users:
            URLChecker.check_application_url(user, app)
            URLChecker.check_api_url(user, app)
            
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Database commit error for user {user.username}: {e}")

def init_scheduler(app):
    """Initialize and start the background scheduler"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: check_all_urls(app),
        trigger="interval",
        seconds=Config.CHECK_INTERVAL_SECONDS,
        id='url_checker',
        replace_existing=True
    )
    scheduler.start()
    return scheduler
