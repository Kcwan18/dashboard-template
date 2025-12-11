import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Scoring configuration
    APP_URL_REQUIRED_TEXT = "Unicorn.Rentals Mobile API Service"
    API_ACCOUNT_ID = "361574505353"
    REQUEST_TIMEOUT = 5
    POINTS_PER_CHECK = 10
    CHECK_INTERVAL_SECONDS = 60
