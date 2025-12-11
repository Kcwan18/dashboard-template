# Game Dashboard Application

This is a Flask-based web application for the GameDay competition. It allows users to register/login, submit URLs for health checking, and earn points based on the availability of their services.

## Project Structure

```
dashboard/
├── app.py              # Main application entry point
├── config.py           # Configuration settings
├── models.py           # Database models
├── routes.py           # Route handlers
├── checker.py          # URL checking logic
├── scheduler.py        # Background task scheduler
├── requirements.txt    # Python dependencies
├── Makefile           # Build and run commands
├── templates/         # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── score_history.html
│   └── leaderboard.html
└── db.sqlite          # SQLite database (created at runtime)
```

## Features

1.  **User Authentication**: Login and registration system.
2.  **URL Monitoring**: Users submit two types of URLs:
    -   Application URL: Checked for specific text content
    -   API Gateway URL: Checked for specific JSON response
3.  **Scoring System**: Automated checks every minute award points for valid responses.
4.  **Score History**: Users can view their complete scoring history with timestamps and reasons.
5.  **Leaderboard**: Real-time ranking of all users based on their scores.
6.  **Auto-refresh**: Dashboard automatically refreshes every 60 seconds.

## Pre-configured Users

The application comes with 4 pre-configured users for testing:

| Username | Password |
|----------|----------|
| user1    | password123 |
| user2    | password123 |
| user3    | password123 |
| user4    | password123 |

## Installation & Running

1.  **Install Dependencies**:
    ```bash
    make install
    ```

2.  **Run the Application**:
    ```bash
    make run
    ```

3.  **Access the Dashboard**:
    Open your browser and navigate to: `http://localhost:5000`

## Makefile Commands

-   `make install`: Install required Python packages
-   `make run`: Start the Flask application
-   `make clean`: Remove Python cache files
-   `make reset-db`: Delete the database (will be recreated on next run)

## How to Play

1.  Login with one of the pre-configured users or register a new one.
2.  In the Dashboard, enter your URLs:
    -   **Application URL**: Your deployed application endpoint
    -   **API Gateway URL**: Your API Gateway endpoint
3.  Click "Update URLs".
4.  The system will check your URLs every minute.
5.  Check "Score History" to see detailed scoring events.
6.  View the "Leaderboard" to see your ranking!

## Configuration

Edit `config.py` to modify:
-   Check interval (default: 60 seconds)
-   Points per successful check (default: 10)
-   Required text/JSON content
-   Request timeout settings

